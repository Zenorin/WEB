---
name: "needs-trade-web-renewal-intake"
description: "Plan the NEEDS TRADE renewal before implementation: scope, PRD, IA, WBS, service catalog, and conversion flow."
---

# NEEDS TRADE Web Renewal Intake

## Use when
- Starting or revising the NEEDS TRADE website renewal.
- Turning business notes into PRD, requirements, IA, route map, phase gates, WBS, or Codex command queue.
- Deciding whether a feature is active-now, deferred-with-contract, or out-of-scope.

## Required workflow
1. Classify the task as planning, reference-analysis, implementation, validation, or handoff.
2. Write goals, non-goals, target users, service catalog, conversion CTAs, and workspace/admin scope.
3. Separate confirmed capabilities from planned capabilities and assumptions.
4. Map each feature to one module path and one workstream.
5. Produce or update PRD, requirements, IA/route map, component inventory, WBS, and command queue before implementation.
6. Keep the first implementation slice narrow: main shell, service routes, or quote intake.

## Output contract
- `docs/product/PRD.md` or `docs/product/renewal-prd.md`
- `docs/product/requirements.md`
- `docs/design/ia-route-map.md`
- `docs/design/component-inventory.md`
- `docs/planning/WBS.md`
- `docs/planning/codex-command-queue.md`

## Red flags
- Treating the current minimal GitHub repo as a finished codebase without checking files.
- Replacing planning with UI implementation.
- Claiming Rocket Growth, customs, KC, or origin work without explicit responsibility boundaries.
- Putting hosting, domain, API, login, cookie, token, or customer data into generated docs.

## Handoff
- Report changed files, commands run, PASS/FAIL results, remaining risks, rollback note, and personal input needs.
- Cite project paths, not copied reference content.
