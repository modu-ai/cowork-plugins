"""threads-poster-runner — 발행 큐 실행 CLI (수동 킥 + server.py 재사용).

due() 큐를 순회하며 :class:`ThreadsClient` 2단계 발행(create_container → publish)
을 수행한다. 자격증명이 없으면 크래시 대신 설정 안내 메시지를 출력하고 exit 0 한다
(호출 스크립트가 실패로 간주해 불필요한 알림을 띄우지 않도록).

사용 (usage)::

    threads-poster-runner [--db PATH] [--limit N] [--dry-run] [--once POST_ID]

설계 (design):
  - 핵심 루프는 :func:`_process` 에 분리되어 있다 — server.py 의
    ``threads_queue_publish_due`` MCP 도구가 세션 안 수동/분산 발행을 위해 본
    로직을 재사용한다. 테스트는 가짜 Queue 와 가짜 ThreadsClient 을 주입해
    결정적으로 검증한다.
  - DB 경로 / publish delay / 자격증명은 모두 환경변수에서 읽는다.

참고: launchd/cron 기반 백그라운드 자동 발행은 제거되었다. 본 CLI 는 셸에서의
수동 1회 킥(``--once`` / ``--dry-run``) 용도로 남아있으며, 일상적 발행은 세션 안에서
``threads_queue_publish_due`` MCP 도구로 이루어진다.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Any, Optional

from .queue import Queue
from .threads_api import ThreadsClient

# Threads 권장: container 생성 후 평균 ~30초 대기 후 publish (server.py 와 동일값).
DEFAULT_PUBLISH_DELAY = 30.0
DEFAULT_LIMIT = 10
# Threads 24시간 발행 한도 (공식 문서 기준). runner 는 이 값을 초과하면 중단한다.
RATE_LIMIT_24H = 250


def _default_db_path() -> str:
    """환경변수 → DB 경로 해석 (resolve DB path from env).

    우선순위 (precedence):
      1. ``THREADS_POSTER_DB`` (명시적 경로)
      2. ``$CLAUDE_PLUGIN_ROOT/mcp-servers/threads-poster/.data/queue.db``
      3. 패키지 기준 상대 경로 폴백 (``../../.data/queue.db``)
    """
    explicit = os.environ.get("THREADS_POSTER_DB")
    if explicit:
        return explicit
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if root:
        return os.path.join(
            root, "mcp-servers", "threads-poster", ".data", "queue.db"
        )
    here = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(here, "..", "..", ".data", "queue.db"))


def _publish_delay_seconds() -> float:
    """``THREADS_PUBLISH_DELAY`` 환경변수 읽기 (server.py 와 동일 로직, 기본 30초)."""
    raw = os.environ.get("THREADS_PUBLISH_DELAY")
    if raw is None:
        return DEFAULT_PUBLISH_DELAY
    try:
        return float(raw)
    except ValueError:
        return DEFAULT_PUBLISH_DELAY


def _build_queue(db_path: str) -> Queue:
    """Queue 생성 팩토리 — 테스트가 monkeypatch 로 교체할 수 있게 분리."""
    return Queue(db_path)


def _build_client(access_token: str, user_id: str) -> ThreadsClient:
    """ThreadsClient 생성 팩토리 — 테스트가 monkeypatch 로 교체할 수 있게 분리."""
    return ThreadsClient(access_token=access_token, threads_user_id=user_id)


def _container_call(post: dict[str, Any], client: ThreadsClient) -> str:
    """포스트 row → ``create_container`` 호출 (media_type → kwargs 매핑).

    TEXT 는 ``text``, IMAGE 는 ``image_url``, VIDEO 는 ``video_url`` 을 건넨다.
    캡션(text) 은 IMAGE/VIDEO 에서 존재할 때만 붙인다. TEXT 인데 text 가 None 이면
    ThreadsClient 가 ValueError → 호출자가 mark_failed 처리한다.
    """
    media_type = post["media_type"]
    kwargs: dict[str, Any] = {}
    text = post.get("text")
    if media_type == "TEXT":
        kwargs["text"] = text
    elif media_type == "IMAGE":
        if text:
            kwargs["text"] = text
        kwargs["image_url"] = post.get("image_url")
    elif media_type == "VIDEO":
        if text:
            kwargs["text"] = text
        kwargs["video_url"] = post.get("video_url")
    return client.create_container(media_type, **kwargs)


def _process(
    queue: Queue,
    client: ThreadsClient,
    *,
    limit: int = DEFAULT_LIMIT,
    dry_run: bool = False,
    once: Optional[int] = None,
    delay: float = 0.0,
) -> dict[str, Any]:
    """큐를 순회하며 발행 시도 (core processing loop).

    server.py 의 ``threads_queue_publish_due`` 도 본 함수를 재사용한다.

    Args:
        queue: 발행 큐.
        client: Threads API 클라이언트.
        limit: 1회 실행 최대 발행 수.
        dry_run: 참이면 상태 변경 없이 발행 대상만 나열.
        once: 특정 post id — 주어지면 due/스케줄/레이트리밋 을 무시하고 강제 발행.
        delay: create_container 와 publish 사이 대기(초). Threads 권장 ~30초.

    Returns:
        ``published`` / ``failed`` / ``skipped`` 카운트와 ``messages`` 리스트를
        담은 dict. ``dry_run`` 플래그도 포함된다.
    """
    messages: list[str] = []
    published = 0
    failed = 0
    skipped = 0

    # --once: 특정 포스트 강제 발행 (due/스케줄 무시, 수동 kick 용)
    if once is not None:
        post = queue.get(once)
        if post is None:
            messages.append(f"post id={once} 를 찾을 수 없음 (not found)")
            return {
                "published": 0,
                "failed": 0,
                "skipped": 0,
                "dry_run": False,
                "messages": messages,
            }
        if post["status"] in ("PUBLISHED", "FAILED"):
            messages.append(
                f"post id={once} 상태={post['status']} (이미 종단 상태, 스킵)"
            )
            return {
                "published": 0,
                "failed": 0,
                "skipped": 1,
                "dry_run": False,
                "messages": messages,
            }
        posts = [post]
        rate_check = False  # --once 는 수동 override → 24h 한도 검사 생략
    else:
        posts = queue.due()[:limit]
        rate_check = True

    # --dry-run: 상태 변경 없이 발행 대상만 나열
    if dry_run:
        for p in posts:
            messages.append(
                f"[dry-run] 발행 예정 post id={p['id']} "
                f"type={p['media_type']} status={p['status']}"
            )
        return {
            "published": 0,
            "failed": 0,
            "skipped": len(posts),
            "dry_run": True,
            "messages": messages,
        }

    for idx, post in enumerate(posts):
        # 24h 레이트리밋 검사 — 한도 도달 시 즉시 중단하고 남은 건은 skipped.
        if rate_check and queue.published_in_last_24h() >= RATE_LIMIT_24H:
            remaining = len(posts) - idx
            skipped += remaining
            messages.append(
                f"[rate-limit] 최근 24h 발행 수 >= {RATE_LIMIT_24H}, "
                f"중단 (skipped {remaining}건)"
            )
            break
        try:
            queue.increment_attempt(post["id"])
            container_id = _container_call(post, client)
            if delay > 0:
                time.sleep(delay)
            media_id = client.publish(container_id)
            permalink = f"https://www.threads.net/@<username>/post/{media_id}"
            queue.mark_published(
                post["id"],
                container_id=container_id,
                media_id=media_id,
                permalink_hint=permalink,
            )
            published += 1
            messages.append(
                f"post id={post['id']} 발행 성공 media_id={media_id}"
            )
        except Exception as exc:
            # 한 건 실패가 전체 런을 중단시키지 않는다 — 다음 포스트로 계속.
            queue.mark_failed(post["id"], error=str(exc))
            failed += 1
            messages.append(f"post id={post['id']} 발행 실패: {exc}")
            continue

    return {
        "published": published,
        "failed": failed,
        "skipped": skipped,
        "dry_run": False,
        "messages": messages,
    }


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="threads-poster-runner",
        description="Threads 발행 큐 runner (수동 킥용 CLI)",
    )
    parser.add_argument(
        "--db",
        default=None,
        help="SQLite 큐 DB 경로 (기본: THREADS_POSTER_DB 환경변수 또는 플러그인 루트)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"1회 실행 최대 발행 수 (기본 {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="상태 변경 없이 발행 대상만 출력",
    )
    parser.add_argument(
        "--once",
        type=int,
        default=None,
        help="특정 post id 를 due/스케줄 무시하고 강제 발행 (수동 kick)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    """CLI 진입점 (entry point — 수동 셸 킥용).

    자격증명 미설정 시 설정 안내 메시지 출력 후 exit 0 (호출 스크립트 실패 처리 회피).
    일상적 발행은 세션 안의 ``threads_queue_publish_due`` MCP 도구를 통한다.
    """
    args = _parse_args(argv)
    access_token = os.environ.get("THREADS_ACCESS_TOKEN", "")
    user_id = os.environ.get("THREADS_USER_ID", "")
    if not access_token or not user_id:
        print(
            "[threads-poster-runner] Threads 자격증명이 설정되지 않았습니다 "
            "(THREADS_ACCESS_TOKEN, THREADS_USER_ID 환경변수 필요). "
            "발급 절차는 mcp-servers/threads-poster/CONNECTORS.md 참조. 종료(0)."
        )
        return 0

    db_path = args.db or _default_db_path()
    queue = _build_queue(db_path)
    client = _build_client(access_token, user_id)
    try:
        result = _process(
            queue,
            client,
            limit=args.limit,
            dry_run=args.dry_run,
            once=args.once,
            delay=_publish_delay_seconds(),
        )
    finally:
        queue.close()
        client.close()

    summary = (
        f"published={result['published']} "
        f"failed={result['failed']} "
        f"skipped={result['skipped']}"
    )
    if result["dry_run"]:
        summary += " (dry-run)"
    print(summary)
    for msg in result["messages"]:
        print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
