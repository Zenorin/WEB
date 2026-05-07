# Project Source Integration Guide

Recommended repository placement:

```text
AGENTS.md
PLANS.md
.codex/config.toml
.codex/policy.lock.json
.agents/skills/*/SKILL.md
<module>/AGENTS.md
docs/skillset/*.md
```

After generation: review diff, fill real commands, run `validate-generated`, then commit profile and generated guidance together.
