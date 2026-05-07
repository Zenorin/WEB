---
name: "no-feature-deletion-guard"
description: "Prevent deletion/hiding of behavior without role trace, replacement, migration, or approval."
---

# No Feature Deletion Guard

## Deletion gate
Before deleting, hiding, disabling, or replacing any UI option, fallback, debug/mock path, or legacy behavior:
1. Trace usage or role.
2. Identify replacement or migration.
3. Add/adjust tests when behavior matters.
4. Obtain explicit approval or document the deprecation path.

## Handoff
- Summarize changes, evidence, risks, and next steps.
- Cite relevant project docs or source files by path.
