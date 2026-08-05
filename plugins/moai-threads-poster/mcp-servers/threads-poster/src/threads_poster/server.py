"""moai-threads-poster MCP 서버 — stdio 진입점 (stdio MCP server, entry point).

Threads(Meta) Graph API 로 텍스트·이미지·비디오를 발행하는 즉시 발행 도구 5종과
SQLite 발행 큐 관리 도구 5종(M2) 을 노출한다. 자격증명은 환경변수
(``THREADS_ACCESS_TOKEN``, ``THREADS_USER_ID``) 에서 읽는다 — 미설정 시 서버는
크래시하지 않고, 각 도구가 설정 안내(setup_required) 에러를 반환한다.

즉시 발행 도구 (immediate-publish tools):
  - ``threads_publish_text``   : 텍스트 게시
  - ``threads_publish_image``  : 이미지 게시
  - ``threads_publish_video``  : 비디오 게시
  - ``threads_get_profile``    : 프로필 조회 (health check)
  - ``threads_refresh_token``  : 장기 토큰 수동 갱신

큐 관리 도구 (queue-management tools, M2 + 분산 등록):
  - ``threads_queue_add``          : 큐에 PENDING 포스트 추가
  - ``threads_queue_add_batch``    : 초안 여러 개를 베스트 슬롯에 분산 등록(batch)
  - ``threads_queue_approve``      : PENDING → APPROVED 승인
  - ``threads_queue_list``         : 큐 목록 조회
  - ``threads_queue_get``          : 단일 포스트 상세
  - ``threads_queue_publish_due``  : due 큐 수동 처리 (세션 안 발행 — runner._process 재사용)

문체 프로필 도구 (style profile tools — Threads 자격증명 불필요, 로컬 파일 I/O):
  - ``threads_style_save``         : 문체 프로필 마크다운을 디스크에 저장
  - ``threads_style_load``         : 저장된 문체 프로필 조회 (없으면 exists=False)

멀티 채널 포맷 도구 (multi-channel formatter — 발행 안 함, 포맷만):
  - ``threads_format_multi_channel`` : Threads/Facebook/X 용으로 텍스트 변형.
    Threads=큐 도구용, Facebook·X=복붙용. X 는 x_tier(free/premium) 에 따라 분할.
"""

from __future__ import annotations

import os
import re
import time
from datetime import date, datetime, timedelta
from typing import Any, Callable, Optional
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import FastMCP

from .queue import Queue
from .runner import _default_db_path, _process as run_queue_once
from .threads_api import ThreadsAPIError, ThreadsClient
from .instagram_api import InstagramAPIError, InstagramClient

# Threads 권장: container 생성 후 평균 ~30초 대기 후 publish.
# Recommended: wait ~30s on average between create_container and publish.
DEFAULT_PUBLISH_DELAY = 30.0

# 분산 발행 케이던스 — Asia/Seoul 표준시, 베스트 프랙티스 주 3-5회 화/수/목.
# Distributed-publishing cadence constants (Asia/Seoul, best-practice Tue/Wed/Thu).
SEOUL_TZ = ZoneInfo("Asia/Seoul")
# Python weekday(): 월=0, 화=1, 수=2, 목=3, 금=4, 토=5, 일=6.
_BATCH_SLOT_HOUR = 12  # 피크 점심 슬롯 12:00 (cadence.peak 참고).
_WEEKLY_3_DAYS = (1, 2, 3)  # 화·수·목 — 주 3회 기본 케이던스.
_WEEKLY_5_DAYS = (0, 1, 2, 3, 4)  # 월-금 — 주 5회(매일 평일) 케이던스.
_VALID_BATCH_CADENCES = ("weekly_3", "weekly_5", "manual")
_VALID_BATCH_MEDIA_TYPES = ("TEXT", "IMAGE", "VIDEO")

_INSTRUCTIONS = (
    "Threads(Meta) Graph API 자동 포스팅 MCP. "
    "텍스트·이미지·비디오 2단계 발행(create container → publish), "
    "프로필 조회(health check), 장기 토큰 갱신. "
    "OAuth2 Bearer access_token. 사전 설정: THREADS_ACCESS_TOKEN, THREADS_USER_ID 환경변수."
)
mcp: FastMCP = FastMCP("moai-threads-poster", instructions=_INSTRUCTIONS)

_client_singleton: Optional[ThreadsClient] = None


# ------------------------------------------------------------------ helpers
def _load_credentials() -> tuple[str, str]:
    """환경변수에서 자격증명 읽기 (read credentials from env)."""
    return (
        os.environ.get("THREADS_ACCESS_TOKEN", ""),
        os.environ.get("THREADS_USER_ID", ""),
    )


def _setup_required_error() -> dict[str, Any]:
    """자격증명 미설정 시 돌려줄 구조화 에러 (structured error when creds are absent)."""
    return {
        "error": True,
        "setup_required": True,
        "message": (
            "Threads 자격증명이 설정되지 않았습니다 "
            "(Threads credentials not configured). "
            "THREADS_ACCESS_TOKEN, THREADS_USER_ID 환경변수를 설정하세요. "
            "발급 절차는 mcp-servers/threads-poster/CONNECTORS.md 참조."
        ),
    }


def _get_client() -> Optional[ThreadsClient]:
    """싱글톤 클라이언트 반환 (lazy). 자격증명 미설정 시 ``None``."""
    global _client_singleton
    if _client_singleton is not None:
        return _client_singleton
    access_token, user_id = _load_credentials()
    if not access_token or not user_id:
        return None
    _client_singleton = ThreadsClient(
        access_token=access_token, threads_user_id=user_id
    )
    return _client_singleton


def _reset_client_for_tests() -> None:
    """테스트 전용: 싱글톤 캐시 초기화 (tests only: reset singleton cache)."""
    global _client_singleton
    if _client_singleton is not None:
        _client_singleton.close()
    _client_singleton = None


# --- Instagram (Facebook Login for Business) 싱글톤 — SPEC-THREADS-POSTER-INSTAGRAM-001
# Threads 자격증명과 *독립적인* 두 번째 자격증명 쌍(IG_ACCESS_TOKEN / IG_USER_ID).
# lazy 싱글톤 — IG 도구가 호출될 때만 빌드된다 (Threads-only 세션은 IG 클라이언트를 절대
# 만들지 않는다 → IG_ACCESS_TOKEN/IG_USER_ID 를 읽지 않음, REQ-INST-023).
_ig_client_singleton: Optional[InstagramClient] = None


def _load_ig_credentials() -> tuple[str, str]:
    """Instagram 자격증명 읽기 (read IG credentials from env). Threads 쌍과 별개."""
    return (
        os.environ.get("IG_ACCESS_TOKEN", ""),
        os.environ.get("IG_USER_ID", ""),
    )


