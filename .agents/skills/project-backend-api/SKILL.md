---
name: "project-backend-api"
description: "Own API entrypoints, error envelopes, persistence boundary, authz, and backend test matrix."
---

# Project Backend API

## Scope
- module_paths: `apps/api`
- objective: Own API entrypoints, error envelopes, persistence boundary, authz, and backend test matrix.

## Workflow
1. Define request/response/error contracts.
2. Keep handler/service/repository responsibilities separated.
3. Run backend tests or document blockers.

## Quality gates
- Health route exists.
- API contract changes have tests or explicit evidence.

## Routing discipline
- Do not replace the root workflow skills; use this workstream as the project-specific owner for its module paths.
- Keep generated scaffold paths aligned with `module_paths` and module-local `AGENTS.md`.
- Do not move active policy-pack skills into optional/pruned output.

## Handoff
- Changed files, commands, evidence, risks, and next steps are summarized.
