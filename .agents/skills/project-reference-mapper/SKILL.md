---
name: "project-reference-mapper"
description: "Own clean-room reference role reports, contract extraction, and source-copy audit evidence."
---

# Project Reference Mapper

## Scope
- module_paths: `tools/reference-analysis`
- objective: Own clean-room reference role reports, contract extraction, and source-copy audit evidence.

## Workflow
1. Treat reference files as read-only.
2. Extract roles/contracts without copying implementation.
3. Write role reports before excluding observed behavior.

## Quality gates
- Role report exists.
- Source-copy audit passes.

## Routing discipline
- Do not replace the root workflow skills; use this workstream as the project-specific owner for its module paths.
- Keep generated scaffold paths aligned with `module_paths` and module-local `AGENTS.md`.
- Do not move active policy-pack skills into optional/pruned output.

## Handoff
- Changed files, commands, evidence, risks, and next steps are summarized.
