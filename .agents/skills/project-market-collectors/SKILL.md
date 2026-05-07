---
name: "project-market-collectors"
description: "Own collector contracts, selector fallbacks, session boundaries, and compliance checks."
---

# Project Market Collectors

## Scope
- module_paths: `packages/collectors`
- objective: Own collector contracts, selector fallbacks, session boundaries, and compliance checks.

## Workflow
1. Define allowed inputs/outputs/errors.
2. Avoid brittle selector-only assumptions.
3. Respect session/access-control boundaries.

## Quality gates
- Collector output schema is stable.
- Anti-bot and session boundaries reviewed.

## Routing discipline
- Do not replace the root workflow skills; use this workstream as the project-specific owner for its module paths.
- Keep generated scaffold paths aligned with `module_paths` and module-local `AGENTS.md`.
- Do not move active policy-pack skills into optional/pruned output.

## Handoff
- Changed files, commands, evidence, risks, and next steps are summarized.
