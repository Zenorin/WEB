# WBS

| ID | Phase | Workstream | Module path | Task | Validation | Depends on |
|---|---|---|---|---|---|---|
| WBS-00 | intake | `$project-development-bootstrap` | `.` | Confirm repo state, domain/hosting boundary, and clean-room constraints | `python -S tools/codex/codex_skillset_generator.py validate-generated --root .` | - |
| WBS-01 | stack-decision | `$project-development-bootstrap` | `.` | Review selected stack and active/deferred module policy | `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` | WBS-00 |
| WBS-02 | bootstrap | `$project-development-bootstrap` | `.` | Validate generated repository scaffold | `python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .` | WBS-01 |
| WBS-03 | reference-analysis | `$project-reference-mapper` | `tools/reference-analysis` | Write clean-room webpage reference role report | `pnpm cleanroom:audit` | WBS-02 |
| WBS-04 | renewal-prd | `$project-development-bootstrap` | `.` | Write renewal PRD, IA route map, and component inventory | `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` | WBS-03 |
| WBS-05 | contracts | `$project-contracts` | `packages/contracts` | Define quote intake and operations status contracts | `pnpm --filter @project/contracts typecheck` | WBS-04 |
| WBS-06 | backend-api | `$project-backend-api` | `apps/api` | Implement API shell and quote intake envelope boundary | `cd apps/api && pytest` | WBS-05 |
| WBS-07 | frontend-shell | `$project-frontend-design` | `apps/web` | Implement renewal web shell and quote CTA state coverage after planning approval | `pnpm --filter web build` | WBS-06 |
| WBS-08 | extension-bridge | `$project-extension-bridge` | `apps/extension` | Keep extension boundary deferred unless URL analysis is separately approved | `pnpm --filter extension build` | WBS-07 |
| WBS-09 | collectors | `$project-market-collectors` | `packages/collectors` | Keep collector contract deferred and compliance-gated | `pnpm --filter @project/collectors typecheck` | WBS-08 |
| WBS-10 | core-pipeline | `$project-core-pipeline` | `packages/core` | Model China sourcing and Rocket Growth operations status flow | `pnpm --filter @project/core typecheck` | WBS-09 |
| WBS-11 | integration | `$project-development-bootstrap` | `.` | Connect PRD, contracts, API, web, and operations evidence | `pnpm validate:all` | WBS-10 |
| WBS-12 | handoff | `$evidence-pack` | `.` | Prepare evidence pack and next-session command | `python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .` | WBS-11 |
