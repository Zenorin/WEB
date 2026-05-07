# Codex Command Queue

### WBS-00 — Confirm repo state, domain/hosting boundary, and clean-room constraints

```text
Read AGENTS.md first.
Use $project-development-bootstrap $needs-trade-web-renewal-intake $evidence-pack.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- `AGENTS.md`
- `README_NEEDS_TRADE_CODEX_SKILLSET.md`
- `docs/architecture/boundaries.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `python -S tools/codex/codex_skillset_generator.py validate-generated --root .`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-01 — Review selected stack and active/deferred module policy

```text
Read AGENTS.md first.
Use $project-development-bootstrap $planning-and-task-breakdown.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- `docs/decisions/stack-decision.md`
- `codex-profile.json`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `python -S tools.codex/codex_skillset_generator.py validate-planning --root .`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-02 — Validate generated repository scaffold

```text
Read AGENTS.md first.
Use $project-development-bootstrap $pass-manifest-verification.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- `package.json`
- `pnpm-workspace.yaml`
- `.codex/scaffold-manifest.json`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-03 — Write clean-room webpage reference role report

```text
Read AGENTS.md first.
Use $project-reference-mapper $webpage-reference-renewal $clean-room-reference-analysis $source-copy-audit.

Target workstream: project-reference-mapper
Target module path: tools/reference-analysis

Target files:
- `docs/reference/webpage-reference-role-report.md`
- `tools/reference-analysis/src/index.ts`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `pnpm cleanroom:audit`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-04 — Write renewal PRD, IA route map, and component inventory

```text
Read AGENTS.md first.
Use $needs-trade-web-renewal-intake $spec-driven-development $planning-and-task-breakdown.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- `docs/product/renewal-prd.md`
- `docs/design/ia-route-map.md`
- `docs/design/component-inventory.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `python -S tools/codex/codex_skillset_generator.py validate-planning --root .`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-05 — Define quote intake and operations status contracts

```text
Read AGENTS.md first.
Use $project-contracts $quote-intake-contract $china-sourcing-ops-model $api-contract-change.

Target workstream: project-contracts
Target module path: packages/contracts

Target files:
- `packages/contracts/src/index.ts`
- `docs/contracts/quote-intake-contract.md`
- `docs/contracts/api-contracts.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `pnpm --filter @project/contracts typecheck`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-06 — Implement API shell and quote intake envelope boundary

```text
Read AGENTS.md first.
Use $project-backend-api $quote-intake-contract $api-contract-change.

Target workstream: project-backend-api
Target module path: apps/api

Target files:
- `apps/api/app/main.py`
- `apps/api/tests/test_health.py`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `cd apps/api && pytest`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-07 — Implement renewal web shell and quote CTA state coverage

```text
Read AGENTS.md first.
Use $project-frontend-design $needs-trade-renewal-ui $ui-state-coverage $responsive-layout-review $browser-smoke.

Target workstream: project-frontend-design
Target module path: apps/web

Target files:
- `apps/web/src/App.tsx`
- `apps/web/src/main.tsx`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `pnpm --filter web build`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-08 — Keep extension boundary deferred unless URL analysis is separately approved

```text
Read AGENTS.md first.
Use $project-extension-bridge $privacy-boundary-review.

Target workstream: project-extension-bridge
Target module path: apps/extension

Target files:
- `apps/extension/manifest.json`
- `docs/contracts/extension-message-contracts.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `pnpm --filter extension build`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-09 — Keep collector contract deferred and compliance-gated

```text
Read AGENTS.md first.
Use $project-market-collectors $session-boundary-security $source-copy-audit.

Target workstream: project-market-collectors
Target module path: packages/collectors

Target files:
- `packages/collectors/src/index.ts`
- `tools/checks/clean-room-audit-notes.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `pnpm --filter @project/collectors typecheck`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-10 — Model China sourcing and Rocket Growth operations status flow

```text
Read AGENTS.md first.
Use $project-core-pipeline $china-sourcing-ops-model $rocket-growth-inbound-flow.

Target workstream: project-core-pipeline
Target module path: packages/core

Target files:
- `packages/core/src/index.ts`
- `docs/operations/china-sourcing-ops-model.md`
- `docs/operations/rocket-growth-inbound-flow.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `pnpm --filter @project/core typecheck`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-11 — Connect PRD, contracts, API, web, and operations evidence

```text
Read AGENTS.md first.
Use $planning-and-task-breakdown $quote-intake-contract $evidence-pack.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- `docs/planning/phase-gates.md`
- `docs/planning/codex-command-queue.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `pnpm validate:all`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```

### WBS-12 — Prepare evidence pack and next-session command

```text
Read AGENTS.md first.
Use $evidence-pack $pass-manifest-verification.

Target workstream: evidence-pack
Target module path: .

Target files:
- `PLANS.md`
- `docs/planning/codex-command-queue.md`
- `docs/planning/needs-trade-next-codex-commands.md`

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.
- Do not claim regulated or platform-specific responsibility unless explicitly documented.

Validation commands:
- `python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .`

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: Revert this slice and restore prior generated files/backups if validation fails.
```
