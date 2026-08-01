---
title: "아키텍처 개요 — 격리 VM"
weight: 94
---

# 아키텍처 개요 — 격리 VM

Claude Cowork는 호스트 OS에 직접 실행하지 않고 **격리된 가상머신(VM)** 안에서 작업을 수행합니다. 이것이 Cowork 안전 모델의 핵심입니다.

## 플랫폼별 격리

- **macOS**: Linux VM으로 격리
- **Windows**: Hyper-V/KVM으로 격리

## 왜 격리인가

Cowork는 파일을 읽고 쓰고 명령을 실행하는 에이전트입니다. 격리 VM은 Claude가 사용자가 **명시적으로 공유한 폴더 밖**의 파일에 닿지 못하게 합니다. 설령 문제가 생겨도 VM 안에 갇혀 호스트 시스템 전체로 퍼지지 않습니다.

## 관리자 제어

- **실행 범위 제한** — 어느 폴더까지 허용할지
- **네트워크 송신(egress) 정책** — 외부 통신 허용 범위
- **세분화된 MCP 권한** — 커넥터별 접근 통제
- **실행 모드별 격리** — 모드마다 독립 격리 적용

## 사용자 관점

- 공유한 폴더만 Claude가 봅니다. 그 바깥은 닿을 수 없습니다.
- VM에서 실행되므로 호스트의 다른 앱·파일에 영향을 주지 않습니다.
- 약간의 성능 오버헤드가 있을 수 있습니다.

## 설치 시 주의사항

- VM 설치에 **로컬 관리자 권한**이 필요합니다.
- 회사 관리 PC에서는 IT 부서 승인이 필요할 수 있습니다.

## Sources

- [Claude Cowork 아키텍처 개요 (KO)](https://support.claude.com/ko/articles/14479288)
- [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)
