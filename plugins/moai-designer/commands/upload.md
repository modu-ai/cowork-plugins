---
description: 디자인 시스템 자산을 Claude Design에 업로드 — 자동(DesignSync MCP) 우선 + 수동 폴백
argument-hint: "[DESIGN.md / 자산 폴더 경로]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Upload design system assets to Claude Design (auto-first with manual fallback).

Use Skill("design-sync-upload") with arguments: $ARGUMENTS

Auto path uses the DesignSync MCP (`write_files` / `register_assets` / `finalize_plan`) and requires `/design-login`. When unauthenticated or the MCP is unavailable, it falls back to emitting `UPLOAD-GUIDE.md` + a staged asset folder for manual upload.

---

> **ChatGPT Work(Codex)에서는** 슬래시 명령이 없습니다 — Codex 플러그인 규격은 `skills/`·`hooks/`·
> `.mcp.json`만 지원하고 `commands/`는 지원하지 않습니다. 기능은 그대로 있으니 자연어로 부르세요:
>
> > 디자인 동기화해서 업로드해줘
>
> 이 커맨드는 Claude Cowork 전용 단축키이며, 실제 일은 위 `Skill(...)`이 합니다.