def _ig_setup_required_error() -> dict[str, Any]:
    """IG 자격증명 미설정 시 구조화 에러 (structured IG setup-required error).

    Instagram Professional(Business/Creator) 계정 전용 — Personal 계정은 Graph API 미지원.
    """
    return {
        "error": True,
        "setup_required": True,
        "message": (
            "Instagram 자격증명이 설정되지 않았습니다 "
            "(Instagram credentials not configured). "
            "IG_ACCESS_TOKEN(Facebook Page 액세스 토큰), IG_USER_ID(Instagram Professional "
            "계정 ID) 환경변수를 설정하세요. Instagram Professional(Business 또는 Creator) "
            "계정만 지원됩니다 — Personal 계정은 Graph API 로 발행할 수 없습니다. "
            "발급 절차는 mcp-servers/threads-poster/CONNECTORS.md 참조."
        ),
    }


def _get_ig_client() -> Optional[InstagramClient]:
    """IG 싱글톤 클라이언트 반환 (lazy). 자격증명 미설정 시 ``None``."""
    global _ig_client_singleton
    if _ig_client_singleton is not None:
        return _ig_client_singleton
    access_token, ig_user_id = _load_ig_credentials()
    if not access_token or not ig_user_id:
        return None
    _ig_client_singleton = InstagramClient(
        access_token=access_token, ig_user_id=ig_user_id
    )
    return _ig_client_singleton


def _reset_ig_client_for_tests() -> None:
    """테스트 전용: IG 싱글톤 캐시 초기화 (tests only: reset IG singleton cache)."""
    global _ig_client_singleton
    if _ig_client_singleton is not None:
        _ig_client_singleton.close()
    _ig_client_singleton = None


def _server_client_resolver(platform: str, post: dict[str, Any]) -> Optional[Any]:
    """server.py 큐 도구용 platform별 클라이언트 리졸버 (per-platform client resolver).

    runner._process 에 주입된다. threads row → ``_get_client()``, instagram row →
    ``_get_ig_client()``. lazy 싱글톤이므로 threads-only 큐는 IG 클라이언트를, ig-only 큐는
    Threads 클라이언트를 절대 빌드하지 않는다 (D1.a). 자격증명 미설정 플랫폼의 row 는
    ``None`` 을 반환 → _process 가 setup_required 스킵으로 처리한다.
    """
    if platform == "threads":
        return _get_client()
    if platform == "instagram":
        return _get_ig_client()
    return None


# --- M2: 큐 싱글톤 (queue singleton, lazy, env-driven DB path) -----------------
_queue_singleton: Optional[Queue] = None


def _get_queue() -> Queue:
    """큐 싱글톤 반환 (lazy). DB 경로는 환경변수에서 해석한다 (creds 불필요)."""
    global _queue_singleton
    if _queue_singleton is not None:
        return _queue_singleton
    _queue_singleton = Queue(_default_db_path())
    return _queue_singleton


def _reset_queue_for_tests() -> None:
    """테스트 전용: 큐 싱글톤 캐시 초기화 (tests only: reset queue singleton)."""
    global _queue_singleton
    if _queue_singleton is not None:
        _queue_singleton.close()
    _queue_singleton = None


def _publish_delay_seconds() -> float:
    """``THREADS_PUBLISH_DELAY`` 환경변수 읽기 (기본 30초, 테스트는 0)."""
    raw = os.environ.get("THREADS_PUBLISH_DELAY")
    if raw is None:
        return DEFAULT_PUBLISH_DELAY
    try:
        return float(raw)
    except ValueError:
        return DEFAULT_PUBLISH_DELAY


def _wait_publish_delay() -> None:
    delay = _publish_delay_seconds()
    if delay > 0:
        time.sleep(delay)


def _error_dict(exc: Exception) -> dict[str, Any]:
    return {"error": True, "message": str(exc)}


def _publish_result(media_id: str, container_id: str) -> dict[str, Any]:
    return {
        "media_id": media_id,
        "container_id": container_id,
        "permalink_hint": f"https://www.threads.net/@<username>/post/{media_id}",
        "note": "permalink 은 username 확인 후 조합. threads_get_profile 로 username 조회 가능.",
    }


# --- 분산 발행: 스케줄 계산 (distributed-publishing schedule helpers) --------------
def _now_seoul() -> datetime:
    """현재 시각을 Asia/Seoul aware datetime 으로 반환 (clock seam — 테스트가 monkeypatch)."""
    return datetime.now(SEOUL_TZ)


def _compute_batch_schedule(
    n: int,
    cadence: str,
    start_date: Optional[str],
    now: datetime,
) -> list[Optional[str]]:
    """분산 발행 예약 시각 계산 (pure schedule calculator — no I/O, no datetime.now()).

    ``n`` 개 포스트를 ``cadence`` 프리셋에 따라 Asia/Seoul 12:00 슬롯에 분산한다.
    ``now`` 는 주입된 clock(aware datetime 권장) 이며, 함수 본문은 절대 ``datetime.now()``
    를 호출하지 않는다 — 테스트는 고정 ``now`` 로 결정적 결과를 얻는다.

    Args:
        n: 예약할 슬롯 수.
        cadence: ``weekly_3`` | ``weekly_5`` | ``manual``.
        start_date: 첫 후보 날짜(ISO ``YYYY-MM-DD``). ``None`` 이면 ``now`` 의 날짜.
        now: 기준 시각(aware datetime). 각 슬롯은 이 시각 이후여야 한다.

    Returns:
        ISO-8601 datetime 문자열 리스트(길이 ``n``). ``manual`` 케이던스는 전부 ``None``.

    Raises:
        ValueError: 지원하지 않는 ``cadence``.
    """
    if n <= 0:
        return []
    if cadence == "manual":
        return [None] * n
    if cadence == "weekly_3":
        target_weekdays = _WEEKLY_3_DAYS
    elif cadence == "weekly_5":
        target_weekdays = _WEEKLY_5_DAYS
    else:
        raise ValueError(
            f"지원하지 않는 cadence 입니다 (unsupported cadence): {cadence!r}. "
            f"허용값 (allowed): weekly_3, weekly_5, manual"
        )

    # now 를 Seoul 로 정규화 — naive 면 Seoul 인 것으로 간주.
    now_seoul = now.astimezone(SEOUL_TZ) if now.tzinfo is not None else now.replace(
        tzinfo=SEOUL_TZ
    )
    start = date.fromisoformat(start_date) if start_date else now_seoul.date()

    out: list[Optional[str]] = []
    cursor = start
    # 안전 상한: 2년치 평일을 넘게 탐색하지 않는다 (무한루프 방지).
    for _day in range(366 * 2):
        if len(out) == n:
            break
        if cursor.weekday() in target_weekdays:
            slot = datetime(
                cursor.year, cursor.month, cursor.day,
                _BATCH_SLOT_HOUR, 0, 0, tzinfo=SEOUL_TZ,
            )
            # 오늘이 대상 요일이라도 정오가 지났으면(슬롯 <= now) 건너뛴다.
            # 과거 대상 요일들도 자동으로 스킵된다(slot < now).
            if slot > now_seoul:
                out.append(slot.isoformat())
        cursor += timedelta(days=1)
    return out


