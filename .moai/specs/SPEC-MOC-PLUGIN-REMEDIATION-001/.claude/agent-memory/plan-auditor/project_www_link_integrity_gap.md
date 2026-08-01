---
name: www-link-integrity-gap
description: www Hugo site has NO working broken-internal-link checker — audit any www content/IA SPEC whose AC claims "0 broken links" as a testability defect
metadata:
  type: project
---

The `www/` Hugo site (theme hugo-geekdoc) has NO mechanical broken-internal-link verification available. Any SPEC AC asserting "broken internal link 0" is mechanically unsupported as written.

**Why:** Verified 2026-07-02 during SPEC-MOC-SITE-IA-001 plan-audit:
- `hugo.toml` sets no `refLinksErrorLevel` → `hugo --gc --minify` exits 0 even with broken internal markdown links.
- `www/content` uses ZERO `ref`/`relref` shortcodes → Hugo has nothing to build-time-validate; all internal links are plain `[x](/path)` which Hugo never checks.
- `www/scripts/check-docs-health.mjs` is NOT a link checker (it checks skill/plugin counts + stale-count/fal.ai text residue) AND is mis-pathed for this repo (resolves CONTENT to `<root>/docs-site/content` which does not exist; correct tree is `www/content`).
- No `htmltest`/lychee config exists.

**How to apply:** When auditing a www content/IA SPEC, treat any "hugo build exit 0 ⇒ 0 broken links" equivalence as FALSE. Flag AC's link-integrity claim as a testability defect unless the SPEC adds a real link-check tool (htmltest/lychee/custom script) OR sets refLinksErrorLevel=ERROR AND converts internal links to relref. Also: alias-completeness AC's using `grep -rl '^aliases:' ... | wc -l ≥ 1` are too weak to verify "every removed path has an alias" — one alias passes while dozens 404. Note: interactive shell aliases `ls` to `ls -la` here, so `ls | grep '^name'` pipelines fail — use `find`/`ls -1` for counts.
