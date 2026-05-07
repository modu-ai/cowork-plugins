# Strict 5인 파이프라인 명세 (보존용)

이 문서는 `epoko77-ai/im-not-ai` v1.6.1 원본의 **Strict 모드 5인 에이전트 파이프라인** 명세를 cowork 환경에 보존한 것입니다. 현재 `humanize-korean` 스킬은 **Fast 모드 단일 콜**만 구현하며, 이 문서는 향후 별도 워크플로(독립 플러그인 또는 Agent Teams 모드)로 정밀 검증 파이프라인을 확장할 때 참조용입니다.

## 적용 시점

- 입력 8,000자 초과 장문
- Fast 모드 결과가 등급 C·D로 판정된 경우
- 사용자가 `--strict`·"정밀 모드"·"5인 파이프라인"을 명시한 경우
- 내용 훼손 위험이 큰 텍스트(법무·의료·재무 등 정확성 요구 도메인)

## 7인 에이전트 (원본 정의)

| 에이전트 | 모드 | 역할 |
|---|---|---|
| `humanize-monolith` | Fast 디폴트 | 단일 호출 윤문(탐지·윤문·자체검증 일괄, 도구 호출 4~5회 캡) |
| `ai-tell-detector` | Strict | span 단위 JSON 탐지 리포트 생성 |
| `korean-style-rewriter` | Strict | finding 기반 수술적 윤문, 변경률 모니터링 |
| `content-fidelity-auditor` | Strict | 의미 동등성 감사(13항), 훼손 시 롤백 지시 |
| `naturalness-reviewer` | Strict | 잔존 AI 티 · 과윤문 · 자연도 판정, 품질 등급 A~D |
| `korean-ai-tell-taxonomist` | 별도 명령 | 분류 체계(SSOT) 관리, 신규 패턴 심사 승격 |
| `humanize-web-architect` | 옵션 | Next.js 15 + Vercel 웹 서비스 확장 설계 |

cowork 통합 시 위 에이전트 정의는 가져오지 않았습니다(현재 스킬은 단일 콜 Fast 모드만 사용). 원본 정의는 [im-not-ai/.claude/agents/](https://github.com/epoko77-ai/im-not-ai/tree/main/.claude/agents) 참조.

## 데이터 흐름 (Strict)

```
01_input.txt
    ↓ [ai-tell-detector]
02_detection.json
    ↓ [korean-style-rewriter]
03_rewrite.md + 03_rewrite_diff.json
    ↓ [병렬 검증 팀]
    ├→ [content-fidelity-auditor] → 04_fidelity_audit.json
    └→ [naturalness-reviewer]      → 05_naturalness_review.json
    ↓ [오케스트레이터 종합 분기]
    ├→ accept              → final.md + summary.md
    ├→ rewrite_round_2     → Phase B로 복귀(target finding)
    ├→ rollback_and_rewrite → 문제 edit 롤백 후 재윤문
    └→ hold_and_report     → 사람 검토 권고
```

최대 3회 재윤문 후에도 미해결이면 `hold_and_report`로 사람 개입.

## Phase 별 산출물

| 파일 | 내용 |
|---|---|
| `01_input.txt` | 원문 그대로 |
| `02_detection.json` | AI 티 탐지 리포트(위치·종류·심각도) |
| `03_rewrite.md` | 윤문본 |
| `03_rewrite_diff.json` | 윤문 전후 diff(Edit 이력) |
| `03_rewrite_v2.md`, `v3.md` | 2차·3차 윤문본(루프 진입 시) |
| `04_fidelity_audit.json` | 의미 동등성 감사 결과(13항 체크리스트) |
| `05_naturalness_review.json` | 자연도 재측정 결과(잔존·과윤문 판정) |
| `final.md` + `summary.md` | 최종 윤문본 + 점수·주요 변경·등급 요약 |

## 종합 판정 매트릭스

| fidelity | naturalness | 종합 | 후속 |
|---|---|---|---|
| full_pass | accept / accept_with_note | **최종 승인** | Phase D로 |
| full_pass | rewrite_round_2 | **2차 윤문** | Phase B 재호출(target finding) |
| full_pass | rollback_and_rewrite | **롤백 후 재윤문** | 윤문가에 edit 롤백 지시 |
| conditional_pass | - | **롤백된 edit만 재시도** | Phase B 재호출 |
| fail | - | **전면 재작업** | Phase B 전면 재호출 |

## fidelity 13항 체크리스트 (content-fidelity-auditor)

1. 사실 명제 동등성
2. 수치·통계·비율 일치
3. 고유명사·기관명·인명 100% 보존
4. 직접 인용 한 글자 보존
5. 시간 표현(연도·날짜·시점) 일치
6. 인과 관계·논리 흐름 동등
7. 주장의 강도(단언 vs 추측) 보존
8. 부정·긍정 polarity 보존
9. 조건절·전제 보존
10. 주체-객체 관계 보존
11. 비유·상징 의도 보존(원문에 있는 것만)
12. 명시되지 않은 함의 추가 금지
13. 장르 적합성(칼럼·리포트 register)

한 항목이라도 위반이면 해당 edit 롤백 지시 → 윤문가에 conditional_pass 신호.

## naturalness 판정(naturalness-reviewer)

- **accept**: S1 잔존 0, S2 잔존 ≤2, 변경률 10~25%, 자연도 점수 70%+
- **accept_with_note**: S1 잔존 0, S2 잔존 3~4 — 비치명적 잔존 메모만 첨부
- **rewrite_round_2**: S1 잔존 1~2 또는 과윤문 시그널 1~2개 → 2차 윤문 진입
- **rollback_and_rewrite**: 과윤문 시그널 3+ → 윤문가에 롤백 지시

## 향후 확장 시 cowork 적용 방안

### 옵션 1: 독립 플러그인 (`moai-humanize`)

7인 에이전트 + 1 skill + 2 commands를 캡슐화한 독립 플러그인. `.claude/agents/` 경로에 7개 에이전트 정의 배치, `commands/humanize.md`·`humanize-redo.md`로 슬래시 커맨드 노출.

### 옵션 2: Agent Teams 모드

cowork v2.x의 Agent Teams 모드를 활용해 `humanize-review-team`을 동적 구성. 워크플로우:
1. `TeamCreate` → 팀 생성(detector·rewriter·auditor·reviewer)
2. 단계별 `Agent()` 호출(role_profile 사용)
3. 병렬 검증은 implementer/reviewer 역할로 분산
4. `TeamDelete` → 자원 해제

### 옵션 3: 단일 스킬 시뮬레이션 (현재는 미구현)

이 스킬 본문에서 Phase A→B→C→D를 도구 호출로 시뮬레이션 가능합니다(SKILL.md 본문이 5배 길어지고 신뢰도가 단일 콜 대비 낮아져 현재는 채택하지 않음).

## 라이선스

원본 명세는 [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) v1.6.1 (MIT License)에서 보존했습니다. 7인 에이전트 정의 본문은 가져오지 않았으며, 원문 출처를 그대로 참조하시기 바랍니다.

---

Version: 2.1.0 (cowork preservation)
Original Source: epoko77-ai/im-not-ai v1.6.1, MIT License
Last Updated: 2026-05-07