# ------------------------------------------------------------------ tools
@mcp.tool()
def threads_publish_text(text: str) -> dict[str, Any]:
    r"""Threads 에 텍스트 게시 (publish a text post).

    텍스트 전용 스레드를 만들어 발행한다 (create TEXT container → wait → publish).
    ``text`` 는 500 UTF-8 바이트 제한 — 이모지·한글은 바이트 단위로 계산.

    Args:
        text: 게시할 텍스트 본문 (500 UTF-8 바이트 이하).

    Returns:
        ``media_id``, ``container_id``, ``permalink`` 힌트를 포함한 dict.
        자격증명 미설정 시 ``setup_required`` 에러 dict 를 반환한다 (서버 크래시 없음).
    """
    client = _get_client()
    if client is None:
        return _setup_required_error()
    try:
        container_id = client.create_container("TEXT", text=text)
        _wait_publish_delay()
        media_id = client.publish(container_id)
        return _publish_result(media_id, container_id)
    except (ValueError, ThreadsAPIError) as exc:
        return _error_dict(exc)


@mcp.tool()
def threads_publish_image(text: str, image_url: str) -> dict[str, Any]:
    r"""Threads 에 이미지 게시 (publish an image post).

    이미지(JPEG/PNG, ≤8MB, 공개 URL) 컨테이너를 만들어 발행한다.
    ``text`` 는 캡션(선택) — 500 UTF-8 바이트 제한.

    Args:
        text: 캡션 본문 (빈 문자열 허용 — 캡션 없는 이미지 발행).
        image_url: 공개 접근 가능한 이미지 URL.

    Returns:
        ``media_id``, ``container_id``, ``permalink`` 힌트 dict.
        자격증명 미설정 시 ``setup_required`` 에러.
    """
    client = _get_client()
    if client is None:
        return _setup_required_error()
    try:
        kwargs: dict[str, Any] = {"image_url": image_url}
        if text:
            kwargs["text"] = text
        container_id = client.create_container("IMAGE", **kwargs)
        _wait_publish_delay()
        media_id = client.publish(container_id)
        return _publish_result(media_id, container_id)
    except (ValueError, ThreadsAPIError) as exc:
        return _error_dict(exc)


@mcp.tool()
def threads_publish_video(text: str, video_url: str) -> dict[str, Any]:
    r"""Threads 에 비디오 게시 (publish a video post).

    비디오(MOV/MP4, ≤1GB, ≤5분, 공개 URL) 컨테이너를 만들어 발행한다.
    ``text`` 는 캡션(선택) — 500 UTF-8 바이트 제한.

    Args:
        text: 캡션 본문 (빈 문자열 허용).
        video_url: 공개 접근 가능한 비디오 URL.

    Returns:
        ``media_id``, ``container_id``, ``permalink`` 힌트 dict.
        자격증명 미설정 시 ``setup_required`` 에러.
    """
    client = _get_client()
    if client is None:
        return _setup_required_error()
    try:
        kwargs: dict[str, Any] = {"video_url": video_url}
        if text:
            kwargs["text"] = text
        container_id = client.create_container("VIDEO", **kwargs)
        _wait_publish_delay()
        media_id = client.publish(container_id)
        return _publish_result(media_id, container_id)
    except (ValueError, ThreadsAPIError) as exc:
        return _error_dict(exc)


@mcp.tool()
def threads_get_profile() -> dict[str, Any]:
    r"""Threads 프로필 조회 (health check / who-am-I).

    ``username``, ``id``, ``followers_count``, ``profile_picture_url`` 를 반환한다.
    자격증명이 유효한지 확인하는 용도로 가장 먼저 호출해 볼 것.

    Returns:
        프로필 dict. 자격증명 미설정 시 ``setup_required`` 에러.
    """
    client = _get_client()
    if client is None:
        return _setup_required_error()
    try:
        return client.get_profile()
    except ThreadsAPIError as exc:
        return _error_dict(exc)


@mcp.tool()
def threads_refresh_token() -> dict[str, Any]:
    r"""장기 액세스 토큰 수동 갱신 (manually refresh long-lived token).

    장기 토큰(60일) 을 갱신해 새 ``access_token`` 을 받는다.
    단기 토큰(1h) 은 본 도구로 갱신할 수 없다 — 먼저 장기 토큰으로 교환 필요
    (CONNECTORS.md 참조).

    Returns:
        새 ``access_token`` 을 담은 dict. 자격증명 미설정 시 ``setup_required`` 에러.
    """
    client = _get_client()
    if client is None:
        return _setup_required_error()
    try:
        new_token = client.refresh_token()
        return {"access_token": new_token, "refreshed": True}
    except ThreadsAPIError as exc:
        return _error_dict(exc)


# ------------------------------------------------------------------ M2: 큐 관리 도구 (queue-management tools)
# 세션 안에서 전체 플로우(enqueue → approve → publish) 를 구동할 수 있도록 큐 조작
# 도구를 둔다. 순수 큐 조작(add/add_batch/approve/list/get) 은 자격증명 없이도
# 동작하며(로컬 SQLite), publish_due 만 자격증명이 필요하다.


@mcp.tool()
def threads_queue_add(
    media_type: str,
    text: Optional[str] = None,
    image_url: Optional[str] = None,
    video_url: Optional[str] = None,
    scheduled_at: Optional[str] = None,
) -> dict[str, Any]:
    r"""발행 큐에 포스트 추가 (enqueue a post as PENDING).

    ``media_type`` ∈ ``TEXT`` | ``IMAGE`` | ``VIDEO``. 즉시 발행 예정으로
    넣려면 ``scheduled_at`` 에 ISO-8601 시각을 전달한다 (미지정 시 NULL = due 즉시).

    Returns:
        ``post_id`` / ``status`` / ``media_type`` / ``scheduled_at`` dict.
        미지원 ``media_type`` 은 ``error`` dict.
    """
    try:
        q = _get_queue()
        post_id = q.enqueue(
            media_type,
            text=text or None,
            image_url=image_url or None,
            video_url=video_url or None,
            scheduled_at=scheduled_at or None,
        )
        post = q.get(post_id)
        return {
            "post_id": post_id,
            "status": post["status"],
            "media_type": post["media_type"],
            "scheduled_at": post["scheduled_at"],
        }
    except ValueError as exc:
        return _error_dict(exc)


