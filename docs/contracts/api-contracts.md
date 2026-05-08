# API Contracts

## Purpose
This document defines planned API envelopes only. It does not implement backend routes, persistence, auth, uploads, payments, crawling, or external platform integrations.

## Shared source of truth
The planned API must import and preserve the shared shapes from `packages/contracts/src/index.ts`:
- `QuoteRequestInput`
- `QuoteRequestValidationIssue`
- `QuoteRequestEnvelope`
- `OperationRecord`
- `OperationEvidence`
- `OperationTimelineEvent`
- `RocketGrowthInboundRecord`

## Envelope conventions
All planned endpoints should return serializable envelopes:

```ts
export interface ApiSuccessEnvelope<T> {
  ok: true;
  data: T;
  requestId?: string;
}

export interface ApiErrorEnvelope {
  ok: false;
  error: {
    code: string;
    message: string;
    issues?: QuoteRequestValidationIssue[];
  };
  requestId?: string;
}
```

These envelope names are documentation-only until an API slice implements them.

## Planned public endpoints
| Method | Path | Request | Success data | Notes |
|---|---|---|---|---|
| `POST` | `/api/quote-requests` | `QuoteRequestInput` | `QuoteRequestEnvelope` | Validate and normalize only. Persistence belongs to a later API slice. |
| `GET` | `/api/quote-requests/:requestId` | none | Customer-safe `OperationRecord` | Planned customer workspace read boundary. |

## Planned admin endpoints
| Method | Path | Request | Success data | Notes |
|---|---|---|---|---|
| `GET` | `/api/admin/quote-requests` | filter query | `OperationRecord[]` | Admin-only queue boundary. |
| `GET` | `/api/admin/quote-requests/:requestId` | none | `OperationRecord` | Admin-only detail boundary. |
| `PATCH` | `/api/admin/quote-requests/:requestId/status` | status, customer note, internal note boundary | `OperationRecord` | Must validate status transitions in a later core/API slice. |
| `POST` | `/api/admin/quote-requests/:requestId/evidence` | `OperationEvidence` metadata | `OperationRecord` | Metadata-only planning boundary; binary file upload is deferred. |
| `PUT` | `/api/admin/rocket-growth/:inboundId/checklist/:itemId` | checklist item status update | `RocketGrowthInboundRecord` | Planned Rocket Growth inbound prep checklist boundary. |

## Customer-safe field boundary
Customer-facing endpoints may expose:
- `OperationRecord.status`
- `OperationRecord.stage`
- customer-visible timeline events
- customer-visible evidence
- `blockerReason`
- `customerVisibleNote`

Customer-facing endpoints must not expose:
- `operatorNotes`
- raw credentials, cookies, sessions, tokens, or platform login data
- internal audit metadata
- partner/private supplier notes unless explicitly approved
- unsupported platform, customs, KC, legal, or delivery guarantees

## Validation error boundary
Quote intake validation should forward `QuoteRequestValidationIssue` objects from `validateQuoteRequestInput(input)`. Field paths must remain stable so web forms can map errors without parsing messages.

## Deferred integrations and non-goals
- No route implementation in this slice.
- No database persistence.
- No binary file upload or storage.
- No auth/session implementation.
- No payment or settlement.
- No browser extension, collectors, 1688 automation, marketplace scraping, or platform API calls.
- No credential collection or storage.
- No guaranteed Coupang approval, Rocket Growth acceptance, customs clearance, KC certification, legal result, or delivery date.

## Compatibility notes
- API DTOs must not redefine contract literals locally.
- Breaking changes to shared contracts require API compatibility notes and migration guidance.
- New API endpoints should identify whether they are public, customer-authenticated, or admin-only before implementation.
