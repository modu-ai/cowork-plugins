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

## 설치

Settings > Plugins > moai-cowork-plugins에서 `moai-support` 선택
