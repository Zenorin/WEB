# Codex Command Queue

## Queue rule
Run slices in WBS order unless the business owner explicitly changes priority. Each slice must preserve clean-room constraints, avoid secrets, and report changed files, validation, risks, and rollback notes.

### WBS-00 — Repo intake and clean-room boundary

```text
Read AGENTS.md first.
Use $project-development-bootstrap $needs-trade-web-renewal-intake $evidence-pack.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- AGENTS.md
- README_NEEDS_TRADE_CODEX_SKILLSET.md
- docs/architecture/boundaries.md
- docs/product/PRD.md
- docs/planning/WBS.md
- docs/planning/codex-command-queue.md

Allowed changes:
- Confirm guidance, repo state, planning surface, and clean-room constraints.
- Update directly required planning evidence only.

Forbidden changes:
- Do not implement product code.
- Do not add secrets, credentials, cookies, sessions, API keys, or private tokens.
- Do not copy restricted reference source text/assets.
- Do not claim regulated or platform outcomes.

Validation commands:
- python -S tools/codex/codex_skillset_generator.py validate-generated --root .

Expected evidence:
- Files read
- Changed files, if any
- Commands run and PASS/FAIL results
- Remaining risks
- Rollback note
```

### WBS-01 — Stack and module policy decision

```text
Read AGENTS.md first.
Use $project-development-bootstrap $planning-and-task-breakdown $evidence-pack.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- docs/decisions/stack-decision.md
- codex-profile.json
- docs/planning/WBS.md

Allowed changes:
- Review selected stack and active/deferred module policy.
- Keep scaffold policy aligned with module routing.

Forbidden changes:
- Do not treat the scaffold as a finished product.
- Do not implement UI, API, extension, collector, or automation behavior.
- Do not add secrets or credentials.

Validation commands:
- python -S tools/codex/codex_skillset_generator.py validate-planning --root .

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Stack/module decision notes
- Rollback note
```

### WBS-02 — Scaffold validation

```text
Read AGENTS.md first.
Use $project-development-bootstrap $pass-manifest-verification $evidence-pack.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- package.json
- pnpm-workspace.yaml
- .codex/scaffold-manifest.json

Allowed changes:
- Validate generated repository scaffold and document blockers.
- Keep generated governance files intact.

Forbidden changes:
- Do not delete generated files or module-local AGENTS.md files.
- Do not implement product behavior in this slice.
- Do not add secrets or credentials.

Validation commands:
- python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Scaffold risks or blockers
- Rollback note
```

### WBS-03 — Clean-room webpage reference role report

```text
Read AGENTS.md first.
Use $project-reference-mapper $webpage-reference-renewal $clean-room-reference-analysis $source-copy-audit $evidence-pack.

Target workstream: project-reference-mapper
Target module path: tools/reference-analysis

Target files:
- docs/reference/webpage-reference-role-report.md

Allowed changes:
- Update only the reference role report and directly required planning evidence.
- Extract role, IA, service-flow, customer journey, evidence, and conversion-flow observations.

Forbidden changes:
- Do not implement UI/product code.
- Do not copy reference source, HTML, CSS, JavaScript, images, icons, slogans, exact marketing copy, tracking snippets, hidden text, cookies, sessions, or credentials.
- Do not claim guaranteed Coupang approval, customs clearance, KC certification, delivery date, or platform outcome.

Validation commands:
- node tools/checks/cleanroom-audit.mjs

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Observed facts vs inferred requirements
- Clean-room reject list
- Remaining open questions
- Rollback note
```

### WBS-04 — Renewal planning package

