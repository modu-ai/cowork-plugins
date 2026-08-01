---
title: "심화 — 자율 실행 /goal·/loop·auto"
weight: 104
---

# 심화 — 자율 실행 /goal·/loop·auto

세 가지 자율 실행 기본형입니다. "무엇이 다음 턴을 시작하는가"로 고릅니다.

## 비교

| 방식 | 다음 턴 시작 | 멈춤 |
|------|-------------|------|
| `/goal` | 이전 턴 끝 | 조건 충족 |
| `/loop` | 시간 간격 | 사용자 취소 |
| auto mode | (도구 승인 자동화) | — |

## `/goal <condition>`

목표 기반 연속 실행. 조건이 충족될 때까지 턴을 이어갑니다.

**예**: `/goal 모든 테스트 통과할 때까지 계속`

## Implementation Kickoff Approval

자율 실행도 **진입 전 사람 승인은 필수**입니다. 자율 실행이 파괴적 작업(삭제·푸시)을 미리 승인하지는 않습니다.

## Sources

- [Best practices](https://code.claude.com/docs/en/best-practices)
- [Common workflows](https://code.claude.com/docs/en/common-workflows)
