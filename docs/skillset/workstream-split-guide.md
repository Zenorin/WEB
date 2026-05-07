# Workstream Split Guide

Project-specific workstreams are first-class skills. They do not replace universal workflow or policy-pack skills; they route actual repo paths to the correct development owner.

## $project-development-bootstrap — Project Development Bootstrap
- module_paths: `.`
- objective: Create and validate the repo bootstrap, workspace, env template, and shared build scripts without overriding workstream routing.
- quality_gates:
  - Root package/workspace files exist.
  - No secret values are committed.
  - validate-scaffold passes.

## $project-frontend-design — Project Frontend Design
- module_paths: `apps/web`
- objective: Own UI composition, screen states, responsive layout, and browser smoke checks for the web app.
- quality_gates:
  - Web build or blocker evidence exists.
  - Loading/empty/error/success states are covered.

## $project-backend-api — Project Backend API
- module_paths: `apps/api`
- objective: Own API entrypoints, error envelopes, persistence boundary, authz, and backend test matrix.
- quality_gates:
  - Health route exists.
  - API contract changes have tests or explicit evidence.

## $project-contracts — Project Contracts
- module_paths: `packages/contracts`
- objective: Own shared DTO/schema/event contracts and compatibility notes.
- quality_gates:
  - Contract package builds.
  - Breaking changes include migration notes.

## $project-core-pipeline — Project Core Pipeline
- module_paths: `packages/core`
- objective: Own deterministic core processing, pipeline state, and idempotent execution contracts.
- quality_gates:
  - Core package builds.
  - Idempotency risks reviewed.

## $project-extension-bridge — Project Extension Bridge
- module_paths: `apps/extension`
- objective: Own extension permissions, message contracts, content/background boundaries, and privacy review.
- quality_gates:
  - Manifest permissions are justified.
  - Message contract is documented.

## $project-market-collectors — Project Market Collectors
- module_paths: `packages/collectors`
- objective: Own collector contracts, selector fallbacks, session boundaries, and compliance checks.
- quality_gates:
  - Collector output schema is stable.
  - Anti-bot and session boundaries reviewed.

## $project-reference-mapper — Project Reference Mapper
- module_paths: `tools/reference-analysis`
- objective: Own clean-room reference role reports, contract extraction, and source-copy audit evidence.
- quality_gates:
  - Role report exists.
  - Source-copy audit passes.
