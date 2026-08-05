---
description: 하이브리드 디자인 워크플로우 — Path A(Claude Design import) 또는 Path B(코드 기반 브랜드 디자인) 경로 선택
argument-hint: "[자연어 요청]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Route the request into the `/design` hybrid workflow (03 §5.2). The orchestrator collects the path choice via AskUserQuestion first, then dispatches `$ARGUMENTS` into the matching pipeline. Obey `design.yaml` (`.moai/config/sections/design.yaml`) parameters — never hardcode thresholds.

**Path A — Claude Design import** (user has a handoff bundle / URL):
1. Skill("design-workflow") — README-first bundle import + security scan (reject executables/symlinks/traversal) + `manifest.json` version whitelist → `.moai/design/{tokens,components,copy}.json`
2. Skill("design-handoff-reader") — summarize bundle + emit paste-ready Claude Code instruction
3. Skill("design-handoff") — assemble 5-file handoff package when a handoff is the deliverable

**Path B — Code-based brand design** (no bundle; design from brand directly):
1. Skill("design-system-prep") + Skill("design-brand-system") in parallel — brand assets → DESIGN.md + DTCG tokens (WCAG 2.1 AA)
2. Skill("design-copywriting") — brand-aligned copy (anti-AI-slop, generation-time avoidance)
3. Skill("design-iteration-loop") — Builder-Evaluator quality loop (max 5, pass_threshold 0.75, Sprint Contract, 4-dimension scoring)

(UX prompt pattern advisor available via Skill("design-prompt-builder").)
