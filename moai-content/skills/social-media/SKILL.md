---
name: social-media
description: |
  [DEPRECATED v2.3.0] 본 스킬은 moai-marketing:sns-content로 흡수되었습니다. 신규 호출은 /sns-content를 사용하세요.
  글로벌 4채널(스레드·X·링크드인·유튜브쇼츠)과 한국 3채널(인스타·네이버 블로그·카카오)을 모두 sns-content에서 지원합니다.
  본 스텁은 v2.5.0까지 외부 참조 호환성 보존용으로 유지됩니다.
user-invocable: true
version: 2.3.0
---

# social-media — RELOCATED

## REDIRECT

본 스킬은 **v2.3.0부터 `moai-marketing:sns-content`로 흡수**되었습니다.

## 마이그레이션

| 기존 호출 | 신규 호출 |
|----------|----------|
| `/social-media` | `/sns-content` |

`sns-content`는 다음 두 가지 모드를 모두 지원합니다.

### 한국 3채널 모드 (기본)

- 인스타그램 (피드·릴스·스토리)
- 네이버 블로그 (C-Rank 최적화)
- 카카오 채널

### 글로벌 4채널 모드 (v2.3.0 신규 — social-media에서 이관)

- 스레드 (Threads)
- X (구 Twitter)
- 링크드인 (LinkedIn)
- 유튜브 쇼츠 (YouTube Shorts)

## 통합 사유

`moai-content:social-media`와 `moai-marketing:sns-content`가 SNS 콘텐츠 영역에서 책임 경계가 모호하여 셀러·마케터가 어디로 호출할지 혼동되는 문제를 해결하기 위해 단일 스킬로 통합했습니다 (SPEC-CATALOG-CLEANUP-007 REQ-CLEANUP-003).

## 제거 일정

본 스텁은 cowork-plugins 정책상 **최소 2 minor 버전 (v2.5.0)까지 유지**됩니다. 외부에서 `/social-media`를 직접 참조하는 코드가 있다면 v2.5.0 이전에 `/sns-content`로 마이그레이션해주세요.

---

Version: 2.3.0
Classification: DEPRECATED → moai-marketing:sns-content
Relocated: v2.3.0 (SPEC-CATALOG-CLEANUP-007)
