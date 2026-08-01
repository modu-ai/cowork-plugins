---
title: "심화 — GitHub Actions·CI"
weight: 103
---

# 심화 — GitHub Actions·CI

## claude-code-action

공식 GitHub Action. PR/이슈에서 `@claude` 멘션으로 Claude Code를 호출합니다.

### 설정

1. 저장소에 워크플로우 파일 추가 (`.github/workflows/claude.yml`)
2. `anthropics/claude-code-action` 액션 사용
3. PR에서 `@claude` 멘션으로 호출

## 헤드리스 CI

`claude -p "<prompt>"`로 파이프라인에서 자동 실행합니다.

**예**: `claude -p "lint 에러 수정해줘"` → 종료 코드로 성공/실패 판별.

## {{< icon triangle-alert >}} 보안 주의

신뢰할 수 없는 GitHub 콘텐츠 처리 시 CI 비밀(secret) 노출 위험이 있습니다. 권한과 비밀 스코핑에 주의하세요.

## Sources

- [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Troubleshoot](https://code.claude.com/docs/en/troubleshoot-install)
