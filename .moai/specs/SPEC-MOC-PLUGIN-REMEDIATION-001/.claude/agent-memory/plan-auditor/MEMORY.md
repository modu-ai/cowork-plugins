# Memory Index

- [www link-integrity gap](project_www_link_integrity_gap.md) — www Hugo site has NO broken-link checker; "0 broken links" ACs are mechanically unsupported (no refLinksErrorLevel, no ref/relref, check-docs-health.mjs is not a link checker + mis-pathed, no htmltest)
- [Mechanical AC false-PASS check](feedback_mechanical_ac_false_pass_check.md) — run every ≥1 addition-predicate against HEAD before scoring; if it already passes, the AC cannot verify its REQ
- [REMEDIATION-001 verdict](project_remediation_001_verdict.md) — iter2 FAIL 0.74 + STOP (regression vs iter1 0.83); 5 flagged ACs fixed but same false-pass class survives in AC-003/019/020/021 + 001c/014-wiring
