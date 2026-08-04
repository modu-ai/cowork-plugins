"""SQLite 백업 발행 큐 — stdlib sqlite3 만 사용 (추가 의존성 없음).

Threads 발행 전 작업을 보관하는 로컬 큐다. MCP 서버(server.py) 와 runner CLI
(runner.py) 양쪽에서 같은 DB 파일을 공유한다. 모든 메서드는 동기식이며 평범한
dict 를 반환한다.

상태 머신 (state machine)::

    PENDING → APPROVED → PUBLISHED
                       ↘ FAILED   (재시도 정책은 M3+, M2 에서는 FAILED 종단)

축 (axes):
  - ``platform`` (``threads`` | ``instagram``): 각 row 가 어느 플랫폼으로 발행되는지
    구분. 기본 ``threads`` — 기존 Threads-only 호출자는 바꿀 필요 없음 (REQ-INST-023).
    runner 가 row 의 platform 을 보고 ``ThreadsClient`` / ``InstagramClient`` 로 분기.

설계 참고 (design notes):
  - DB 경로 해석은 호출자(server.py / runner.py) 책임이다 — 본 모듈은 ``db_path``
    생성자 인자만 받는다 (테스트는 tmp 경로 주입).
  - 시간 의존 로직(``scheduled_at`` 비교, 24h 카운트) 은 주입 가능한 ``clock``
    callable 에 의존한다 — 테스트는 고정 clock 을 주입해 결정적 결과를 얻는다.
  - 스키마 생성은 ``CREATE TABLE IF NOT EXISTS`` 로 멱등이다 (같은 경로를 다시
    열어도 에러 없음, 기존 데이터 보존).
  - ``platform`` 컬럼은 PRAGMA-guarded ALTER 로 멱등 추가된다 — SQLite ALTER 는
    ``IF NOT EXISTS`` 를 지원하지 않으므로 ``PRAGMA table_info`` 로 존재 확인 후 추가.
    구(Threads-only) DB 를 열면 기존 row 전체가 ``platform='threads'`` 기본값으로
    제자리 마이그레이션된다 (데이터 손실 없음, REQ-INST-012).
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

# 큐가 받아들이는 media_type. REELS 은 Instagram 전용 라벨 (Threads 에는 없음) 이지만
# 통합 큐는 플랫폼 무관 저장소이므로 허용한다 — runner 가 platform 별로 발행 시맨틱을 결정한다.
# CAROUSEL 풀 플로우는 범위 밖(spec §H).
_VALID_MEDIA_TYPES = {"TEXT", "IMAGE", "VIDEO", "REELS"}
_VALID_STATUSES = {"PENDING", "APPROVED", "PUBLISHED", "FAILED"}
# 큐가 받아들이는 platform (SPEC-THREADS-POSTER-INSTAGRAM-001). 'threads' 가 기본값이라
# 기존 Threads-only 호출자는 아무것도 바꾸지 않아도 그대로 동작한다 (REQ-INST-023).
_VALID_PLATFORMS = {"threads", "instagram"}


def now_iso() -> str:
    """현재 시각을 ISO-8601 문자열로 반환 (non-Queue 호출자용 helper).

    Queue 인스턴스 내부에서는 주입된 clock 을 쓰지만, server/runner 처럼
    Queue 밖에서 단발적으로 "지금" 이 필요한 호출자는 이 helper 를 쓴다.
    """
    return datetime.now().isoformat()


class Queue:
    """SQLite 백업 발행 큐 (SQLite-backed publish queue).

    Args:
        db_path: SQLite DB 파일 경로. 부모 디렉토리가 없으면 생성한다.
        clock: 현재 시각을 반환하는 callable (기본 ``datetime.now``).
            ``scheduled_at`` 비교와 24h 카운트의 기준 시각을 결정한다 —
            테스트는 고정 clock 을 주입해 시간 의존 동작을 결정적으로 만든다.
    """

    def __init__(self, db_path: str, *, clock: Callable[[], datetime] = datetime.now):
        self._db_path = db_path
        self._clock = clock
        parent = os.path.dirname(db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        # WAL + busy_timeout: MCP 서버 프로세스와 runner 프로세스가 같은 DB 를
        # 동시에 열 때의 경합을 완화한다 (multi-process 안전성).
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA busy_timeout=5000")
        self._migrate()

    # ------------------------------------------------------------------ schema
    def _migrate(self) -> None:
        """멱등 스키마 마이그레이션 (idempotent schema setup).

        ``CREATE ... IF NOT EXISTS`` 로 보호되어 같은 DB 를 다시 열어도 안전하다.
        ``platform`` 컬럼은 PRAGMA-guarded ALTER 로 추가한다 — SQLite 가
        ``ALTER TABLE ... ADD COLUMN IF NOT EXISTS`` 를 지원하지 않기 때문에
        ``PRAGMA table_info(posts)`` 로 컬럼 존재를 확인한 뒤 없을 때만 ADD COLUMN.
        구(Threads-only) DB 의 기존 row 는 ``platform='threads'`` 기본값으로 채워진다.
        """
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                media_type    TEXT    NOT NULL,
                text          TEXT,
                image_url     TEXT,
                video_url     TEXT,
                status        TEXT    NOT NULL DEFAULT 'PENDING',
                scheduled_at  TEXT,
                approved_at   TEXT,
                published_at  TEXT,
                container_id  TEXT,
                media_id      TEXT,
                permalink_hint TEXT,
                attempts      INTEGER NOT NULL DEFAULT 0,
                last_error    TEXT,
                created_at    TEXT    NOT NULL,
                updated_at    TEXT    NOT NULL
            )
            """
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status)"
        )
        # platform 컬럼 멱등 추가 (REQ-INST-011). SQLite ALTER 는 IF NOT EXISTS 를
        # 지원하지 않으므로 PRAGMA table_info 로 가드한다. NOT NULL + DEFAULT 'threads'
        # 라 기존 row 전체가 안전하게 threads 로 제자리 마이그레이션된다.
        existing_cols = {
            row[1] for row in self._conn.execute("PRAGMA table_info(posts)").fetchall()
        }
        if "platform" not in existing_cols:
            self._conn.execute(
                "ALTER TABLE posts ADD COLUMN platform TEXT NOT NULL DEFAULT 'threads'"
            )
        self._conn.commit()

    # ------------------------------------------------------------------ internal
    def _now_iso(self) -> str:
        """주입된 clock 기반 ISO 시각 (injected-clock ISO timestamp)."""
        return self._clock().isoformat()

    # ------------------------------------------------------------------ API
    def enqueue(
        self,
        media_type: str,
        *,
        text: Optional[str] = None,
        image_url: Optional[str] = None,
        video_url: Optional[str] = None,
        scheduled_at: Optional[str] = None,
        status: str = "PENDING",
        platform: str = "threads",
    ) -> int:
        """큐에 포스트 추가 → row id 반환 (add a post to the queue).

        Args:
            media_type: ``TEXT`` | ``IMAGE`` | ``VIDEO``.
            text: 본문/캡션 (선택). TEXT 포스트의 경우 발행 시점에 필수.
            image_url: 공개 이미지 URL (IMAGE 포스트 필수).
            video_url: 공개 비디오 URL (VIDEO 포스트 필수).
            scheduled_at: 발행 예정 시각(ISO-8601). 미지정 시 NULL (즉시 due).
            status: 초기 상태(기본 ``PENDING``). ``APPROVED`` 직접 enqueue 도 허용.
            platform: ``threads`` (기본) | ``instagram``. runner 가 어느 플랫폼
                클라이언트로 발행할지 결정. 기본 ``threads`` 로 기존 Threads-only
                호출자는 바꿀 필요 없다 (REQ-INST-023).

        Returns:
            새 row 의 ``id``.
        """
        if media_type not in _VALID_MEDIA_TYPES:
            raise ValueError(
                f"지원하지 않는 media_type 입니다 (unsupported media_type): {media_type!r}. "
                f"허용값 (allowed): TEXT, IMAGE, VIDEO, REELS"
            )
        if status not in _VALID_STATUSES:
            raise ValueError(
                f"지원하지 않는 status 입니다 (unsupported status): {status!r}. "
                f"허용값 (allowed): PENDING, APPROVED, PUBLISHED, FAILED"
            )
        if platform not in _VALID_PLATFORMS:
            raise ValueError(
                f"지원하지 않는 platform 입니다 (unsupported platform): {platform!r}. "
                f"허용값 (allowed): threads, instagram"
            )
        now = self._now_iso()
        cur = self._conn.execute(
            """
            INSERT INTO posts
                (media_type, text, image_url, video_url, status,
                 scheduled_at, platform, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (media_type, text, image_url, video_url, status, scheduled_at, platform, now, now),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def approve(self, post_id: int, scheduled_at: Optional[str] = None) -> bool:
        """``PENDING`` → ``APPROVED`` 전환 (flip status to APPROVED).

        ``scheduled_at`` 미지정 시 현재 시각을 발행 예정으로 기록한다 (즉시 due).
        이미 예약된 포스트의 시각을 덮어쓰려면 명시적으로 전달할 것.

        Returns:
            해당 row 가 갱신되었으면 ``True``, row 가 없으면 ``False``.
        """
        now = self._now_iso()
        effective_schedule = scheduled_at if scheduled_at is not None else now
        cur = self._conn.execute(
            """
            UPDATE posts
               SET status       = 'APPROVED',
                   approved_at  = ?,
                   scheduled_at = ?,
                   updated_at   = ?
             WHERE id = ?
            """,
            (now, effective_schedule, now, post_id),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def get(self, post_id: int) -> Optional[dict[str, Any]]:
        """단일 포스트 조회 (fetch one post). 없으면 ``None``."""
        cur = self._conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = cur.fetchone()
        return dict(row) if row is not None else None

    def list(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        platform: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """포스트 목록 (list posts, newest first by id desc).

        Args:
            status: 상태 필터(선택). 미지정 시 전체 상태.
            limit: 최대 행 수.
            platform: 플랫폼 필터(선택, ``threads`` | ``instagram``). 미지정 시 전체 플랫폼.
        """
        clauses: list[str] = []
        params: list[Any] = []
        if status is not None:
            clauses.append("status = ?")
            params.append(status)
        if platform is not None:
            clauses.append("platform = ?")
            params.append(platform)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        params.append(limit)
        cur = self._conn.execute(
            f"SELECT * FROM posts{where} ORDER BY id DESC LIMIT ?", params
        )
        return [dict(r) for r in cur.fetchall()]

    def due(
        self, now: Optional[str] = None, platform: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """발행 대기(``APPROVED``) 중 만료된 포스트 반환 (return due APPROVED posts).

        조건 (conditions):
          - ``status = 'APPROVED'``
          - ``scheduled_at IS NULL`` 이거나 ``scheduled_at <= now``
          - (``PUBLISHED`` / ``FAILED`` 는 status 필터로 이미 제외됨)

        Args:
            now: 기준 시각 ISO-8601. 미지정 시 주입된 ``clock()`` 사용.
            platform: 플랫폼 필터(선택, ``threads`` | ``instagram``). 미지정 시 전체 플랫폼.

        Returns:
            due 포스트 리스트 (id 오름차순 — 선입선출).
        """
        now_iso_value = now if now is not None else self._now_iso()
        if platform is not None:
            cur = self._conn.execute(
                """
                SELECT * FROM posts
                 WHERE status = 'APPROVED'
                   AND platform = ?
                   AND (scheduled_at IS NULL OR scheduled_at <= ?)
                 ORDER BY id ASC
                """,
                (platform, now_iso_value),
            )
        else:
            cur = self._conn.execute(
                """
                SELECT * FROM posts
                 WHERE status = 'APPROVED'
                   AND (scheduled_at IS NULL OR scheduled_at <= ?)
                 ORDER BY id ASC
                """,
                (now_iso_value,),
            )
        return [dict(r) for r in cur.fetchall()]

    def mark_published(
        self,
        post_id: int,
        *,
        container_id: str,
        media_id: str,
        permalink_hint: Optional[str] = None,
    ) -> bool:
        """발행 성공 기록 (record successful publish).

        ``status`` → ``PUBLISHED``, ``published_at`` / ``container_id`` / ``media_id``
        를 채우고 ``last_error`` 를 제거한다.
        """
        now = self._now_iso()
        cur = self._conn.execute(
            """
            UPDATE posts
               SET status         = 'PUBLISHED',
                   published_at   = ?,
                   container_id   = ?,
                   media_id       = ?,
                   permalink_hint = ?,
                   last_error     = NULL,
                   updated_at     = ?
             WHERE id = ?
            """,
            (now, container_id, media_id, permalink_hint, now, post_id),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def mark_failed(self, post_id: int, *, error: str) -> bool:
        """발행 실패 기록 (record failed attempt).

        M2 에서는 FAILED 가 종단 상태다 (재시도 정책은 M3+).
        """
        now = self._now_iso()
        cur = self._conn.execute(
            """
            UPDATE posts
               SET status     = 'FAILED',
                   last_error = ?,
                   updated_at = ?
             WHERE id = ?
            """,
            (error, now, post_id),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def increment_attempt(self, post_id: int) -> None:
        """시도 횟수 +1 (bump attempts counter). 발행 시도 직전에 호출."""
        self._conn.execute(
            "UPDATE posts SET attempts = attempts + 1, updated_at = ? WHERE id = ?",
            (self._now_iso(), post_id),
        )
        self._conn.commit()

    def published_in_last_24h(self) -> int:
        """최근 24시간 내 발행 성공 수 (Threads 24h 한도 250 참고용).

        ``clock() - 24h`` 이후에 ``published_at`` 이 찍힌 PUBLISHED row 수.
        """
        cutoff = (self._clock() - timedelta(hours=24)).isoformat()
        cur = self._conn.execute(
            """
            SELECT COUNT(*) AS n FROM posts
             WHERE status = 'PUBLISHED'
               AND published_at IS NOT NULL
               AND published_at >= ?
            """,
            (cutoff,),
        )
        row = cur.fetchone()
        return int(row["n"]) if row is not None else 0

    # ------------------------------------------------------------------ lifecycle
    def close(self) -> None:
        """연결 종료 (close the SQLite connection)."""
        self._conn.close()

    def __enter__(self) -> "Queue":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
