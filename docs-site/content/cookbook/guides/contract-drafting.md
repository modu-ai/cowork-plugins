---
title: "계약서 작성 가이드"
weight: 10
description: "NDA · SLA · 공급계약 · 이용약관을 moai-legal 스킬로 작성하는 절차와 한국 실무 체크포인트."
geekdocBreadcrumb: true
---
> 계약서는 한 번 잘못 보내면 회수가 어렵습니다. cowork-plugins의 `moai-legal` 스킬을 활용해 초안 작성·위험 조항 식별·표준 조항 적용까지 안전하게 진행합니다.

## 사용 스킬

| 단계 | 스킬 | 용도 |
|---|---|---|
| 빠른 NDA 검토 | `moai-legal:nda-triage` | 받은 NDA를 5분 내 위험도 분류 |
| 본격 검토·작성 | `moai-legal:contract-review` | 위험 조항 분석 + 수정 권고 |
| 컴플라이언스 체크 | `moai-legal:compliance-check` | 개인정보·전자상거래법 적합성 |
| AI 슬롭 검수 | `moai-core:ai-slop-reviewer` | 외부 발송 전 마지막 검수 |

## 한국 실무 체크포인트

작성·검토 시 한국 법무 실무에서 가장 자주 누락되는 4가지:

1. **준거법·관할 명시** — 한국법 적용 + 서울중앙지방법원이 한국 기업끼리 계약의 기본
2. **개인정보처리방침 별도 합의** — 계약 본문이 아닌 별도 동의서로 분리
3. **불가항력 조항** — 코로나·자연재해·정부 명령 등 명시
4. **분쟁해결 단계** — 협의 → 조정 → 중재(KCAB) → 소송 순서 명시

## 워크플로우 예시 — NDA 검토 30초 체인

이메일로 NDA가 도착했을 때:

```
> "이 NDA 검토해줘. 위험 조항만 표로 뽑아주고, 우리 측에 불리한 부분만 빨갛게 표시해서 DOCX로 저장해줘."
```

`nda-triage` → `contract-review` → `docx-generator` 체인이 자동으로 흘러갑니다.

## 표준 조항 라이브러리 만들기

자주 쓰는 조항(보안 책임 한도, 데이터 반환·파기 절차, 손해배상 상한)을 회사 표준으로 고정하려면:

```
> "이 NDA에서 '데이터 파기' 조항 표현을 우리 회사 표준으로 만들어 메모리에 저장해줘. 다음부터는 자동으로 이 표현 사용해줘."
```

[프로젝트 메모리](../../../cowork/projects-memory/)의 `feedback` 종류로 저장되어, 같은 프로젝트의 다음 NDA 검토에서 자동 적용됩니다.

## 자주 겪는 실수

- **AI 초안을 그대로 발송** — 반드시 변호사 또는 사내 법무팀 검토 후 외부에 보냅니다. AI는 초안 도구입니다 ([안전하게 사용하기](../../../cowork/safety/)).
- **민감 정보가 든 PDF를 그대로 입력** — 인적사항·계좌번호는 마스킹 후 입력합니다.
- **계약 상대방이 보낸 표준 양식이라고 그대로 사인** — 상대방 표준 양식이 바로 우리 측에 가장 불리한 양식인 경우가 흔합니다.

## 다음 단계

- [법률 리스크 관리](../legal-risk/) — 계약 외 법적 리스크 전반
- [컴플라이언스 체크리스트](../../templates/compliance/) — GDPR·PIPA·ISMS 체크
- [트랙 — 법률](../../tracks/track-legal/)

---

### Sources

- moai-legal 플러그인 [`contract-review`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-legal/skills/contract-review/SKILL.md), [`nda-triage`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-legal/skills/nda-triage/SKILL.md)
- [한국 표준약관 (공정거래위원회)](https://www.ftc.go.kr)
