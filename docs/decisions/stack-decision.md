# Stack Decision

This file is generated from `codex-profile.json`. It must be reviewed before scaffolded code is treated as the active development baseline.

## Decision mode
- stack_selection_mode: `decision-first`
- stack_decision_required: `True`
- scaffold_generation_policy: `blocked_until_stack_selected`

## Selected stack
- frontend: `react-vite-typescript`
- api: `fastapi-python`
- extension: `chrome-mv3-typescript`
- package_manager: `pnpm`

## Decision reason
Selected React/Vite/TypeScript, FastAPI, Chrome MV3 placeholder, and pnpm workspace from the v4.9.5 web-clean-room preset. For this renewal, web/API/contracts/reference-analysis are active first; extension/collectors/core remain contract/deferred unless URL analysis or collection is approved later.

## Candidate stacks
- `react-vite-fastapi`: frontend=`react-vite-typescript`, api=`fastapi-python`, extension=`chrome-mv3-typescript`, package_manager=`pnpm` — Default for clean-room web plus local Python API prototyping.
- `react-vite-fastify`: frontend=`react-vite-typescript`, api=`fastify-typescript`, extension=`chrome-mv3-typescript`, package_manager=`pnpm` — Use when a single TypeScript runtime is preferred.

## Gate
Scaffold is approved only when `selected_stack` is present, matches `runtime_stack` and `package_manager`, and this decision file is present in `docs/decisions/stack-decision.md`.
