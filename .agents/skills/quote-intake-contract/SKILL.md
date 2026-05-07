---
name: "quote-intake-contract"
description: "Define and maintain the quote/request/status contract across web, API, contracts, workspace, and admin flows."
---

# Quote Intake Contract

## Use when
- Creating or changing quote request forms, API DTOs, status enums, customer workspace fields, admin review fields, or validation errors.
- Connecting `apps/web`, `apps/api`, and `packages/contracts`.

## Baseline fields
`requestId`, `customerType`, `sourceType`, `productUrl`, `productName`, `targetQuantity`, `salesChannels`, `requiredServices`, `attachments`, `status`, `createdAt`, `updatedAt`.

## Status enum baseline
`draft`, `submitted`, `reviewing`, `quote-preparing`, `quote-sent`, `sample-requested`, `sample-reviewing`, `production-pending`, `production-running`, `china-warehouse-received`, `inspection-running`, `labeling-packaging`, `customs-shipping`, `rocket-growth-inbound-prep`, `inbound-complete`, `completed`, `blocked`, `cancelled`.

## Required workflow
1. Update contracts first, then API, then web UI.
2. Keep customer-visible labels separate from internal operations notes.
3. Do not store raw cookies, platform login data, or third-party account credentials.
4. Provide validation errors with stable field paths.
5. Add migration notes when status names change.

## Handoff
- Report changed files, commands run, PASS/FAIL results, remaining risks, rollback note, and personal input needs.
- Cite project paths, not copied reference content.
