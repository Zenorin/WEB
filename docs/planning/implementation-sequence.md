# Implementation Sequence

## WBS-00 — Confirm repo state, domain/hosting boundary, and clean-room constraints
- phase: `intake`
- workstream: `$project-development-bootstrap`
- module_path: `.`
- validation: `python -S tools/codex/codex_skillset_generator.py validate-generated --root .`

## WBS-01 — Review selected stack and active/deferred module policy
- phase: `stack-decision`
- workstream: `$project-development-bootstrap`
- module_path: `.`
- validation: `python -S tools/codex/codex_skillset_generator.py validate-planning --root .`

## WBS-02 — Validate generated repository scaffold
- phase: `bootstrap`
- workstream: `$project-development-bootstrap`
- module_path: `.`
- validation: `python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .`

## WBS-03 — Write clean-room webpage reference role report
- phase: `reference-analysis`
- workstream: `$project-reference-mapper`
- module_path: `tools/reference-analysis`
- validation: `pnpm cleanroom:audit`

## WBS-04 — Write renewal PRD, IA route map, and component inventory
- phase: `renewal-prd`
- workstream: `$project-development-bootstrap`
- module_path: `.`
- validation: `python -S tools/codex/codex_skillset_generator.py validate-planning --root .`

## WBS-05 — Define quote intake and operations status contracts
- phase: `contracts`
- workstream: `$project-contracts`
- module_path: `packages/contracts`
- validation: `pnpm --filter @project/contracts typecheck`

## WBS-06 — Implement API shell and quote intake envelope boundary
- phase: `backend-api`
- workstream: `$project-backend-api`
- module_path: `apps/api`
- validation: `cd apps/api && pytest`

## WBS-07 — Implement renewal web shell and quote CTA state coverage
- phase: `frontend-shell`
- workstream: `$project-frontend-design`
- module_path: `apps/web`
- validation: `pnpm --filter web build`

## WBS-08 — Keep extension boundary deferred unless URL analysis is separately approved
- phase: `extension-bridge`
- workstream: `$project-extension-bridge`
- module_path: `apps/extension`
- validation: `pnpm --filter extension build`

## WBS-09 — Keep collector contract deferred and compliance-gated
- phase: `collectors`
- workstream: `$project-market-collectors`
- module_path: `packages/collectors`
- validation: `pnpm --filter @project/collectors typecheck`

## WBS-10 — Model China sourcing and Rocket Growth operations status flow
- phase: `core-pipeline`
- workstream: `$project-core-pipeline`
- module_path: `packages/core`
- validation: `pnpm --filter @project/core typecheck`

## WBS-11 — Connect PRD, contracts, API, web, and operations evidence
- phase: `integration`
- workstream: `$project-development-bootstrap`
- module_path: `.`
- validation: `pnpm validate:all`

## WBS-12 — Prepare evidence pack and next-session command
- phase: `handoff`
- workstream: `$evidence-pack`
- module_path: `.`
- validation: `python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .`
