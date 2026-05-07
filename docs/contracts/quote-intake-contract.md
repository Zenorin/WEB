# Quote Intake Contract

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
  productUrl?: string;
  bulkInquiry?: string; // description of bulk Excel upload / batch request
  productDescription?: string;
  requestedServices: Array<
    "china_sourcing" | "oem_odm" | "production" | "inspection" | "compliance" | "rocket_growth_inbound"
  >;
  salesChannel?: "coupang" | "smartstore" | "retail" | "corporate" | "other";
  quantity?: number;
  targetTimeline?: string;
  specialRequirements?: string;
  evidenceNotes?: string;
  operatorNotes?: string;
  blockerReason?: string;
}
```

## Validation rules
- `customerName`: required, non-empty string.
- `customerEmail`: required, valid email format.
- `preferredContactMethod`: required, one of `email`, `phone`, or `chat`.
- `productUrl` or `bulkInquiry`: at least one must be present.
- `requestedServices`: required, at least one service selected.
- `quantity`: optional, but if provided must be a positive integer.
- `salesChannel`: optional, should reflect the buyer’s target platform.
- `targetTimeline`: optional, free-text description of desired schedule.
- `specialRequirements`: optional, free-text detail for OEM/sample/compliance needs.

## Quote intake fields
- `productUrl`: source product link for sourcing inquiry.
- `bulkInquiry`: Excel/bulk request description for multiple SKUs.
- `requestedServices`: selected service categories.
- `salesChannel`: intended destination such as Coupang/Rocket Growth or Smartstore.
- `quantity`: requested order size.
- `targetTimeline`: expected production or inbound timeline.
- `specialRequirements`: additional details like labeling, customs, inspection, or product specifications.
- `evidenceNotes`: evidence expectations such as photo checks or packaging proof.
- `operatorNotes`: internal operator guidance and assumptions.
- `blockerReason`: reason for any request hold or missing information.

## Security boundary
- Do not store raw platform credentials, cookies, sessions, customer passwords, or API keys in quote request objects.
- Do not persist browser extension tokens, 1688 login data, or any unauthorized automation credentials.
- Keep customer contact details and request metadata separate from secret operational credentials.
