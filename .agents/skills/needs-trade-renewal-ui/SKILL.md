---
name: "needs-trade-renewal-ui"
description: "Implement the renewal UI for sourcing/OEM/logistics conversion flows with complete responsive and state coverage."
---

# NEEDS TRADE Renewal UI

## Use when
- Editing `apps/web` for landing pages, service pages, quote forms, workspace shell, admin shell, or status pages.
- Translating PRD/IA into components and routes.

## UI structure to prefer
- Main landing page with clear service promise and primary CTA.
- Service routes for sourcing, OEM/ODM, goods production, inspection/packaging, customs/KC/origin, warehouse, and Rocket Growth inbound preparation.
- Quote request route for URL, product idea, quantity, channel, required work, file attachment placeholder, and contact details.
- Customer workspace shell for request list, status, quote, sample, production, inspection photos, payment, shipment, and inbound evidence.
- Admin shell only as a guarded scaffold unless operations requirements are confirmed.

## Required workflow
1. Read PRD, IA/route map, and reference role report before editing UI.
2. Implement one route or component slice at a time.
3. Keep content original, Korean-first, and specific to NEEDS TRADE.
4. Cover loading, empty, validation-error, server-error, success, disabled, and permission/unauthenticated states.
5. Check mobile, tablet, and desktop layouts.
6. Avoid deleting existing generated scaffolds unless replacement behavior is documented.

## Handoff
- Report changed files, commands run, PASS/FAIL results, remaining risks, rollback note, and personal input needs.
- Cite project paths, not copied reference content.
