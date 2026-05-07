---
name: "project-core-pipeline"
description: "Own deterministic core processing, pipeline state, and idempotent execution contracts."
---

# Project Core Pipeline

## Scope
- module_paths: `packages/core`
- objective: Own deterministic core processing, pipeline state, and idempotent execution contracts.

## Workflow
1. Separate pure core logic from IO.
2. Define retry/cancel/error behavior.
3. Add deterministic tests for core transformations.

## Quality gates
- Core package builds.
- Idempotency risks reviewed.

## Routing discipline
- Do not replace the root workflow skills; use this workstream as the project-specific owner for its module paths.
- Keep generated scaffold paths aligned with `module_paths` and module-local `AGENTS.md`.
- Do not move active policy-pack skills into optional/pruned output.

## Handoff
- Changed files, commands, evidence, risks, and next steps are summarized.
