---
description: www 온라인 문서(Hugo/Geekdoc) 작성·동기화·감사 하네스 — 멀티모달(mermaid/SVG/Higgsfield) + 한국어 윤문
argument-hint: "[자연어 요청 또는 대상]"
allowed-tools: Skill
---

# /harness:www-docs

moai-cowork 공식 사이트(claude.mo.ai.kr)의 www 온라인 문서를 작성·전파·감사하는 하네스.

**Runner**: `hns-www-docs-run.js` · **manifest**: `.claude/commands/harness/www-docs/manifest.json`

## 라우팅 (자연어 → specialist)

- 새 문서 작성 · 가이드/쿡북/릴리스 노트 → **writer → polish → audit**
- 플러그인/스킬/에이전트 추가·업데이트·삭제 → **sync** (문서 전파)
- 기존 문서 품질 점검(DS 규칙·대비·빌드) → **audit**

자연어 요청을 Runner가 적절한 specialist로 분배한다.