@mcp.tool()
def threads_queue_add_batch(
    posts: list[dict[str, Any]],
    cadence: str = "weekly_3",
    start_date: Optional[str] = None,
    approve: bool = False,
) -> dict[str, Any]:
    r"""초안 여러 개를 베스트 슬롯에 분산 등록 (batch-enqueue drafts across best slots).

    승인된(또는 승인 대기) 초안 N 개를 받아 ``cadence`` 프리셋에 따라 Asia/Seoul
    12:00 슬롯에 자동 분산 예약한다. 한 주 치 포스트를 한 번에 예약할 때 쓴다.

    Args:
        posts: ``{media_type, text?, image_url?, video_url?}`` 초안 dict 리스트 (≥1).
            ``media_type`` 기본값 ``TEXT``.
        cadence: 분산 프리셋 — ``weekly_3`` (화/수/목, 기본) · ``weekly_5`` (월-금)
            · ``manual`` (scheduled_at 미지정, 호출자가 나중에 설정).
        start_date: 첫 후보 날짜(ISO ``YYYY-MM-DD``). 기본 오늘(Seoul).
        approve: ``True`` 면 계산된 예약으로 바로 ``APPROVED`` 로 등록
            (이 호출 안에서 이미 초안을 검토했을 때). 기본 ``False`` = ``PENDING``.

    Returns:
        ``count`` · ``post_ids`` · ``schedules`` ({post_id, scheduled_at} 리스트)
        · ``cadence`` dict. 입력 검증 실패 시 ``error`` dict.
    """
    # --- 입력 검증 (enqueue 전에 전체 선검증 — 부분 실패 방지) ---
    if not isinstance(posts, list) or len(posts) == 0:
        return {
            "error": True,
            "message": (
                "posts 는 최소 1개 이상의 초안 dict 리스트여야 합니다 "
                "(posts must be a non-empty list of draft dicts)."
            ),
        }
    if cadence not in _VALID_BATCH_CADENCES:
        return {
            "error": True,
            "message": (
                f"지원하지 않는 cadence 입니다 (unsupported cadence): {cadence!r}. "
                f"허용값 (allowed): weekly_3, weekly_5, manual"
            ),
        }
    normalized: list[tuple[str, Optional[str], Optional[str], Optional[str]]] = []
    for idx, p in enumerate(posts):
        if not isinstance(p, dict):
            return {
                "error": True,
                "message": f"posts[{idx}] 가 dict 가 아닙니다 (not a dict): {type(p).__name__}",
            }
        media_type = p.get("media_type", "TEXT")
        if media_type not in _VALID_BATCH_MEDIA_TYPES:
            return {
                "error": True,
                "message": (
                    f"posts[{idx}] 의 media_type 이 지원하지 않는 값입니다 "
                    f"(unsupported media_type): {media_type!r}. "
                    f"허용값 (allowed): TEXT, IMAGE, VIDEO"
                ),
            }
        normalized.append(
            (
                media_type,
                p.get("text") or None,
                p.get("image_url") or None,
                p.get("video_url") or None,
            )
        )

    # --- 예약 시각 계산 (pure helper, 주입 clock) ---
    try:
        schedules_iso = _compute_batch_schedule(
            len(normalized), cadence, start_date, _now_seoul()
        )
    except ValueError as exc:
        return _error_dict(exc)

    # --- 일괄 enqueue (검증 통과했으므로 여기서 ValueError 발생 안 함) ---
    q = _get_queue()
    status = "APPROVED" if approve else "PENDING"
    post_ids: list[int] = []
    schedules: list[dict[str, Any]] = []
    for (media_type, text, image_url, video_url), sched in zip(
        normalized, schedules_iso, strict=True
    ):
        pid = q.enqueue(
            media_type,
            text=text,
            image_url=image_url,
            video_url=video_url,
            scheduled_at=sched,
            status=status,
        )
        post_ids.append(pid)
        schedules.append({"post_id": pid, "scheduled_at": sched})

    return {
        "count": len(post_ids),
        "post_ids": post_ids,
        "schedules": schedules,
        "cadence": cadence,
    }


@mcp.tool()
def threads_queue_approve(
    post_id: int, scheduled_at: Optional[str] = None
) -> dict[str, Any]:
    r"""PENDING 포스트를 APPROVED 로 승인 (approve a queued post).

    ``scheduled_at`` 미지정 시 현재 시각으로 예약(즉시 due). 이미 예약된 시각을
    덮어쓰려면 명시적으로 전달.

    Returns:
        갱신된 ``status`` / ``approved_at`` / ``scheduled_at`` dict.
        해당 post 가 없으면 ``error`` dict.
    """
    q = _get_queue()
    ok = q.approve(post_id, scheduled_at=scheduled_at or None)
    if not ok:
        return {
            "error": True,
            "not_found": True,
            "message": f"post id={post_id} 를 찾을 수 없습니다 (not found)",
        }
    post = q.get(post_id)
    return {
        "post_id": post_id,
        "status": post["status"],
        "approved_at": post["approved_at"],
        "scheduled_at": post["scheduled_at"],
    }


@mcp.tool()
def threads_queue_list(
    status: Optional[str] = None, limit: int = 50
) -> dict[str, Any]:
    r"""큐 포스트 목록 조회 (list queued posts, newest first).

    Args:
        status: 필터(PENDING|APPROVED|PUBLISHED|FAILED). 미지정 시 전체.
        limit: 최대 행 수(기본 50).

    Returns:
        ``count`` 와 ``posts`` 리스트를 담은 dict.
    """
    q = _get_queue()
    posts = q.list(status=status, limit=limit)
    return {"count": len(posts), "posts": posts}


@mcp.tool()
def threads_queue_get(post_id: int) -> dict[str, Any]:
    r"""단일 큐 포스트 상세 조회 (fetch one queued post).

    Returns:
        포스트 row dict. 해당 post 가 없으면 ``not_found`` 에러 dict.
    """
    q = _get_queue()
    post = q.get(post_id)
    if post is None:
        return {
            "error": True,
            "not_found": True,
            "message": f"post id={post_id} 를 찾을 수 없습니다 (not found)",
        }
    return post


@mcp.tool()
def threads_queue_publish_due(limit: int = 10) -> dict[str, Any]:
    r"""due 큐(Threads)를 수동 처리 (process due Threads rows now, session-driven publishing).

    세션 안에서 분산 예약된 **Threads** 포스트들을 실제로 발행하기 위한 도구. 백그라운드 자동
    발행은 없으므로(수동 승인 모델, REQ-INST-022), 예약 시각이 도래한 포스트는 이 도구로 직접
    flush 한다. 내부적으로 runner._process 를 재사용한다(platform="threads" 필터 — Instagram row
    는 건드리지 않는다, D8(a)). 자격증명 필요(미설정 시 ``setup_required`` 에러).

    Returns:
        ``published`` / ``failed`` / ``skipped`` 카운트와 ``messages`` 리스트 dict.
    """
    # Threads 자격증명 게이트 — 기존 동작 byte-identical 보존 (REQ-INST-023).
    if _get_client() is None:
        return _setup_required_error()
    q = _get_queue()
    return run_queue_once(
        q,
        client_resolver=_server_client_resolver,
        platform="threads",
        limit=limit,
        dry_run=False,
        once=None,
        delay=_publish_delay_seconds(),
    )


