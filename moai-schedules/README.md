# moai-schedules

스케줄 관리 플러그인 — 반복 업무 자동 실행, 스케줄 등록/조회/관리.

다른 `moai-*` 스킬을 정해진 시간에 자동으로 실행하여 반복 업무를 자동화합니다. Claude Cowork의 `/schedule` 명령과 Scheduled Tasks 기능을 활용합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [create-schedule](./skills/create-schedule/) | 자동화 스케줄 설정, 일별/주별/수동 실행 주기, 프롬프트 템플릿 작성 | 1 | ✅ |
| [list-schedules](./skills/list-schedules/) | 스케줄 목록 조회, 상태 확인(활성/일시정지/오류), 실행 이력 | 0 | ✅ |
| [manage-schedule](./skills/manage-schedule/) | 스케줄 수정/삭제/일시정지/재개, 복제, 즉시 실행, 최적화 권고 | 0 | ✅ |

## 사용 예시

```
매주 월요일 오전 9시에 weekly report 자동 생성해줘
```

```
등록된 스케줄 목록 보여줘
```

```
브리핑 스케줄 주기를 매일에서 주 3회로 변경해줘
```

## 설치

Settings > Plugins > moai-cowork-plugins에서 `moai-schedules` 선택
