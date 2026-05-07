---
name: "webpage-reference-renewal"
description: "Extract clean-room website renewal roles from reference pages without copying implementation, assets, or exact copy."
---

# Webpage Reference Renewal

## Use when
- Reviewing `needstrade.com`, competitor pages, or reference pages for renewal planning.
- Building a clean-room role report before UI implementation.
- Comparing IA, CTA flow, service taxonomy, trust elements, pricing/fee presentation, and customer journey.

## Required workflow
1. Record each reference URL, access time, and what was observable.
2. Extract only role-level information: section purpose, navigation group, CTA intent, user flow, evidence type, and service taxonomy.
3. Do not copy HTML, CSS, JS, image assets, icons, logos, slogans, exact marketing text, tracking snippets, hidden text, cookies, session values, or class names.
4. Convert observations into a new NEEDS TRADE-specific structure.
5. Put all copied/prohibited items into a reject list.
6. Produce implementation-neutral requirements and component candidates.

## Output contract
`docs/reference/webpage-reference-role-report.md` with reference inventory, observable IA/CTA map, service taxonomy, customer journey observations, prohibited-copy reject list, renewal decisions, and open assumptions.

## Acceptance criteria
- Reference facts, assumptions, and decisions are separated.
- Every implementation suggestion is rephrased as original NEEDS TRADE behavior.
- No exact copy, asset, source, hidden value, or tracking snippet is reused.

## Handoff
- Report changed files, commands run, PASS/FAIL results, remaining risks, rollback note, and personal input needs.
- Cite project paths, not copied reference content.
