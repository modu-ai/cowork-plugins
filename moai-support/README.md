# moai-support

고객 지원 플러그인 — 티켓 분류, 응답 초안, KB 문서, 에스컬레이션 관리.

고객 문의 접수부터 우선순위 분류, 경어 기반 응답 초안, 지식베이스 문서 작성, VIP 에스컬레이션까지 CS 운영 전반을 지원합니다. Zendesk, Freshdesk, 카카오비즈니스 형식을 지원합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [ticket-triage](./skills/ticket-triage/) | 유형 분류(기술/결제/배송/불만), 긴급도(P1~P4), 담당팀 배정 | 1 | ✅ |
| [draft-response](./skills/draft-response/) | 이메일/채팅/공식 답변서 초안, 채널별 어조 최적화 | 0 | ✅ |
| [kb-article](./skills/kb-article/) | FAQ, 사용자 가이드, 트러블슈팅, 헬프센터 아티클 | 0 | ✅ |
| [escalation-manager](./skills/escalation-manager/) | 에스컬레이션 레벨 배정, VIP 응대, VOC 분석, CS 요약 보고서 | 1 | ✅ |

## Cowork 커넥터

| 서비스 | 연결 | 용도 |
|--------|------|------|
| Slack | Settings > Connectors > Slack | CS 채널 문의 수집, 에스컬레이션 알림 |
| Notion | Settings > Connectors > Notion | KB 문서 생성/관리, 에스컬레이션 로그 |

커넥터 미연결 시에도 모든 스킬이 동작합니다 (수동 입력/마크다운 출력으로 폴백). 커넥터 설정 상세: [CONNECTORS.md](./CONNECTORS.md)

## 사용 예시

```
환불 요청 고객에게 보낼 이메일 초안 써줘. 정책상 7일 이내만 환불 가능해.
```

```
배송 관련 자주 묻는 질문 FAQ 10개 작성해줘
```

```
이번 주 CS 요약 보고서 만들어줘. 불만 유형별 분류 포함.
```

## 주요 워크플로우 체인

```
티켓 자동 분류·배정
  ticket-triage(유형·긴급도) → draft-response(응답 초안) → ai-slop-reviewer

지식베이스 운영
  kb-article(FAQ·가이드) → docx-generator(헬프센터 아티클) → ai-slop-reviewer

VIP·불만 에스컬레이션
  ticket-triage(P1 긴급) → escalation-manager(VIP 응대 + VOC 분석) → docx-generator

주간 CS 보고
  escalation-manager(VOC 분석) → moai-bi/executive-summary → pptx-designer
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| B2B 영업 메일·후속 시퀀스 | `moai-sales/proposal-writer` (예정 sales-followup) |
| 마케팅 이메일 시퀀스 | `moai-marketing/email-sequence` |
| 카카오 채널 마케팅 콘텐츠 | `moai-marketing/sns-content` |
| KB 문서를 한글(.hwpx)·PDF로 | `moai-office/hwpx-writer`, `moai-office/pdf-writer` |

## 한국 CS 환경 특화

- **카카오비즈니스·네이버 톡톡** 응답 형식 호환
- **개인정보보호법** 준수 자동 점검 (고객 식별 정보 마스킹)
- **경어 표준**: 직급·연령에 따른 자연스러운 한국어 어조
- **Zendesk·Freshdesk·자체 CRM** export 형식 지원
- **VOC 분석**: 불만·문의·칭찬 분류 + 카테고리별 트렌드

## 설치

Settings > Plugins > cowork-plugins에서 `moai-support` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
