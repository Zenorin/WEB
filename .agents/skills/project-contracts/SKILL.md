---
name: "project-contracts"
description: "Own shared DTO/schema/event contracts and compatibility notes."
---

# Project Contracts

## Scope
- module_paths: `packages/contracts`
- objective: Own shared DTO/schema/event contracts and compatibility notes.

## Workflow
1. Define stable public shapes.
2. Check downstream impact before changing fields.
3. Document migrations for breaking changes.

## Quality gates
- Contract package builds.
- Breaking changes include migration notes.

## Routing discipline
- Do not replace the root workflow skills; use this workstream as the project-specific owner for its module paths.
- Keep generated scaffold paths aligned with `module_paths` and module-local `AGENTS.md`.
- Do not move active policy-pack skills into optional/pruned output.

## Handoff
- Changed files, commands, evidence, risks, and next steps are summarized.