# ------------------------------------------------------------------ 문체 프로필 (style profile — 로컬 파일 I/O, Threads 자격증명 불필요)
# threads-style-learn 스킬이 분석한 문체 프로필을 안정적인 경로에 저장하고,
# threads-post-draft 스킬이 초안 작성 시 불러와 적용한다. Threads API 자격증명과
# 무관한 순수 로컬 파일 도구다 — setup_required 게이트를 거치지 않는다.

_STYLE_PROFILE_FILENAME = "style-profile.md"


def _default_style_path() -> str:
    r"""스타일 프로필 기본 경로 해석 (resolve default style-profile path from env).

    우선순위 (precedence) — ``runner._default_db_path`` 와 동일한 패턴/동일 ``.data/`` 디렉토리:
      1. ``$CLAUDE_PLUGIN_ROOT/mcp-servers/threads-poster/.data/style-profile.md``
      2. 패키지 기준 상대 경로 폴백 (``../../.data/style-profile.md``)
    """
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if root:
        return os.path.join(
            root, "mcp-servers", "threads-poster", ".data", _STYLE_PROFILE_FILENAME
        )
    here = os.path.dirname(__file__)
    return os.path.abspath(
        os.path.join(here, "..", "..", ".data", _STYLE_PROFILE_FILENAME)
    )


@mcp.tool()
def threads_style_save(
    profile_markdown: str, path: Optional[str] = None
) -> dict[str, Any]:
    r"""문체 프로필을 디스크에 저장 (save the style profile markdown to disk).

    ``threads-style-learn`` 스킬이 분석한 문체 프로필을 안정적인 경로에 쓴다. 기본 경로는
    ``$CLAUDE_PLUGIN_ROOT/mcp-servers/threads-poster/.data/style-profile.md`` 이며
    ``.data/`` 디렉토리가 없으면 생성한다. Threads 자격증명은 필요 없다 — 로컬 파일 쓰기 전용.

    Args:
        profile_markdown: 저장할 프로필 마크다운 본문.
        path: 저장할 파일 경로(명시적 지정 시). 미지정 시 기본 경로 사용.

    Returns:
        ``{path, saved: True, chars: N}`` dict. 입력 타입 오류 / I/O 실패 시 ``error`` dict.
    """
    if not isinstance(profile_markdown, str):
        return {
            "error": True,
            "message": (
                f"profile_markdown 는 str 이어야 합니다 (must be str): "
                f"{type(profile_markdown).__name__}"
            ),
        }
    target = path or _default_style_path()
    try:
        parent = os.path.dirname(target)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(profile_markdown)
    except OSError as exc:
        return {"error": True, "message": f"스타일 프로필 저장 실패 (write failed): {exc}"}
    return {"path": target, "saved": True, "chars": len(profile_markdown)}


@mcp.tool()
def threads_style_load(path: Optional[str] = None) -> dict[str, Any]:
    r"""저장된 문체 프로필을 읽는다 (load the style profile markdown).

    ``threads-post-draft`` 스킬이 초안 작성 전 이 도구로 프로필 존재 여부를 확인하고,
    있으면 그 문체 차원을 초안에 반영한다. Threads 자격증명 불필요 — 로컬 파일 읽기 전용.

    Args:
        path: 읽을 파일 경로(명시적 지정 시). 미지정 시 기본 경로.

    Returns:
        ``{path, exists: bool, profile: <markdown or None>}`` dict.
        파일이 없으면 ``exists: False, profile: None`` (에러가 아님).
        I/O 에러 시 ``error`` dict.
    """
    target = path or _default_style_path()
    if not os.path.exists(target):
        return {"path": target, "exists": False, "profile": None}
    try:
        with open(target, "r", encoding="utf-8") as fh:
            content = fh.read()
    except OSError as exc:
        return {"error": True, "message": f"스타일 프로필 읽기 실패 (read failed): {exc}"}
    return {"path": target, "exists": True, "profile": content}


# ------------------------------------------------------------------ 멀티 채널 포맷 (multi-channel formatter — 발행 안 함, 포맷만)
# Threads(직접 발행) / Facebook(복붙 전용) / X(free=스레드 분할 · premium=단일) 용으로
# 텍스트를 변형한다. Facebook 개인 계정은 API 발행이 정책상 불가하므로 본 도구는
# Facebook/X 로 발행하지 않고 *복붙용* 텍스트만 만든다. Threads 결과는 queue 도구로 넘긴다.
#
# 길이 제한 참고 (2026 baseline):
#   - Threads  : 500 UTF-8 바이트
#   - X free   : 트윗당 280자  → 초과 시 1/ · 2/ 번호 트윗 체인으로 분할
#   - X premium: 25,000자      → 단일 문자열 그대로
#   - Facebook : 개인 계정 글자 수 제한 없음 (단, API 발행 불가 → 복붙)

_VALID_X_TIERS = ("free", "premium")
_DEFAULT_CHANNELS = ("threads", "facebook", "x")
_KNOWN_CHANNELS = ("threads", "facebook", "x")
# X Premium 단일 트윗 글자 수 상한 (2026 baseline).
_X_PREMIUM_MAX_CHARS = 25000


def _utf8_bytes(s: str) -> int:
    """UTF-8 인코딩 바이트 수 (UTF-8 byte length)."""
    return len(s.encode("utf-8"))


def _truncate_utf8(text: str, max_bytes: int) -> str:
    r"""UTF-8 문자 경계에서 ``max_bytes`` 이하로 자른다 (byte-boundary-safe truncation).

    바이트 단위로 자른 뒤 ``errors="ignore"`` 로 디코딩해 잘린 멀티바이트 문자의
    잔여 바이트를 버린다 — 깨진 문자(�) 가 생기지 않는다.
    """
    encoded = text.encode("utf-8")[:max_bytes]
    return encoded.decode("utf-8", errors="ignore")


def _fit_bytes(text: str, max_bytes: int, ellipsis: str = "…") -> tuple[str, int]:
    r"""``text`` 를 ``max_bytes`` 이하의 UTF-8 로 다듬는다 (word-boundary truncation + ellipsis).

    예산 내면 그대로 반환. 초과 시 (ellipsis 바이트를 뺀 예산 안에서) 최대한 채우되
    마지막 공백(단어 경계) 에서 끊고 ellipsis 를 붙인다 — 단어 중간을 자르지 않는다.
    공백을 찾지 못하면 UTF-8 문자 경계에서 하드 자른다.

    의미 보존 *요약* 은 LLM 작업이라 이 도구는 하지 않는다 — 본 함수는 기계적 안전망이다.
    진짜 요약이 필요하면 호출 *전* 에 LLM 이 본문을 줄여야 한다.

    Returns:
        (다듬은 텍스트, 실제 UTF-8 바이트 수).
    """
    nbytes = _utf8_bytes(text)
    if nbytes <= max_bytes:
        return text, nbytes
    ellipsis_bytes = _utf8_bytes(ellipsis)
    target = max_bytes - ellipsis_bytes
    if target <= 0:
        # max_bytes 자체가 ellipsis 보다 작다 — ellipsis 없이 문자 경계 하드 자름.
        cut = _truncate_utf8(text, max_bytes)
        return cut, _utf8_bytes(cut)
    truncated = _truncate_utf8(text, target)
    last_space = truncated.rfind(" ")
    if last_space > 0:
        truncated = truncated[:last_space].rstrip()
    out = truncated + ellipsis
    return out, _utf8_bytes(out)


