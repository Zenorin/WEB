# Quote Intake Contract

## Purpose
Define the first planning contract for NEEDS TRADE quote/request intake across the public web, customer workspace, admin workspace, API, and shared contracts. This is a documentation contract until implemented in `packages/contracts` and `apps/api`.

## Entity: QuoteRequest

```ts
export type QuoteRequestStatus =
  | "request_received"
  | "reviewing"
  | "quote_preparing"
  | "quote_sent"
  | "sample_requested"
  | "production_pending"
  | "production_running"
  | "china_warehouse_received"
  | "inspection_running"
  | "labeling_packaging"
  | "rocket_growth_inbound_prep"
  | "customs_shipping"
  | "inbound_complete"
  | "completed"
  | "blocked"
  | "cancelled";

export type RequestedService =
  | "china_sourcing"
  | "purchase_agency"
  | "oem_odm"
  | "production"
  | "inspection"
  | "labeling_packaging"
  | "compliance_readiness"
  | "warehouse_shipping"
  | "rocket_growth_inbound";

export type SalesChannel =
  | "coupang"
  | "smartstore"
  | "retail"
  | "corporate"
  | "other";

export interface QuoteRequest {
  id: string;
  status: QuoteRequestStatus;
  createdAt: string; // ISO 8601
  updatedAt: string; // ISO 8601

  customerName: string;
  customerCompany?: string;
  customerEmail: string;
  customerPhone?: string;
  preferredContactMethod: "email" | "phone" | "chat";

  requestTypes: Array<
    "product_url" | "bulk_inquiry" | "oem_sample" | "inspection_evidence" | "rocket_growth_prep"
  >;
  productUrl?: string;
  bulkInquiry?: string;
  productDescription?: string;
  oemRequirements?: string;
  inboundRequirements?: string;

  requestedServices: RequestedService[];
  salesChannel?: SalesChannel;
  quantity?: number;
  targetTimeline?: string;
  specialRequirements?: string;
  complianceQuestions?: string;
  evidenceNotes?: string;

  customerVisibleNote?: string;
  operatorNotes?: string;
  blockerReason?: string;
}
```

## Minimum create payload
| Field | Required | Notes |
|---|---:|---|
| `customerName` | yes | Non-empty string. |
| `customerEmail` | yes | Valid email format. |
| `preferredContactMethod` | yes | `email`, `phone`, or `chat`. |
| `requestTypes` | yes | At least one request path. |
| `productUrl` or `bulkInquiry` or `productDescription` | yes | At least one product/request detail must be present. |
| `requestedServices` | yes | At least one selected service. |
| `quantity` | no | Positive integer when present. |
| `salesChannel` | no | Use `coupang` for Rocket Growth intent when applicable. |
| `targetTimeline` | no | Free text; must not be treated as guaranteed delivery date. |
| `specialRequirements` | no | Packaging, product, sample, or operational details. |
| `complianceQuestions` | no | Advisory question field only. |
| `evidenceNotes` | no | Photo, inspection, label, packing, or handoff evidence expectations. |

## Request path requirements
| Request path | Required details | Optional details |
|---|---|---|
| `product_url` | `productUrl` or product description | quantity, sales channel, special requirements |
| `bulk_inquiry` | `bulkInquiry` text description | future file upload after storage approval |
| `oem_sample` | `productDescription` or `oemRequirements` | material, packaging, target quantity, sample needs |
| `inspection_evidence` | product/request description and evidence needs | defect criteria, photo checklist, warehouse receipt notes |
| `rocket_growth_prep` | inbound requirements or product description | SKU, barcode/label needs, carton/pallet details, channel timing |

## Status ownership
| Status | Set by | Customer visible? | Evidence expected |
|---|---|---:|---|
| `request_received` | system/API | yes | request summary |
| `reviewing` | operator/admin | yes | clarification questions or operator summary |
| `quote_preparing` | operator/admin | yes | estimate assumptions |
| `quote_sent` | operator/admin | yes | quote summary or document reference |
| `sample_requested` | operator/admin | yes | sample specs and supplier milestone |
| `production_pending` | operator/admin | yes | production plan or pending confirmation |
| `production_running` | operator/admin | yes | progress notes |
| `china_warehouse_received` | operator/admin | yes | receipt count and photos |
| `inspection_running` | operator/admin | yes | inspection checklist and photos |
| `labeling_packaging` | operator/admin | yes | label/barcode/packing evidence |
| `rocket_growth_inbound_prep` | operator/admin | yes | inbound prep checklist and coordination notes |
| `customs_shipping` | operator/admin | yes | document/shipping coordination notes |
| `inbound_complete` | operator/admin | yes | handoff/readiness evidence |
| `completed` | operator/admin | yes | final summary |
| `blocked` | operator/admin | yes | customer-safe blocker reason |
| `cancelled` | operator/admin | yes | cancellation note |

## Security and privacy boundary
- Never collect or store marketplace passwords, cookies, sessions, API keys, 1688 credentials, Coupang credentials, customer account passwords, or private tokens in quote intake.
- File upload is deferred until storage, retention, scanning, access control, and privacy policy are approved.
- `operatorNotes` are internal-only and must not be returned to customer-facing endpoints.
- `customerVisibleNote`, `blockerReason`, status labels, and approved evidence may be shown to the customer.
- Admin changes require authentication, authorization, and audit logging in later implementation slices.

## API planning boundary
- `POST /api/quote-requests`: create request with minimum payload validation.
- `GET /api/quote-requests/:id`: customer-safe request detail.
- `GET /api/admin/quote-requests`: admin request queue, admin-only.
- `PATCH /api/admin/quote-requests/:id/status`: status transition and notes, admin-only.
- `POST /api/admin/quote-requests/:id/evidence`: deferred until file/evidence storage is approved.

## Compatibility notes
- Status strings are durable public contract values; changes require migration notes.
- New requested service values may be added if UI, API, contracts, and operations docs are updated together.
- Strong platform/legal guarantees must not be encoded as status names or success states.
