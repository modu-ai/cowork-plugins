---
title: "플러그인 사용"
weight: 70
description: "플러그인을 어디서 찾고 어떻게 설치·관리하는지, 한국 실무용 cowork-plugins 마켓플레이스 사용법까지 정리합니다."
geekdocBreadcrumb: true
---
> 플러그인(plugin)은 여러 스킬·서브에이전트·MCP 커넥터를 하나의 도메인으로 묶은 번들입니다. 사용자는 플러그인을 설치하기만 하면, 그 안의 스킬들이 자연어 요청에 자동으로 반응하게 됩니다.

## 플러그인은 어디서 찾나

크게 세 곳에서 플러그인을 구합니다.

- **Claude 공식 플러그인 카탈로그**: [claude.com/plugins](https://claude.com/plugins) — 영업·재무·법무·마케팅·HR 등 기본 제공
- **공식 오픈소스**: [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- **커뮤니티 마켓플레이스**: [`modu-ai/cowork-plugins`](https://github.com/modu-ai/cowork-plugins) — 한국 실무 환경 최적화(사업계획·IR·세무·법무·카드뉴스 등 17개)

## 설치 흐름

```mermaid
flowchart LR
    A["사이드바 > 사용자 지정<br/>> 개인 플러그인"] --> B["마켓플레이스 추가<br/>modu-ai/cowork-plugins"]
    B --> C["목록에서<br/>플러그인 선택"]
    C --> D["+ 버튼으로<br/>설치"]
    D --> E["✅ 스킬 자동 활성화"]

    style A fill:#e6f0ff,stroke:#3070d0
    style B fill:#fff4e6,stroke:#e09040
    style C fill:#e6ffec,stroke:#30a050
    style D fill:#f5e6ff,stroke:#9050d0
    style E fill:#dff5dd,stroke:#3a8a3a,stroke-width:2px
```

커뮤니티 마켓플레이스를 예로 들면 아래 순서입니다.

1. Cowork **좌측 사이드바 > 사용자 지정(Customize) > 개인 플러그인** 진입
2. **플러그인 추가 > 마켓플레이스 추가** 버튼
3. URL 칸에 `modu-ai/cowork-plugins` 입력 → 동기화
4. 목록에서 원하는 플러그인 옆 **+** 클릭해 설치
5. `moai-core`가 있다면 반드시 가장 먼저 설치 — 프로젝트 초기화·라우터·AI 슬롭 검수가 여기에 있습니다.

설치가 끝나면 [빠른 시작](../../plugins/quick-start/)의 `/project init`으로 프로젝트 맞춤 `CLAUDE.md`를 생성할 수 있습니다.

## 플러그인 관리

- **활성/비활성 토글**: 설치한 뒤에도 프로젝트별로 켰다 끌 수 있습니다.
- **업데이트**: 마켓플레이스에서 최신 버전 확인 후 재동기화합니다.
- **조직 정책 (Team·Enterprise)**: 관리자가 승인한 플러그인만 구성원이 사용하도록 제한할 수 있습니다.

## 커스터마이즈

기존 플러그인을 조직 맥락에 맞춰 수정하려면 [플러그인 커스터마이즈 튜토리얼](https://claude.com/resources/tutorials/how-to-customize-plugins-in-cowork)을 참고하세요.

## 다음 단계

- [플러그인 카탈로그](../../plugins/) — 실제 설치 가능한 플러그인 모음
- [빠른 시작](../../plugins/quick-start/) — 설치 후 5분 안에 첫 체인 돌리기

---

### Sources

- [Use plugins in Claude Cowork](https://support.claude.com/en/articles/13837440)
- [Manage plugins for your organization](https://support.claude.com/en/articles/13837433)
- [Customize Cowork with plugins (blog)](https://claude.com/blog/cowork-plugins)
- [How to customize plugins in Cowork](https://claude.com/resources/tutorials/how-to-customize-plugins-in-cowork)