def _adapt_for_threads(text: str) -> tuple[str, int]:
    r"""Threads 용 텍스트 변형 — 500 UTF-8 바이트 이하 (byte-budget enforcement)."""
    return _fit_bytes(text, 500)


def _adapt_for_facebook(text: str) -> str:
    r"""Facebook 용 텍스트 변형 — 개인 계정은 글자 수 제한 없음, 대화체·이모지 유지.

    가벼운 정규화(앞뒤 공백 제거, 3줄 이상 빈 줄 → 2줄) 만 한다. 톤 조정(더 대화적으로)
    은 LLM 영역이라 여기서 하지 않는다. Facebook 은 *복붙용* 이다 (API 발행 불가).
    """
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _adapt_for_x_premium(text: str) -> tuple[str, bool]:
    r"""X Premium 용 — 단일 문자열(≤25000자). 초과 시 잘라내고 truncate 플래그.

    Returns:
        (텍스트, 잘라냈는지 여부).
    """
    if len(text) <= _X_PREMIUM_MAX_CHARS:
        return text, False
    return text[:_X_PREMIUM_MAX_CHARS], True


def _take_prefix(token: str, budget: int, counter: Callable[[str], int]) -> str:
    r"""``token`` 에서 ``counter(접두) <= budget`` 인 최장 접두 반환 (longest fitting prefix).

    단일 문자조차 ``budget`` 을 초과하면 빈 문자열을 반환한다 (호출자가 한 글자 강제 처리).
    """
    best = ""
    for ch in token:
        cand = best + ch
        if counter(cand) > budget:
            break
        best = cand
    return best


def _hard_split_token(
    token: str, budget: int, counter: Callable[[str], int]
) -> list[str]:
    r"""단일 토큰이 ``budget`` 을 초과할 때 조각으로 자른다 (hard-split an oversized token).

    각 조각의 ``counter`` 값은 ``budget`` 이하다. 단일 문자가 ``budget`` 을 초과하는
    극단적 케이스는 한 글자씩 강제 분할한다 (진행 보장 — 무한루프 방지).
    """
    pieces: list[str] = []
    remaining = token
    while remaining:
        piece = _take_prefix(remaining, budget, counter)
        if not piece:
            piece = remaining[0]
        pieces.append(piece)
        remaining = remaining[len(piece):]
    return pieces


def _split_for_x_thread(
    text: str,
    limit: int = 280,
    *,
    counter: Callable[[str], int] = len,
) -> list[str]:
    r"""X(트위터) 무료 tier 스레드 분할 — 각 트윗 ≤ ``limit``, 단어 경계에서 자른다 (numbered, boundary-aware).

    X 무료 tier 는 트윗당 280자 제한이다. 긴 텍스트를 ``1/ `` · ``2/ `` … 번호가 붙은
    트윗 체인으로 나눈다. 접두 번호(``N/ ``)도 ``limit`` 에 포함해 계산하므로, 각 트윗의
    *전체* 길이(접두 + 내용)가 ``limit`` 을 넘지 않는다.

    분할 원칙 (split rules):
      - 공백 단위로 단어를 쪼갠다 (``text.split()``) — 단어 중간은 자르지 않는다.
      - 단일 단어가 (접두를 뺀) 내용 예산보다 긴 극단적 케이스만 어쩔 수 없이 글자 단위로
        강제 분할한다 (``_hard_split_token``). 일반적인 텍스트에서는 발생하지 않는다.
      - 접두 번호 길이는 자릿수에 따라 자라난다(9→10, 99→100) — 각 청크마다 *현재* idx
        기준으로 예산을 다시 계산해 정확도를 보장한다.

    Args:
        text: 분할할 원본 텍스트.
        limit: 트윗당 최대 길이. 기본 280 (X 무료 tier). 접두 포함.
        counter: 길이 측정 callable (기본 ``len`` = 문자 수). 테스트가 바이트 기반 카운터를
            주입해 알고리즘이 존중하는지 검증할 수 있다.

    Returns:
        번호가 붙은 트윗 문자열 리스트. 빈 입력 → 빈 리스트.

    Raises:
        TypeError: ``text`` 가 str 이 아닐 때.
        ValueError: ``limit`` 가 번호 접두를 담기에 너무 작을 때 (``< 4`` 또는 접두 초과).
    """
    if not isinstance(text, str):
        raise TypeError(
            f"text 는 str 이어야 합니다 (text must be str): {type(text).__name__}"
        )
    if limit < 4:
        raise ValueError(
            f"limit 가 너무 작습니다 (limit too small): {limit}. 최소 4 (\"1/ \" + 1 char)."
        )
    if not text.strip():
        return []

    words = text.split()
    chunks: list[str] = []
    idx = 1
    current: list[str] = []
    current_len = 0
    i = 0
    while i < len(words):
        prefix = f"{idx}/ "
        budget = limit - counter(prefix)
        if budget <= 0:
            raise ValueError(
                f"limit {limit} 이 번호 접두를 담기에 너무 작습니다 "
                f"(limit too small for prefix at idx={idx})."
            )
        w = words[i]
        if current:
            sep = counter(" ")
            if current_len + sep + counter(w) <= budget:
                current.append(w)
                current_len += sep + counter(w)
                i += 1
            else:
                # 현재 청크에 더 못 넣음 → 닫고 새 청크 시작 (w 재처리).
                chunks.append(prefix + " ".join(current))
                idx += 1
                current = []
                current_len = 0
        else:
            wl = counter(w)
            if wl <= budget:
                current = [w]
                current_len = wl
                i += 1
            else:
                # 단일 단어가 예산 초과 — 글자 단위 강제 분할, 각 조각을 자체 청크로.
                for piece in _hard_split_token(w, budget, counter):
                    chunks.append(prefix + piece)
                    idx += 1
                    prefix = f"{idx}/ "
                    budget = limit - counter(prefix)
                current = []
                current_len = 0
                i += 1
    if current:
        prefix = f"{idx}/ "
        chunks.append(prefix + " ".join(current))
    return chunks


