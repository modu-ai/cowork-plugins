---
title: "심화 — 샌드박스"
weight: 105
---

# 심화 — 샌드박스

## 격리 패턴

- **권한 시스템** — 1차 샌드박스 (default 모드가 매 작업 확인)
- **Docker / devcontainer** — 컨테이너로 강한 분리 (`devcontainer.json` 설정). 프로젝트 루트에 devcontainer를 정의해 재사용
- **VM** — 가상머신 격리, 가장 강력한 분리

격리가 강할수록 Claude가 시스템에 미치는 영향이 제한됩니다. 작업 위험도가 높을수록 더 강한 격리를 쓰세요.

## 최소 권한 폴더

특정 프로젝트 폴더만 지정해 접근 범위를 제한합니다. **전체 홈 디렉토리를 열지 마세요.**

**예**: `~/projects/my-app`만 허용, `~/` 전체는 거부.

## 왜 격리가 필수인가

`--dangerously-skip-permissions`를 쓰면 모든 안전장치가 해제됩니다. 이 경우 반드시 Docker/VM 같은 격리 환경에서만 써야 합니다 — 그렇지 않으면 Claude가 시스템 전체에 접근할 수 있습니다.

일반적인 default 모드에서도, 신뢰하지 않는 코드베이스(제3자 저장소 등)를 다룰 때는 격리 환경이 권장됩니다.

## Sources

- [Permissions](https://code.claude.com/docs/en/permissions)
- [Permission modes](https://code.claude.com/docs/en/permission-modes)
