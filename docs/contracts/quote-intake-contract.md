# Quote Intake Contract

## Purpose
Define the active NEEDS TRADE quote/request intake contract across the public web, customer workspace, admin workspace, API, and shared contracts. `packages/contracts/src/index.ts` is the source of truth for exported TypeScript names, literal values, DTO fields, and validation helpers.

This document does not implement backend routes, UI, persistence, upload/storage, payment, crawling, 1688 automation, credential/session handling, or external platform integrations.

## Source-of-truth exports
The shared contract exports these quote intake and operations values:

```ts
export type QuoteRequestType =
  | "product_url"
  | "bulk_excel"
  | "oem_odm_sample"
  | "rocket_growth_inbound"
  | "inspection_photo_evidence"
  | "general_consultation";

export type SalesChannel =
  | "coupang"
  | "rocket_growth"
  | "smartstore"
  | "retail"
  | "corporate"
  | "other";

export type RequestedService =
  | "china_sourcing"
  | "purchase_agency"
  | "bulk_excel_inquiry"
  | "oem_odm"
  | "sample_request"
  | "production_coordination"
  | "inspection_photo_evidence"
  | "labeling_barcode_packaging"
  | "china_warehouse"
  | "customs_readiness"
  | "shipping_inbound_coordination"
  | "rocket_growth_inbound_prep"
  | "general_consultation";

export type OperationStatus =
  | "request_received"
  | "reviewing"
  | "supplier_discovery"
  | "quote_preparing"
  | "quote_sent"
  | "sample_requested"
  | "sample_reviewing"
  | "production_pending"
  | "production_running"
  | "china_warehouse_received"
  | "inspection_running"
  | "labeling_packaging"
  | "customs_shipping"
  | "rocket_growth_inbound_prep"
  | "inbound_complete"
  | "completed"
  | "blocked"
  | "cancelled";
```

## QuoteRequestInput

```ts
export interface QuoteRequestInput {
  requesterName: string;
  requesterCompany?: string;
  contact: string;
  preferredContactMethod?: "email" | "phone" | "chat";
  requestTypes: QuoteRequestType[];
  requestedServices: RequestedService[];
  salesChannels?: SalesChannel[];
  productUrl?: string;
  productName?: string;
  productDescription?: string;
  quantity?: number;
  itemCount?: number;
  bulkFileIntent?: boolean;
  oemSampleNotes?: string;
  rocketGrowthInboundNotes?: string;
  inspectionPhotoEvidenceNotes?: string;
  generalConsultationNotes?: string;
  targetTimeline?: string;
  evidenceRequested?: OperationEvidenceType[];
}
```

## QuoteRequestEnvelope

```ts
export interface QuoteRequestEnvelope {
  requestId: string;
  accepted: boolean;
  status: OperationStatus;
  createdAt: string;
  updatedAt: string;
  input: QuoteRequestInput;
  validationIssues: QuoteRequestValidationIssue[];
}
```

`createQuoteRequestEnvelope(input)` normalizes the input, validates it, creates a deterministic `quote_...` request id from the supplied timestamp, sets `accepted` to `true` only when there are no validation issues, and initializes `status` as `request_received`.

## QuoteRequestValidationIssue

```ts
export interface QuoteRequestValidationIssue {
  field: string;
  code:
    | "required"
    | "invalid_value"
    | "unsupported_field"
    | "forbidden_secret_like_field"
    | "forbidden_secret_like_value";
  message: string;
}
```

Field paths must remain stable for API and web form error mapping. Nested secret-like fields are reported with dot paths and array indexes such as `attachments[0].secret`.

## Minimum create payload
| Field | Required | Notes |
|---|---:|---|
| `requesterName` | yes | Non-empty string after trimming. |
| `contact` | yes | Non-empty contact string after trimming. |
| `requestTypes` | conditional | Required by product behavior, but the current validator only applies path-specific rules when recognized request paths are present. |
| `requestedServices` | yes | At least one value from `RequestedService`. |
| `preferredContactMethod` | no | `email`, `phone`, or `chat` when present. |
| `salesChannels` | no | Zero or more values from `SalesChannel`; use `rocket_growth` for Rocket Growth channel intent when applicable. |
| `productUrl` | conditional | Required when `requestTypes` includes `product_url`. |
| `quantity` | conditional | Required when `requestTypes` includes `oem_odm_sample` or `rocket_growth_inbound`. |
| `itemCount` | conditional | For `bulk_excel`, required unless `bulkFileIntent` is `true`. |
| `bulkFileIntent` | conditional | For `bulk_excel`, set `true` when the customer intends a future bulk Excel file handoff. Actual upload/storage is deferred. |
| `productName` | no | Product identifier or working name. |
| `productDescription` | no | Product/request details, including general consultation detail when useful. |
| `oemSampleNotes` | no | OEM/ODM sample requirements and assumptions. |
| `rocketGrowthInboundNotes` | no | China-side Rocket Growth inbound preparation requirements. |
| `inspectionPhotoEvidenceNotes` | no | Inspection/photo evidence expectations. |
| `generalConsultationNotes` | no | General sourcing or operations consultation context. |
| `targetTimeline` | no | Planning text only; must not be treated as a guaranteed delivery date. |
| `evidenceRequested` | no | Zero or more `OperationEvidenceType` values. |