@mcp.tool()
def threads_format_multi_channel(
    text: str,
    x_tier: str = "free",
    channels: Optional[list[str]] = None,
) -> dict[str, Any]:
    r"""텍스트를 Threads / Facebook / X 용으로 각각 포맷한다 (multi-channel formatter).

    **발행은 하지 않는다 — 포맷만 한다.**

      - **Threads**: 500 UTF-8 바이트 이하로 다듬어 ``threads_queue_add`` /
        ``threads_queue_add_batch`` 에 넘길 수 있는 형태로 반환 (바이트 수 포함).
      - **Facebook**: 개인 계정은 API 발행이 정책상 불가하므로 *복붙용* 텍스트를 반환한다
        (본 도구는 Facebook 으로 발행하지 않는다). 가벼운 정규화만 적용.
      - **X**: ``x_tier`` 에 따라 —
          - ``"free"``: 트윗당 280자 — 긴 텍스트를 ``1/ `` · ``2/ `` 번호 트윗 체인으로 분할.
          - ``"premium"``: 단일 문자열(≤25000자) 그대로 반환 (초과 시 잘라내고 플래그).

    Args:
        text: 원본 텍스트 (각 채널에 맞춰 변형된다).
        x_tier: ``"free"`` (기본) 또는 ``"premium"``. 그 외 값은 ``error`` dict.
        channels: 포맷할 채널 리스트(기본 ``["threads","facebook","x"]``).
            알 수 없는 채널 이름은 무시된다.

    Returns:
        채널별 포맷 결과 dict:
          - ``threads``: ``{"text", "bytes", "max_bytes"}`` — queue 도구용.
          - ``facebook``: 복붙용 텍스트 *문자열*.
          - ``x``: ``free`` → 번호 트윗 *리스트* · ``premium`` → 단일 *문자열*.
          - 최상위: ``channels`` · ``x_tier`` · ``note`` (복붙 안내).
        잘못된 ``x_tier`` / ``text`` 타입은 ``error`` dict.
    """
    if not isinstance(text, str):
        return {
            "error": True,
            "message": (
                f"text 는 str 이어야 합니다 (text must be str): {type(text).__name__}"
            ),
        }
    if x_tier not in _VALID_X_TIERS:
        return {
            "error": True,
            "message": (
                f"지원하지 않는 x_tier 입니다 (unsupported x_tier): {x_tier!r}. "
                f"허용값 (allowed): free, premium"
            ),
        }
    wanted = list(channels) if channels is not None else list(_DEFAULT_CHANNELS)
    selected = [c for c in wanted if c in _KNOWN_CHANNELS]

    out: dict[str, Any] = {
        "channels": selected,
        "x_tier": x_tier,
        "note": (
            "Threads 출력은 threads_queue_add / threads_queue_add_batch 로 큐에 넘기세요. "
            "Facebook·X 출력은 *복붙용* 입니다 — 본 도구는 Facebook/X 로 발행하지 않습니다."
        ),
    }
    if "threads" in selected:
        adapted, nbytes = _adapt_for_threads(text)
        out["threads"] = {"text": adapted, "bytes": nbytes, "max_bytes": 500}
    if "facebook" in selected:
        out["facebook"] = _adapt_for_facebook(text)
    if "x" in selected:
        if x_tier == "free":
            out["x"] = _split_for_x_thread(text, limit=280)
        else:
            adapted, truncated = _adapt_for_x_premium(text)
            out["x"] = adapted
            if truncated:
                out["x_truncated"] = True
    return out


# ------------------------------------------------------------------ Instagram 도구 (SPEC-THREADS-POSTER-INSTAGRAM-001)
# Threads 도구와 *평행한* Instagram 발행/예약/조회 도구. Facebook Login for Business 호스트
# (graph.facebook.com), JPEG-only, REELS, VIDEO/REELS 컨테이너 폴링. 자격증명은 Threads 쌍과
# 독립적인 IG_ACCESS_TOKEN/IG_USER_ID. Instagram Professional(Business/Creator) 계정 전용.
#
# [스케줄링 교정 — REQ-INST-009] Instagram Graph API 는 서버 측 스케줄링 파라미터가 *없다*.
# 예약 = 큐에 intent(캡션+미디어 URL+예정 시각) 보관. 실제 발행은 예정 시각 도래 후 사용자가
# 세션에서 instagram_queue_publish_due 를 호출할 때 일어난다 (백그라운드 자동 발행 없음).
_VALID_IG_MEDIA_TYPES = ("IMAGE", "VIDEO", "REELS")


def _ig_publish_result(media_id: str, container_id: str) -> dict[str, Any]:
    return {
        "media_id": media_id,
        "container_id": container_id,
        # @MX:TODO: [AUTO] permalink 은 media_id 가 아닌 shortcode 조합이어야 할 수 있다 (runner D4).
        "permalink_hint": f"https://www.instagram.com/p/{media_id}/",
        "platform": "instagram",
    }


