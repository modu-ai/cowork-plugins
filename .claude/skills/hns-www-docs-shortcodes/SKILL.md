---
description: www Hugo 숏코드 카탈로그 — icon/mascot/terminal/catalog-count/employee-skills/mermaid/version 등 10종 사용법. 하드코딩 금지 집계 숏코드 포함.
metadata:
  version: "1.0.0"
  category: "reference"
triggers:
  keywords: ["숏코드", "shortcode", "icon", "mascot", "catalog-count", "employee-skills"]
---

# Hugo 숏코드 카탈로그 (www/layouts/shortcodes/)

| 숏코드 | 용도 | 호출 예 |
|---|---|---|
| `icon` | DS Lucide 아이콘 (이모지 대체 전용) | `{{< icon check >}}` · `{{< icon name="triangle-alert" size="20" class="tone-warning" >}}` |
| `mascot` | 6종 마스코트 | `{{< mascot thinking >}}` |
| `terminal` | macOS 터미널 chrome 코드블록 | `{{< terminal title="설치" lang="bash" >}}...{{< /terminal >}}` |
| `catalog-count` | data에서 자동 집계 (**하드코딩 금지**) | `{{< catalog-count plugins >}}` · `{{< catalog-count skills >}}` |
| `employee-agents` | 직원별 에이전트 표 자동 생성 | `{{< employee-agents "moai-designer" >}}` |
| `employee-skills` | 직원별 스킬 표 자동 생성 | `{{< employee-skills "moai-designer" >}}` |
| `mermaid` | 다이어그램 (DS 팔레트 자동) | `{{< mermaid >}}...{{< /mermaid >}}` |
| `version` | 사이트 버전 (v1.1.0) | `{{< version >}}` |
| `release-date` | 릴리스 날짜 | `{{< release-date >}}` |
| `screenshot-request` | 스크린샷 자리표시자 (DS alert) | `{{< screenshot-request "설명" >}}` |

## 규칙
- **catalog-count / employee-agents / employee-skills**는 `data/agent_teams.json`에서 자동 집계 — **하드코딩 금지** (드리프트 방지). 데이터는 `gen-agent-teams.py`로 재생성.
- `icon`은 이모지의 **유일한 대체** — 본문에 이모지 쓰지 말고 `icon` 숏코드.
- 마크다운 호출과 레이아웃 partial 호출(`{{ partial "ds-icon" "camera" }}`) 양쪽 지원.
