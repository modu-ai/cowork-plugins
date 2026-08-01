---
title: "문제 해결"
weight: 100
---

# 문제 해결

## 문제 → 해결

| 문제 | 해결 |
|------|------|
| `command not found` | PATH 확인 / 재설치 |
| npm 설치 실패 | 네트워크·프록시 확인 |
| 회사 방화벽 | `HTTP_PROXY` / `HTTPS_PROXY` 설정 |
| SSL/TLS 오류 | 인증서·시간 동기 확인 |
| 로그인 루프 | 캐시 삭제 후 재로그인 |
| Node.js 버전 | ES2020 지원 버전 필요 (LTS 권장) |

## Node.js 버전 확인

```bash
node -v
```

ES2020을 지원하는 버전(LTS 권장)이어야 합니다.

## 디버그 명령

- `claude --debug` — 상세 로그 출력
- `/debug` — 세션 상태·훅 로그 확인

## Sources

- [Troubleshoot install & login](https://code.claude.com/docs/en/troubleshoot-install)
- [What's new](https://code.claude.com/docs/en/whats-new)