@mcp.tool()
def instagram_publish_image(text: str, image_url: str) -> dict[str, Any]:
    r"""Instagram 에 이미지 발행 (publish an image — JPEG-only, immediate 2-stage).

    JPEG 이미지(공개 URL) 컨테이너를 만들어 즉시 발행한다. PNG 는 거부된다(Threads 와 상이).
    ``text`` 는 캡션(선택). Instagram 은 서버 측 스케줄링을 지원하지 않는다 — 예약하려면
    ``instagram_schedule`` 로 큐에 intent 를 보관할 것.

    Returns:
        ``media_id``/``container_id``/``permalink_hint`` dict. 자격증명 미설정 시 ``setup_required``.
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        kwargs: dict[str, Any] = {"image_url": image_url}
        if text:
            kwargs["text"] = text
        container_id = client.create_container("IMAGE", **kwargs)
        media_id = client.publish(container_id)  # IMAGE 는 폴링 불필요
        return _ig_publish_result(media_id, container_id)
    except (ValueError, InstagramAPIError) as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_publish_video(text: str, video_url: str) -> dict[str, Any]:
    r"""Instagram 에 비디오 발행 (publish a video — 2-stage + container polling).

    비디오(공개 URL) 컨테이너 생성 후 ``FINISHED`` 될 때까지 폴링한 뒤 발행한다(REQ-INST-007).
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        kwargs: dict[str, Any] = {"video_url": video_url}
        if text:
            kwargs["text"] = text
        container_id = client.create_container("VIDEO", **kwargs)
        client.wait_until_finished(container_id)
        media_id = client.publish(container_id)
        return _ig_publish_result(media_id, container_id)
    except (ValueError, InstagramAPIError) as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_publish_reel(
    text: str, video_url: str, share_to_feed: bool = True
) -> dict[str, Any]:
    r"""Instagram 에 릴 발행 (publish a REEL — REELS container + polling).

    REELS 컨테이너(``media_type=REELS`` + ``video_url`` + ``share_to_feed``) 생성 후 폴링 · 발행.
    ``share_to_feed=True`` (기본) 면 피드에도 공유.
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        kwargs: dict[str, Any] = {"video_url": video_url, "share_to_feed": share_to_feed}
        if text:
            kwargs["text"] = text
        container_id = client.create_container("REELS", **kwargs)
        client.wait_until_finished(container_id)
        media_id = client.publish(container_id)
        return _ig_publish_result(media_id, container_id)
    except (ValueError, InstagramAPIError) as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_schedule(
    media_type: str,
    text: Optional[str] = None,
    image_url: Optional[str] = None,
    video_url: Optional[str] = None,
    scheduled_at: Optional[str] = None,
    share_to_feed: Optional[bool] = None,
) -> dict[str, Any]:
    r"""Instagram 예약 발행 큐 등록 (enqueue an Instagram post — queue-only, NO API call).

    **Instagram 은 서버 측 스케줄링을 지원하지 않는다 (REQ-INST-009).** 본 도구는 큐에
    intent(캡션 + 미디어 URL + 예정 시각)를 ``platform='instagram'`` 으로 보관만 한다 —
    API 는 일절 호출하지 않는다. 실제 발행은 예정 시각 도래 후 사용자가 세션에서
    ``instagram_queue_publish_due`` 를 호출할 때 일어난다 (백그라운드 자동 발행 없음).

    Args:
        media_type: ``IMAGE`` | ``VIDEO`` | ``REELS`` (TEXT 불가 — Instagram 은 텍스트 전용 게시가 없다).
        text: 캡션(선택).
        image_url: 공개 이미지 URL (IMAGE 필수, JPEG 권장).
        video_url: 공개 비디오 URL (VIDEO/REELS 필수).
        scheduled_at: 발행 예정 시각(ISO-8601). 미지정 시 NULL (즉시 due).
        share_to_feed: REELS 용. (현재 큐 스키마가 이 값을 보관하지 않는다 — 즉시 발행 도구인
            ``instagram_publish_reel`` 에서만 적용된다. 예약 릴의 피드 공유는 @MX:DEBT.)

    Returns:
        ``post_id``/``status``/``media_type``/``platform``/``scheduled_at`` dict.
        미지원 ``media_type``(TEXT 등) 은 ``error`` dict.
    """
    # @MX:DEBT: share_to_feed 가 큐에 보관되지 않는다 (posts 스키마에 해당 컬럼 없음).
    #   예약 REELS 의 피드 공유 의도가 보존되려면 posts 테이블에 share_to_feed 컬럼 추가가 필요하다.
    # @MX:CEILING: 현재 예약 REELS 은 publish-time 기본값(share_to_feed 없음) 으로 발행된다.
    # @MX:UPGRADE: posts 스키마에 share_to_feed 컬럼을 추가하고 _container_call 이 이를 반영할 때.
    if media_type not in _VALID_IG_MEDIA_TYPES:
        return {
            "error": True,
            "message": (
                f"Instagram 은 {media_type!r} 게시를 지원하지 않습니다 "
                f"(Instagram supports IMAGE/VIDEO/REELS only — TEXT 불가)."
            ),
        }
    try:
        q = _get_queue()
        post_id = q.enqueue(
            media_type,
            text=text or None,
            image_url=image_url or None,
            video_url=video_url or None,
            scheduled_at=scheduled_at or None,
            platform="instagram",
        )
        post = q.get(post_id)
        return {
            "post_id": post_id,
            "status": post["status"],
            "media_type": post["media_type"],
            "platform": post["platform"],
            "scheduled_at": post["scheduled_at"],
        }
    except ValueError as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_queue_publish_due(limit: int = 10) -> dict[str, Any]:
    r"""due Instagram 큐를 수동 처리 (process due Instagram rows — session-driven publishing).

    예약 시각이 도래한 **Instagram** 포스트들을 실제로 발행한다. 이 도구가 Instagram 의
    *유일한* 발행 트리거다 (서버 측 스케줄링도 백그라운드 자동 발행도 없다 — REQ-INST-009/022).

    IG 자격증명이 미설정이어도 크래시하지 않는다 — 각 due IG row 를 ``setup_required`` 스킵하고
    정상적으로 반환한다 (D1.a(b) skip-and-continue). 자격증명을 설정한 뒤 다시 호출하면 발행된다.

    Returns:
        ``published``/``failed``/``skipped`` 카운트와 ``messages`` 리스트 dict.
    """
    q = _get_queue()
    return run_queue_once(
        q,
        client_resolver=_server_client_resolver,
        platform="instagram",
        limit=limit,
        dry_run=False,
        once=None,
        delay=0.0,  # IG 는 컨테이너 폴링으로 대기 (threads 30s 지연 미적용)
    )


@mcp.tool()
def instagram_get_profile() -> dict[str, Any]:
    r"""Instagram 프로필 조회 (health check / who-am-I).

    ``username``/``id``/``followers_count``/``media_count`` 반환. IG 자격증명이 유효한지
    확인하는 용도로 가장 먼저 호출해 볼 것. 미설정 시 ``setup_required`` 에러.
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        return client.get_profile()
    except InstagramAPIError as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_refresh_token() -> dict[str, Any]:
    r"""Instagram 장기 Page 토큰 수동 갱신 (refresh long-lived Facebook Page token).

    Returns:
        새 ``access_token`` 을 담은 dict. 미설정 시 ``setup_required`` 에러.
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        new_token = client.refresh_token()
        return {"access_token": new_token, "refreshed": True}
    except InstagramAPIError as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_comments_list(media_id: str) -> dict[str, Any]:
    r"""Instagram 미디어의 댓글 목록 (list comments on a media object).

    ``manage_comments`` 권한 필요 (REQ-INST-018). 미설정 시 ``setup_required`` 에러.
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        return client.comments_list(media_id)
    except InstagramAPIError as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_comments_reply(comment_id: str, text: str) -> dict[str, Any]:
    r"""Instagram 댓글에 답글 작성 (reply to a comment).

    ``manage_comments`` 권한 필요 (REQ-INST-018).
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        return client.comments_reply(comment_id, text)
    except (ValueError, InstagramAPIError) as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_comments_hide(comment_id: str) -> dict[str, Any]:
    r"""Instagram 댓글 숨김 (hide a comment).

    ``manage_comments`` 권한 필요 (REQ-INST-018).
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        return client.comments_hide(comment_id)
    except InstagramAPIError as exc:
        return _error_dict(exc)


@mcp.tool()
def instagram_insights(
    metric: str = "reach,impressions",
    period: str = "day",
    media_id: Optional[str] = None,
) -> dict[str, Any]:
    r"""Instagram 인사이트 조회 (fetch account-level or media-level insights).

    ``manage_insights`` 권한 필요 (REQ-INST-019). ``media_id`` 미지정 시 계정 수준,
    지정 시 해당 미디어 수준 인사이트.
    """
    client = _get_ig_client()
    if client is None:
        return _ig_setup_required_error()
    try:
        return client.insights(metric=metric, period=period, media_id=media_id)
    except InstagramAPIError as exc:
        return _error_dict(exc)


# ------------------------------------------------------------------ entrypoint
def main() -> None:
    """stdio 트랜스포트로 MCP 서버 기동 (run the MCP server over stdio)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
