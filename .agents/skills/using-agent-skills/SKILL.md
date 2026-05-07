---
name: "using-agent-skills"
description: "Select the minimum relevant skills, modules, commands, references, and policy packs for the current task."
---

# Using Agent Skills

## Skill selection process
1. Classify the task phase: Define, Plan, Build, Verify, Review, or Ship.
2. Match the working path to a module using `recommend --path` when possible.
3. Use the smallest useful skill set: normally one workflow skill, one domain skill, and `$evidence-pack`.
4. Apply policy-pack skills only when the profile, module, docs, or user explicitly requires them.
5. Do not load every skill by default.

## Handoff
- Summarize changes, evidence, risks, and next steps.
- Cite relevant project docs or source files by path.
