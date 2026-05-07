---
name: "project-extension-bridge"
description: "Own extension permissions, message contracts, content/background boundaries, and privacy review."
---

# Project Extension Bridge

## Scope
- module_paths: `apps/extension`
- objective: Own extension permissions, message contracts, content/background boundaries, and privacy review.

## Workflow
1. Minimize manifest permissions.
2. Define message payload/reply/error shapes.
3. Keep content scripts separated from privileged background logic.

## Quality gates
- Manifest permissions are justified.
- Message contract is documented.

## Routing discipline
- Do not replace the root workflow skills; use this workstream as the project-specific owner for its module paths.
- Keep generated scaffold paths aligned with `module_paths` and module-local `AGENTS.md`.
- Do not move active policy-pack skills into optional/pruned output.

## Handoff
- Changed files, commands, evidence, risks, and next steps are summarized.
