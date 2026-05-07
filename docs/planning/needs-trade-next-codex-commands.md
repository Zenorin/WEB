# NEEDS TRADE Next Codex Commands

```text
Read AGENTS.md first.
Use $needs-trade-web-renewal-intake $webpage-reference-renewal $project-reference-mapper $evidence-pack.

Target workstream: project-reference-mapper
Target module path: tools/reference-analysis

Goal:
Create a clean-room reference role report and renewal PRD for NEEDS TRADE using the existing site and reference pages only as role/IA/service-flow references.

Target files:
- docs/reference/webpage-reference-role-report.md
- docs/product/renewal-prd.md
- docs/design/ia-route-map.md
- docs/design/component-inventory.md
- docs/planning/WBS.md
- docs/planning/codex-command-queue.md

Forbidden changes:
- Do not copy reference source, assets, images, icons, slogans, exact marketing copy, hidden text, tracking snippets, cookies, sessions, or credentials.
- Do not implement UI code in this slice.
- Do not delete existing behavior.

Validation commands:
- python -S tools/codex/codex_skillset_generator.py validate-planning --root .
- node tools/checks/cleanroom-audit.mjs

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Assumptions and blockers
- Rollback note
```