## Request path requirements
| Request path | Business meaning | Required details | Optional details |
|---|---|---|---|
| `product_url` | Product URL inquiry. | `productUrl` | `quantity`, `salesChannels`, `productDescription`, `targetTimeline` |
| `bulk_excel` | Bulk Excel inquiry boundary. | `bulkFileIntent: true` or `itemCount` | `productDescription`; future file upload only after storage approval |
| `oem_odm_sample` | OEM/ODM sample request. | `quantity` | `oemSampleNotes`, `productName`, `productDescription`, `targetTimeline` |
| `rocket_growth_inbound` | Rocket Growth inbound preparation. | `quantity` | `rocketGrowthInboundNotes`, `salesChannels`, SKU/barcode/carton/pallet context in notes |
| `inspection_photo_evidence` | Inspection/photo evidence request. | Recognized request path plus `requestedServices`; no extra validator-required field. | `inspectionPhotoEvidenceNotes`, `evidenceRequested`, warehouse receipt or defect criteria context |
| `general_consultation` | General sourcing or operations consultation. | Recognized request path plus `requestedServices`; no extra validator-required field. | `generalConsultationNotes`, `productDescription`, `targetTimeline` |

## Validation rules
The active helper functions are `normalizeQuoteRequestInput(input)`, `validateQuoteRequestInput(input)`, `createQuoteRequestEnvelope(input, now)`, and `isTerminalOperationStatus(status)`.

| Rule | Issue field | Issue code | Notes |
|---|---|---|---|
| Missing requester name | `requesterName` | `required` | Empty or absent name is rejected. |
| Missing contact | `contact` | `required` | Empty or absent contact is rejected. |
| Missing requested service selection | `requestedServices` | `required` | At least one recognized service is required. |
| Product URL inquiry without URL | `productUrl` | `required` | Applies when `requestTypes` includes `product_url`. |
| Bulk Excel inquiry without file intent or count | `bulkFileIntent` | `required` | Applies when `requestTypes` includes `bulk_excel` and neither `bulkFileIntent: true` nor `itemCount` is present. |
| OEM/ODM sample or Rocket Growth inbound without quantity | `quantity` | `required` | Applies when `requestTypes` includes `oem_odm_sample` or `rocket_growth_inbound`. |
| Unknown top-level input field | the unknown field name | `unsupported_field` | Top-level fields outside `QuoteRequestInput` are rejected. |
| String relying on leading or trailing whitespace | the string field name | `invalid_value` | Normalization trims values, and validation still reports whitespace reliance. |
| Secret-like key anywhere in the input | dot/index path to the key | `forbidden_secret_like_field` | Preserves the forbidden secret-like field validation. |
| Secret-like string value anywhere in the input | dot/index path or `$` | `forbidden_secret_like_value` | Preserves the forbidden secret-like value validation. |

## Status ownership
| OperationStatus | Set by | Customer visible? | Evidence expected |
|---|---|---:|---|
| `request_received` | system/API | yes | `request_summary` |
| `reviewing` | operator/admin | yes | `customer_visible_note` or clarification request |
| `supplier_discovery` | operator/admin | yes | `supplier_candidate` |
| `quote_preparing` | operator/admin | yes | `quote_assumption` |
| `quote_sent` | operator/admin | yes | `quote_assumption` or customer-visible quote reference |
| `sample_requested` | operator/admin | yes | `sample_photo` or sample milestone note |
| `sample_reviewing` | operator/admin | yes | `sample_review_note` |
| `production_pending` | operator/admin | yes | `production_schedule` |
| `production_running` | operator/admin | yes | `production_schedule` and customer-visible progress note |
| `china_warehouse_received` | operator/admin | yes | `warehouse_receipt_count` |
| `inspection_running` | operator/admin | yes | `inspection_checklist`, `inspection_photo`, or `defect_note` |
| `labeling_packaging` | operator/admin | yes | `label_barcode_record`, `packing_carton_note`, or `pallet_preparation_note` |
| `customs_shipping` | operator/admin | yes | `customs_document_checklist` or `shipping_coordination_note` |
| `rocket_growth_inbound_prep` | operator/admin | yes | `rocket_growth_inbound_checklist` |
| `inbound_complete` | operator/admin | yes | `shipping_coordination_note` or `completion_summary` |
| `completed` | operator/admin | yes | `completion_summary` |
| `blocked` | operator/admin | yes | `blocker_reason` |
| `cancelled` | operator/admin | yes | `customer_visible_note` |

`isTerminalOperationStatus(status)` returns `true` for `completed` and `cancelled`.

## Security and privacy boundary
- Never collect or store marketplace passwords, cookies, sessions, API keys, 1688 credentials, Coupang credentials, customer account passwords, private keys, private tokens, or secret-like values in quote intake.
- File upload is deferred until storage, retention, scanning, access control, and privacy policy are approved.
- `operatorNotes` are internal-only and must not be returned to customer-facing endpoints.
- `customerVisibleNote`, `blockerReason`, status labels, and approved customer-visible evidence may be shown to the customer.
- Admin changes require authentication, authorization, and audit logging in later implementation slices.

## API planning boundary
- `POST /api/quote-requests`: planned create boundary using `QuoteRequestInput` and `QuoteRequestEnvelope`.
- `GET /api/quote-requests/:requestId`: planned customer-safe operation detail.
- `GET /api/admin/quote-requests`: planned admin request queue, admin-only.
- `PATCH /api/admin/quote-requests/:requestId/status`: planned status transition and notes boundary, admin-only.
- `POST /api/admin/quote-requests/:requestId/evidence`: metadata-only planning boundary; binary upload/storage is deferred.

## Compatibility notes
- `QuoteRequestType`, `RequestedService`, `SalesChannel`, `OperationStatus`, `OperationStage`, `OperationEvidenceType`, `RocketGrowthInboundStatus`, `QuoteRequestInput`, `QuoteRequestEnvelope`, and `QuoteRequestValidationIssue` values must be imported from `packages/contracts/src/index.ts`.
- Status strings are durable public contract values; changes require migration notes.
- New requested service values may be added only when UI, API, contracts, and operations docs are updated together.
- Strong platform, customs, KC, legal, or delivery guarantees must not be encoded as status names or success states.
