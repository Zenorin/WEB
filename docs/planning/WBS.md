# WBS

## Planning rule
This WBS keeps the first implementation target narrow: web renewal, quote/request intake, customer workspace boundary, and admin workspace boundary. Extension, collectors, 1688 automation, payments, and production storage remain deferred unless a later approved slice changes scope.

| ID | Phase | Workstream | Module path | Task | Validation | Depends on |
|---|---|---|---|---|---|---|
| WBS-00 | intake | `$project-development-bootstrap` | `.` | Confirm repo state, domain/hosting boundary, clean-room constraints, and owner assumptions | `python -S tools/codex/codex_skillset_generator.py validate-generated --root .` | - |
| WBS-01 | stack-decision | `$project-development-bootstrap` | `.` | Review selected stack, active/deferred module policy, and scaffold generation boundary | `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` | WBS-00 |
| WBS-02 | bootstrap | `$project-development-bootstrap` | `.` | Validate generated repository scaffold without changing product behavior | `python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .` | WBS-01 |
| WBS-03 | reference-analysis | `$project-reference-mapper` | `tools/reference-analysis` | Produce clean-room webpage reference role report and reject list for NEEDS TRADE renewal | `node tools/checks/cleanroom-audit.mjs` | WBS-02 |
| WBS-04 | renewal-planning | `$needs-trade-web-renewal-intake` | `.` | Expand renewal PRD, IA/route map, component inventory, operations models, quote contract, phase gates, and command queue | `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` | WBS-03 |
| WBS-05 | contracts | `$project-contracts` | `packages/contracts` | Implement shared quote intake/status DTOs from `docs/contracts/quote-intake-contract.md` | `pnpm --filter @project/contracts typecheck` | WBS-04 |
| WBS-06 | backend-api | `$project-backend-api` | `apps/api` | Implement API shell for quote request create/read and admin status boundary | `cd apps/api && pytest` | WBS-05 |
| WBS-07 | frontend-shell | `$project-frontend-design` | `apps/web` | Implement public renewal web shell, quote CTA, service routes, and workspace/admin placeholders | `pnpm --filter web build` | WBS-06 |
| WBS-08 | frontend-intake | `$project-frontend-design` | `apps/web` | Implement quote intake form states against shared contract | `pnpm --filter web build` | WBS-07 |
| WBS-09 | operations-core | `$project-core-pipeline` | `packages/core` | Implement deterministic status transition helpers for sourcing and Rocket Growth preparation | `pnpm --filter @project/core typecheck` | WBS-08 |
| WBS-10 | extension-boundary | `$project-extension-bridge` | `apps/extension` | Keep extension bridge deferred; document permission/message boundary only if separately approved | `pnpm --filter extension build` | WBS-09 |
| WBS-11 | collector-boundary | `$project-market-collectors` | `packages/collectors` | Keep collectors/1688 automation deferred; document compliance gate only if separately approved | `pnpm --filter @project/collectors typecheck` | WBS-10 |
| WBS-12 | integration | `$project-development-bootstrap` | `.` | Connect PRD, IA, contracts, API, web, operations, and evidence pack | `pnpm validate:all` | WBS-11 |
| WBS-13 | handoff | `$evidence-pack` | `.` | Prepare changed-files evidence, validation results, risks, rollback note, and next-session command | `python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .` | WBS-12 |

## Current slice acceptance
- `docs/reference/webpage-reference-role-report.md` separates observed facts, inferred requirements, decisions, reject list, and open questions.
- `docs/product/renewal-prd.md` defines goals, non-goals, users, confirmed/planned capabilities, service catalog, journeys, and first implementation target.
- `docs/design/ia-route-map.md` and `docs/design/component-inventory.md` define public, customer, and admin boundaries.
- `docs/contracts/quote-intake-contract.md` defines request fields, statuses, validation, security, and API planning boundary.
- `docs/operations/china-sourcing-ops-model.md` and `docs/operations/rocket-growth-inbound-flow.md` avoid guarantee claims and define evidence.
- `docs/planning/codex-command-queue.md` and `docs/planning/phase-gates.md` keep deferred automation guarded.
