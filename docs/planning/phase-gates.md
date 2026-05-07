# Phase Gates

| Phase | PASS condition | FAIL / blocker |
|---|---|---|
| intake | `python -S tools/codex/codex_skillset_generator.py validate-generated --root .` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| stack-decision | `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| bootstrap | `python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| reference-analysis | `pnpm cleanroom:audit` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, unapproved behavior deletion, or failure to document the clean-room reject list |
| renewal-prd | `python -S tools/codex/codex_skillset_generator.py validate-planning --root .` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| contracts | `pnpm --filter @project/contracts typecheck` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| backend-api | `cd apps/api && pytest` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| frontend-shell | `pnpm --filter web build` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| extension-bridge | `pnpm --filter extension build` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| collectors | `pnpm --filter @project/collectors typecheck` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| core-pipeline | `pnpm --filter @project/core typecheck` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| integration | `pnpm validate:all` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
| handoff | `python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |
