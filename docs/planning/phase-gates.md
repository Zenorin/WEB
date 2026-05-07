# Phase Gates

## Gate rule
Each phase must document changed files, validation result, clean-room/security risks, and rollback note before handoff. A command failure can be accepted only when the blocker and next step are explicit.

| Phase | PASS condition | FAIL / blocker |
|---|---|---|
| intake | Repo guidance, root/module `AGENTS.md`, PRD/WBS/queue, clean-room constraints, and owner assumptions are reviewed. `python -S tools/codex/codex_skillset_generator.py validate-generated --root .` passes or blocker is documented. | Missing guidance review, secret exposure, path mismatch, unapproved behavior deletion, or unclear renewal boundary. |
| stack-decision | Stack and active/deferred module policy are documented. `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` passes or blocker is documented. | Scaffold treated as finished product, missing planning docs, or stack mismatch. |
| bootstrap | Generated scaffold validates without product implementation drift. `python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .` passes or blocker is documented. | Missing scaffold files, generated governance deletion, or secret-like value. |
| reference-analysis | Clean-room role report exists with reference inventory, observed facts, inferred requirements, reject list, decisions, and open questions. `node tools/checks/cleanroom-audit.mjs` passes. | Copied source/copy/assets, missing reject list, unsupported platform/legal claims, or failed audit. |
| renewal-planning | Renewal PRD, IA, component inventory, quote contract, operations models, WBS, queue, and phase gates are aligned. `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` passes. | Planning docs disagree on scope, Rocket Growth guarantee claims appear, or extension/collector automation is unguarded. |
| contracts | Shared DTO/status contract matches quote-intake docs and operations lifecycle. `pnpm --filter @project/contracts typecheck` passes. | Breaking contract without migration note, missing status, or customer/admin field leakage. |
| backend-api | API shell validates create/read/admin boundaries and avoids credentials. `cd apps/api && pytest` passes. | Missing validation, unsafe field persistence, unauthenticated admin path, or secret handling. |
| frontend-shell | Public web shell and workspace/admin placeholders build with required states. `pnpm --filter web build` passes. | Missing responsive/state coverage, unsupported claims, copied assets/copy, or hidden admin/customer boundary. |
| frontend-intake | Quote intake UI matches contract and validates required fields. `pnpm --filter web build` passes. | Form collects credentials, required fields mismatch contract, or error/success states are absent. |
| operations-core | Status transition helpers match operations docs. `pnpm --filter @project/core typecheck` passes. | Invalid transition behavior, unsupported guarantee encoded as status, or missing blocker/cancel path. |
| extension-boundary | Extension remains deferred or has approved permission/message/privacy evidence. `pnpm --filter extension build` passes if touched. | Unapproved permissions, session/cookie capture, or marketplace automation claim. |
| collector-boundary | Collectors/1688 automation remain deferred or have approved compliance/session boundary evidence. `pnpm --filter @project/collectors typecheck` passes if touched. | Unauthorized crawling, credential/session reuse, brittle source-copy, or anti-bot boundary gap. |
| integration | PRD, contracts, API, web, operations, and evidence pack agree. `pnpm validate:all` passes or blocker is documented. | Cross-doc mismatch, validation gap, or unreviewed risk. |
| handoff | Evidence pack lists changed files, commands, PASS/FAIL, observed facts vs inferred requirements, reject list, open questions, risks, next steps, and rollback note. `python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .` passes or blocker is documented. | Missing evidence, vague rollback, or open blockers hidden. |

## Non-negotiable blockers
- Real credentials, API keys, cookies, sessions, passwords, or tokens appear in committed docs/code.
- Reference source code, exact marketing copy, images, icons, slogans, tracking snippets, or hidden text are reused.
- Docs or product surfaces claim guaranteed Coupang approval, customs clearance, KC certification, delivery date, or platform outcome.
- Extension, collectors, or automated 1688 crawling are implemented without separate approval.
