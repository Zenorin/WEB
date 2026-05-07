# AGENTS.md — NEEDS TRADE Web Renewal

## Purpose
Use this repository guidance with local `.agents/skills`, planning docs, module routing, and evidence gates.

## Development flow
1. Read `docs/product/PRD.md` and `docs/planning/WBS.md` when present.
2. Follow `docs/planning/codex-command-queue.md` by slice.
3. Use module-local `AGENTS.md` before editing a module path.
4. Validate generated guidance, scaffold, planning docs, and dev-flow ordering.

## Module routing
- `apps/web` → `frontend-product-ui`
  - workstreams: $project-frontend-design
  - generated skills: $project-frontend-design, $needs-trade-renewal-ui, $quote-intake-contract, $rocket-growth-inbound-flow, $design-system-consistency, $ui-state-coverage, $responsive-layout-review, $browser-smoke, $consistency-guard, $evidence-pack
  - optional/pruned: $frontend-product-ui, $accessibility-check, $form-table-filter-ux, $visual-regression-plan
- `apps/api` → `backend-api`
  - workstreams: $project-backend-api
  - generated skills: $project-backend-api, $quote-intake-contract, $api-contract-change, $authz-security-review, $consistency-guard, $evidence-pack
  - optional/pruned: $api-error-handling-review, $backend-test-matrix, $db-migration, $service-repository-boundary-check, $observability-update, $backward-compat-check, $incident-hotfix
- `apps/extension` → `browser-extension`
  - workstreams: $project-extension-bridge
  - generated skills: $project-extension-bridge, $privacy-boundary-review, $consistency-guard, $evidence-pack, $browser-smoke
  - optional/pruned: $extension-permission-review, $content-script-boundary, $message-contract-review
- `packages/contracts` → `shared-contracts`
  - workstreams: $project-contracts
  - generated skills: $project-contracts, $quote-intake-contract, $china-sourcing-ops-model, $rocket-growth-inbound-flow, $api-contract-change, $consistency-guard, $evidence-pack
  - optional/pruned: $backward-compat-check, $documentation-and-adrs
- `packages/core` → `data-pipeline`
  - workstreams: $project-core-pipeline
  - generated skills: $project-core-pipeline, $china-sourcing-ops-model, $rocket-growth-inbound-flow, $consistency-guard, $evidence-pack
  - optional/pruned: $schema-contract-check, $data-quality-gate, $idempotency-check, $observability-update, $backfill-rollout
- `packages/collectors` → `crawler-session`
  - workstreams: $project-market-collectors
  - generated skills: $project-market-collectors, $session-boundary-security, $consistency-guard, $evidence-pack, $privacy-boundary-review
  - optional/pruned: $crawler-contract-review, $anti-bot-compliance-check, $idempotency-check
- `tools/reference-analysis` → `clean-room-rebuild`
  - workstreams: $project-reference-mapper
  - generated skills: $project-reference-mapper, $webpage-reference-renewal, $clean-room-reference-analysis, $reference-role-report, $contract-extraction, $source-copy-audit, $consistency-guard, $evidence-pack

## Planning docs
- `docs/product/PRD.md`
- `docs/planning/WBS.md`
- `docs/planning/codex-command-queue.md`
- `docs/planning/phase-gates.md`

## Available project skills
- `$using-agent-skills`
- `$spec-driven-development`
- `$planning-and-task-breakdown`
- `$context-engineering`
- `$source-driven-development`
- `$incremental-implementation`
- `$test-driven-development`
- `$debugging-and-error-recovery`
- `$code-review-and-quality`
- `$security-and-hardening`
- `$consistency-guard`
- `$evidence-pack`
- `$clean-room-reference-analysis`
- `$reference-role-report`
- `$contract-extraction`
- `$source-copy-audit`
- `$no-feature-deletion-guard`
- `$pass-manifest-verification`
- `$characterization-tests`
- `$privacy-boundary-review`
- `$data-egress-review`
- `$needs-trade-web-renewal-intake`
- `$webpage-reference-renewal`
- `$needs-trade-renewal-ui`
- `$quote-intake-contract`
- `$china-sourcing-ops-model`
- `$rocket-growth-inbound-flow`
- `$design-system-consistency`
- `$ui-state-coverage`
- `$responsive-layout-review`
- `$browser-smoke`
- `$project-development-bootstrap`
- `$project-frontend-design`
- `$project-backend-api`
- `$project-contracts`
- `$project-core-pipeline`
- `$project-extension-bridge`
- `$project-market-collectors`
- `$project-reference-mapper`
- `$authz-security-review`
- `$session-boundary-security`
- `$api-contract-change`

## Done definition
Work is not done until changed files, validation evidence, risks, and next steps are summarized.
