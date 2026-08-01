# CS매니저 (moai-cs)

고객지원·CRM 전담 AI 직원입니다. 티켓 분류, 응답 초안, 에스컬레이션 처리, 지식베이스 작성부터 VOC 분석, 채널별 CRM 메시지까지 고객 접점 실무 스킬 6종을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

**이런 분께 추천**: 온라인 셀러 · CS 담당자 · 1인 사업자

## 설치

Claude Code에서 두 단계로 설치합니다:

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-cs@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-cs
```

## 스킬 6종

호출 형식: `/moai-cs:business-<스킬명>` — 예: `/moai-cs:business-ticket-triage`. 자연어 요청("이 문의 분류해줘")으로도 자동 매칭됩니다.

### 티켓·응대 (4종)

| 스킬 | 역할 |
|------|------|
| `business-ticket-triage` | 문의 유형 분류(기술/결제/배송/불만) · 긴급도 P1~P4 배정 · 담당팀 배정 · 에스컬레이션 판단 |
| `business-draft-response` | 한국어 경어 기반 이메일·채팅·공식 답변서 응답 초안 (채널별 어조 맞춤) |
| `business-escalation-manager` | 불만 에스컬레이션 레벨 배정 · VIP 응대 · 주간 CS 요약 보고서 |
| `business-kb-article` | FAQ · 사용자 가이드 · 트러블슈팅 문서 · 정책 안내문 (Zendesk·Freshdesk·카카오비즈니스 형식) |

### VOC·채널 메시지 (2종)

| 스킬 | 역할 |
|------|------|
| `commerce-voc-triage` | 멀티채널 리뷰 통합 분석 + VOC 3축 분류 · KTAS 5단계 우선순위 트리아지 |
| `commerce-channel-message` | NCM 프레임워크 기반 검색·광고·CRM·앱 푸시 채널별 메시지 15종 + 운영 카피 생성 |

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `cs-responder` | worker | 티켓 트리아지·응답 초안·에스컬레이션·KB 문서·VOC 분석·채널 메시지 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 미승인 약속 금지(환불·보상은 셀러 결정 플레이스홀더)·개인정보 마스킹·감정 완화 우선·VOC 수치 출처 명시를 HARD 규칙으로 준수 |
| `voc-auditor` | read-only audit | 응대 초안 품질, 에스컬레이션 판정-근거 정합성, VOC 분류 근거, 미승인 약속·개인정보 노출을 회의적으로 검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 이관 안내

이 스킬들은 기존 `moai-coworker`(business 카테고리 4종)와 `moai-seller`(commerce 카테고리 2종)에서 고객지원 도메인만 분리해 이관한 것입니다. 구 경로로 호출하던 워크플로우는 `moai-cs:` 네임스페이스로 갱신하세요.

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
