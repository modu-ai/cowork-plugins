"""실제 유튜브 API 연결 확인.

MCP 서버를 붙이기 전에 **자격증명이 진짜 통하는지** 터미널에서 먼저 확인하는 용도다.
테스트 코드는 가짜 응답으로만 돌기 때문에, 엔드포인트·권한·할당량이 실제로 맞는지는
한 번은 진짜로 불러봐야 안다.

    uv run --directory <서버경로> python -m moai_mcp_youtube.selftest

읽기만 한다 — 아무것도 올리거나 바꾸지 않는다. 소모 할당량은 3 units 안쪽이다.
"""

from __future__ import annotations

import sys

from moai_mcp_core import McpToolError

from .client import YouTubeClient
from .config import load_config

OK = "  [OK] "
NG = "  [X]  "


def main() -> int:
    print("유튜브 연결 확인을 시작합니다 (읽기 전용, 약 3 units 소모)\n")

    config = load_config()

    # 1. 환경변수
    print("1) 자격증명 확인")
    missing = [
        name
        for name, value in (
            ("YOUTUBE_CLIENT_ID", config.client_id),
            ("YOUTUBE_CLIENT_SECRET", config.client_secret),
            ("YOUTUBE_REFRESH_TOKEN", config.refresh_token),
        )
        if not value
    ]
    if missing:
        print(NG + f"환경변수가 비어 있습니다: {', '.join(missing)}")
        print("\n   CONNECTORS.md 의 절차로 발급한 뒤 환경변수에 넣고 다시 실행하세요.")
        print("   macOS   : export YOUTUBE_CLIENT_ID=... (한 줄씩)")
        print("   Windows : $env:YOUTUBE_CLIENT_ID=\"...\" (PowerShell)")
        return 1
    print(OK + "세 값이 모두 설정돼 있습니다")

    client = YouTubeClient(config)

    # 2. 토큰 발급 — 여기서 막히면 권한·동의 화면 문제다
    print("\n2) 액세스 토큰 발급")
    try:
        client._refresher.access_token(force=True)  # noqa: SLF001 — 진단 목적
    except McpToolError as exc:
        print(NG + exc.message)
        print("\n   흔한 원인:")
        print("   - 동의 주소에 access_type=offline · prompt=consent 를 빠뜨림")
        print("   - Google Cloud 동의 화면이 '테스트' 상태 (리프레시 토큰 일주일 만료)")
        print("   - 리프레시 토큰을 이미 다른 곳에서 폐기함")
        return 1
    print(OK + "토큰을 받았습니다")

    # 3. 채널 조회 — 실제 API 왕복
    print("\n3) 채널 조회 (channels.list, 1 unit)")
    try:
        data = client.get(
            "channels.list",
            "channels",
            {"part": "snippet,statistics", "mine": "true"}
            if not config.channel_id
            else {"part": "snippet,statistics", "id": config.channel_id},
        )
    except McpToolError as exc:
        print(NG + exc.message)
        if exc.details.get("status") == 403:
            print("\n   403 이면 API 가 꺼져 있거나 권한(scope)이 부족합니다.")
            print("   Google Cloud → API 및 서비스 → 라이브러리에서")
            print("   'YouTube Data API v3' 사용 여부를 확인하세요.")
        return 1

    items = (data or {}).get("items") or []
    if not items:
        print(NG + "채널을 찾지 못했습니다. YOUTUBE_CHANNEL_ID 를 확인하세요.")
        return 1
    snippet = items[0].get("snippet", {})
    stats = items[0].get("statistics", {})
    print(OK + f"채널: {snippet.get('title')}")
    print(f"       구독자 {stats.get('subscriberCount', '비공개')} · 영상 {stats.get('videoCount', '?')}개")

    # 4. 영상 목록 — search 회피 경로가 실제로 도는지
    print("\n4) 내 영상 목록 (업로드 재생목록 경유, 2 units)")
    try:
        playlist_id = client.uploads_playlist_id()
        listing = client.get(
            "playlistItems.list",
            "playlistItems",
            {"part": "snippet,contentDetails", "playlistId": playlist_id, "maxResults": 3},
        )
    except McpToolError as exc:
        print(NG + exc.message)
        return 1

    videos = (listing or {}).get("items") or []
    print(OK + f"최근 영상 {len(videos)}개를 읽었습니다")
    for v in videos:
        print(f"       - {v.get('snippet', {}).get('title')}")

    # 5. 할당량
    quota = client.quota()
    print(f"\n5) 할당량: {quota['used']} 사용 / {quota['remaining']} 남음 (추정)")

    print("\n연결 정상입니다. 이제 Claude Cowork 또는 ChatGPT Work 에서 쓰실 수 있습니다.")
    client.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
