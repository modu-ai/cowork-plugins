---
name: roadmap-manager
description: >
  로드맵 관리 — 프로젝트 트래커, 파트너십 개발, 지속가능성 감사, 다양성&포용 하네스. 로드맵, 마일스톤, 프로젝트 관리, MOU, 전략적 제휴.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 로드맵 관리 (Roadmap Manager)

> moai-product | 프로젝트 및 파트너십 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| project-tracker | 프로젝트 트래커 | 프로젝트 일정, 마일스톤, 리소스 관리 |
| partnership-development | 파트너십 개발 | 전략적 제휴, MOU, 공동사업 기획 |
| sustainability-audit | 지속가능성 감사 | 환경 영향 평가, 지속가능성 지표 |
| diversity-inclusion | 다양성 & 포용 | DEI 전략, 포용적 조직 문화 설계 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

로드맵, 마일스톤, 프로젝트 관리, 일정, 리소스, 파트너십, MOU, 제휴, 지속가능성, DEI

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 전략 판단 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