```text
Read AGENTS.md first.
Use $needs-trade-web-renewal-intake $webpage-reference-renewal $project-reference-mapper $clean-room-reference-analysis $source-copy-audit $evidence-pack.

Target workstream: project-reference-mapper
Target module path: tools/reference-analysis

Goal:
Create a stronger clean-room reference role report and renewal planning package for NEEDS TRADE as an integrated China sourcing, OEM/ODM, inspection, customs, warehouse, and Coupang Rocket Growth inbound operation platform.

Target files:
- docs/reference/webpage-reference-role-report.md
- docs/product/renewal-prd.md
- docs/design/ia-route-map.md
- docs/design/component-inventory.md
- docs/contracts/quote-intake-contract.md
- docs/operations/china-sourcing-ops-model.md
- docs/operations/rocket-growth-inbound-flow.md
- docs/planning/WBS.md
- docs/planning/codex-command-queue.md
- docs/planning/phase-gates.md

Allowed changes:
- Update only the target files and directly required planning evidence.
- Expand weak placeholder docs into actionable docs.
- Keep existing scaffold and validation scripts intact.

Forbidden changes:
- Do not implement UI/product code in this slice.
- Do not copy source code, HTML, CSS, JavaScript, images, icons, slogans, exact marketing copy, hidden text, tracking snippets, cookies, sessions, or credentials from reference sites.
- Do not delete existing behavior or generated governance files.
- Do not add real API keys, passwords, cookies, tokens, or private credentials.
- Do not make legal, customs, KC, or Coupang approval guarantees.

Validation commands:
- python -S tools/codex/codex_skillset_generator.py validate-planning --root .
- node tools/checks/cleanroom-audit.mjs

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Summary of observed facts vs inferred requirements
- Clean-room reject list
- Remaining open questions
- Rollback note
```

### WBS-05 — Shared quote intake contract implementation

```text
Read AGENTS.md first.
Use $project-contracts $quote-intake-contract $china-sourcing-ops-model $api-contract-change $evidence-pack.

Target workstream: project-contracts
Target module path: packages/contracts

Target files:
- packages/contracts/src/index.ts
- docs/contracts/quote-intake-contract.md

Allowed changes:
- Implement TypeScript DTOs/enums from the documented quote intake contract.
- Add compatibility notes if any field names change.

Forbidden changes:
- Do not implement API handlers, UI, extension, collectors, or 1688 automation.
- Do not introduce secrets or platform credentials.
- Do not encode guarantee statuses for Coupang, customs, KC, or delivery outcomes.

Validation commands:
- pnpm --filter @project/contracts typecheck

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Contract fields added/changed
- Compatibility risks
- Rollback note
```

### WBS-06 — Backend quote intake boundary

```text
Read AGENTS.md first.
Use $project-backend-api $quote-intake-contract $api-contract-change $authz-security-review $evidence-pack.

Target workstream: project-backend-api
Target module path: apps/api

Target files:
- apps/api/app/main.py
- apps/api/tests/test_health.py
- docs/contracts/api-contracts.md

Allowed changes:
- Implement minimal quote request create/read boundary and admin route placeholders.
- Validate required fields and safe error envelopes.

Forbidden changes:
- Do not persist marketplace credentials, cookies, sessions, API keys, passwords, or tokens.
- Do not implement file upload, payment, extension, collector, or marketplace crawling behavior.
- Do not expose internal operator notes to customer endpoints.

Validation commands:
- cd apps/api && pytest

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- API contract notes
- Security risks
- Rollback note
```

### WBS-07 — Renewal web shell

```text
Read AGENTS.md first.
Use $project-frontend-design $needs-trade-renewal-ui $quote-intake-contract $design-system-consistency $ui-state-coverage $responsive-layout-review $browser-smoke $evidence-pack.

Target workstream: project-frontend-design
Target module path: apps/web

Target files:
- apps/web/src/App.tsx
- apps/web/src/main.tsx

Allowed changes:
- Implement public route shell, service sections, quote CTA, customer workspace placeholder, and admin workspace placeholder.
- Use original NEEDS TRADE copy and approved/local assets only.

Forbidden changes:
- Do not copy reference site assets, text, layout code, icons, images, or snippets.
- Do not claim guaranteed Coupang approval, customs clearance, KC certification, or delivery outcomes.
- Do not implement extension, collectors, crawling, payment, or production auth.

Validation commands:
- pnpm --filter web build

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- UI state coverage
- Responsive/browser smoke notes
- Rollback note
```

### WBS-08 — Quote intake UI

