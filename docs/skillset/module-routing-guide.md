# Module Routing Guide

Use module-local AGENTS.md files to route Codex work by path. This guide lists generated route skills, optional/pruned skills, and project-specific workstreams.

## web — `apps/web`
- type: `frontend-product-ui`
- workstreams: $project-frontend-design
- generated skills: $project-frontend-design, $needs-trade-renewal-ui, $quote-intake-contract, $rocket-growth-inbound-flow, $design-system-consistency, $ui-state-coverage, $responsive-layout-review, $browser-smoke, $consistency-guard, $evidence-pack
- optional/pruned: $frontend-product-ui, $accessibility-check, $form-table-filter-ux, $visual-regression-plan

## api — `apps/api`
- type: `backend-api`
- workstreams: $project-backend-api
- generated skills: $project-backend-api, $quote-intake-contract, $api-contract-change, $authz-security-review, $consistency-guard, $evidence-pack
- optional/pruned: $api-error-handling-review, $backend-test-matrix, $db-migration, $service-repository-boundary-check, $observability-update, $backward-compat-check, $incident-hotfix

## extension — `apps/extension`
- type: `browser-extension`
- workstreams: $project-extension-bridge
- generated skills: $project-extension-bridge, $privacy-boundary-review, $consistency-guard, $evidence-pack, $browser-smoke
- optional/pruned: $extension-permission-review, $content-script-boundary, $message-contract-review

## contracts — `packages/contracts`
- type: `shared-contracts`
- workstreams: $project-contracts
- generated skills: $project-contracts, $quote-intake-contract, $china-sourcing-ops-model, $rocket-growth-inbound-flow, $api-contract-change, $consistency-guard, $evidence-pack
- optional/pruned: $backward-compat-check, $documentation-and-adrs

## core — `packages/core`
- type: `data-pipeline`
- workstreams: $project-core-pipeline
- generated skills: $project-core-pipeline, $china-sourcing-ops-model, $rocket-growth-inbound-flow, $consistency-guard, $evidence-pack
- optional/pruned: $schema-contract-check, $data-quality-gate, $idempotency-check, $observability-update, $backfill-rollout

## collectors — `packages/collectors`
- type: `crawler-session`
- workstreams: $project-market-collectors
- generated skills: $project-market-collectors, $session-boundary-security, $consistency-guard, $evidence-pack, $privacy-boundary-review
- optional/pruned: $crawler-contract-review, $anti-bot-compliance-check, $idempotency-check

## reference-analysis — `tools/reference-analysis`
- type: `clean-room-rebuild`
- workstreams: $project-reference-mapper
- generated skills: $project-reference-mapper, $webpage-reference-renewal, $clean-room-reference-analysis, $reference-role-report, $contract-extraction, $source-copy-audit, $consistency-guard, $evidence-pack
- optional/pruned: none
