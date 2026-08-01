---
title: "권한·안전 기초"
weight: 95
---

# 권한·안전 기초

## 기본 동작

파일 쓰기·셸 명령·MCP는 기본적으로 **"물어보고 허락"**받습니다(default 모드). Claude가 "이 파일을 수정할까요?"처럼 뭘 하려는지 보여주고 승인을 받습니다.

## 권한 모드

- **default** — 매 작업마다 확인
- **plan** — 계획만 세우고 실행 안 함
- **acceptEdits** — 파일 편집 자동 허용
- **bypassPermissions** — 모두 허용 (위험)
- **auto** — 도구별 자동 승인

`Shift+Tab`으로 모드를 순환합니다.

## allow / deny 규칙

`settings.json`에서 허용·거부 패턴을 지정합니다. 예:
```json
{ "permissions": { "allow": ["Bash(npm test)"], "deny": ["Bash(rm -rf *)"] } }
```

## {{< icon triangle-alert >}} 주의

`--dangerously-skip-permissions`는 **모든 안전장치를 해제**합니다 — 파일 삭제·명령 실행이 무제한이 되므로 절대 쓰지 마세요.

## Sources

- [Permissions](https://code.claude.com/docs/en/permissions)
- [Permission modes](https://code.claude.com/docs/en/permission-modes)