```text
Read AGENTS.md first.
Use $project-frontend-design $quote-intake-contract $ui-state-coverage $responsive-layout-review $browser-smoke $evidence-pack.

Target workstream: project-frontend-design
Target module path: apps/web

Target files:
- apps/web/src/App.tsx

Allowed changes:
- Implement quote intake form states aligned with docs/contracts/quote-intake-contract.md.
- Keep file upload as a deferred placeholder unless storage/privacy work is approved.

Forbidden changes:
- Do not collect passwords, cookies, sessions, marketplace credentials, API keys, or private tokens.
- Do not submit to production endpoints unless configured in a later approved API slice.

Validation commands:
- pnpm --filter web build

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Form validation states
- Remaining API/storage gaps
- Rollback note
```

### WBS-09 — Operations status helpers

```text
Read AGENTS.md first.
Use $project-core-pipeline $china-sourcing-ops-model $rocket-growth-inbound-flow $consistency-guard $evidence-pack.

Target workstream: project-core-pipeline
Target module path: packages/core

Target files:
- packages/core/src/index.ts
- docs/operations/china-sourcing-ops-model.md
- docs/operations/rocket-growth-inbound-flow.md

Allowed changes:
- Implement deterministic status transition helpers and evidence requirements from operations docs.

Forbidden changes:
- Do not implement warehouse integrations, carrier integrations, customs/KC automation, or platform API calls.
- Do not encode platform/legal guarantees as statuses or success states.

Validation commands:
- pnpm --filter @project/core typecheck

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Status/evidence consistency notes
- Rollback note
```

### WBS-10 — Extension boundary remains deferred

```text
Read AGENTS.md first.
Use $project-extension-bridge $privacy-boundary-review $session-boundary-security $evidence-pack.

Target workstream: project-extension-bridge
Target module path: apps/extension

Target files:
- apps/extension/manifest.json
- docs/contracts/extension-message-contracts.md

Allowed changes:
- Document or preserve deferred extension boundary only if separately approved.

Forbidden changes:
- Do not add marketplace credentials, cookies, session capture, scraping permissions, or unapproved host permissions.
- Do not implement 1688/Coupang automation in this slice.

Validation commands:
- pnpm --filter extension build

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Permission/privacy notes
- Rollback note
```

### WBS-11 — Collector and 1688 automation remains deferred

```text
Read AGENTS.md first.
Use $project-market-collectors $session-boundary-security $privacy-boundary-review $source-copy-audit $evidence-pack.

Target workstream: project-market-collectors
Target module path: packages/collectors

Target files:
- packages/collectors/src/index.ts
- tools/checks/clean-room-audit-notes.md

Allowed changes:
- Preserve collector boundary or document deferred compliance gate only if separately approved.

Forbidden changes:
- Do not implement unauthorized crawling, scraping, credential/session reuse, marketplace login, or 1688 automation.
- Do not copy reference source or selector structures.

Validation commands:
- pnpm --filter @project/collectors typecheck

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Compliance/session-boundary notes
- Rollback note
```

### WBS-12 — Integration alignment

```text
Read AGENTS.md first.
Use $planning-and-task-breakdown $consistency-guard $evidence-pack.

Target workstream: project-development-bootstrap
Target module path: .

Target files:
- docs/planning/phase-gates.md
- docs/planning/codex-command-queue.md

Allowed changes:
- Align planning docs, validation commands, risks, and next-session command.

Forbidden changes:
- Do not hide failed validations or unresolved scope risks.
- Do not delete generated governance files.

Validation commands:
- pnpm validate:all

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Cross-doc consistency notes
- Remaining risks and blockers
- Rollback note
```

### WBS-13 — Evidence handoff and next command

```text
Read AGENTS.md first.
Use $evidence-pack $pass-manifest-verification.

Target workstream: evidence-pack
Target module path: .

Target files:
- docs/planning/codex-command-queue.md
- docs/planning/needs-trade-next-codex-commands.md

Allowed changes:
- Prepare changed-files evidence, validation results, risks, rollback note, and next-session command.

Forbidden changes:
- Do not hide failed validations or unresolved scope risks.
- Do not delete generated governance files.

Validation commands:
- python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks and blockers
- Rollback note
```
