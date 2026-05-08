# China Sourcing Operations Model

## Principle
Customer-visible operations must be represented as explicit statuses and evidence artifacts. Do not imply that a service is operational, legally guaranteed, or platform-approved until the business owner confirms process ownership and responsibility.

## Scope
This model covers China sourcing, purchase agency, OEM/ODM, goods production coordination, warehouse receipt, inspection/photo evidence, labeling/barcode/packing, customs/shipping coordination, and Rocket Growth inbound preparation.

## Responsibility levels
| Level | Meaning | Public wording guidance |
|---|---|---|
| Owned | NEEDS TRADE directly performs the task. | May say supported/performed after owner confirmation. |
| Coordinated | NEEDS TRADE coordinates with partner, supplier, warehouse, carrier, or broker. | Say coordinated or supported, not guaranteed. |
| Advisory | NEEDS TRADE provides checklist or readiness guidance. | Say guidance/readiness only. |
| Deferred | Not active in the first release. | Say unavailable or future/approval-gated internally only. |

## Status lifecycle
| Status | Customer label | Purpose | Evidence |
|---|---|---|---|
| `request_received` | Request received | Inquiry accepted and recorded. | Request summary and service selection. |
| `reviewing` | Under review | Operator reviews requested services and missing details. | Operator questions or review note. |
| `supplier_discovery` | Supplier discovery | Supplier candidates, MOQ, lead time, or feasibility are being checked. | Supplier candidate note and quote assumptions. |
| `quote_preparing` | Quote preparing | Quote assumptions and supplier/product feasibility are being reviewed. | Estimate assumptions and required inputs. |
| `quote_sent` | Quote sent | Quote or estimate summary has been delivered. | Quote summary/document reference. |
| `sample_requested` | Sample requested | OEM/sample request has been initiated or coordinated. | Sample specs and milestone note. |
| `sample_reviewing` | Sample reviewing | Sample evidence, customer feedback, or revision questions are being reviewed. | Sample review note and approved photos where applicable. |
| `production_pending` | Production pending | Production plan, supplier confirmation, or approval is pending. | Supplier or production plan note. |
| `production_running` | Production running | Production coordination is underway. | Progress notes and issue records. |
| `china_warehouse_received` | China warehouse received | Goods have arrived at the China warehouse or partner warehouse. | Receipt count, SKU note, warehouse photos. |
| `inspection_running` | Inspection running | Quantity/visible-condition/photo evidence check is underway. | Checklist, photos, defect/blocker notes. |
| `labeling_packaging` | Labeling and packaging | Label, barcode, carton, packing, or pallet prep is underway. | Label/barcode record, packing photos, carton/pallet notes. |
| `rocket_growth_inbound_prep` | Inbound preparation | Coupang-oriented inbound prep checklist and coordination are underway. | Inbound checklist, packing list, coordination notes. |
| `customs_shipping` | Customs/shipping coordination | Export/import document and shipping handoff coordination is underway. | Document checklist and shipment notes. |
| `inbound_complete` | Inbound preparation complete | Preparation evidence or handoff readiness has been completed. | Final evidence summary and handoff note. |
| `completed` | Completed | Request lifecycle is complete. | Final summary. |
| `blocked` | Action needed | Request is paused due to missing info, issue, or customer decision. | Customer-safe blocker reason and next action. |
| `cancelled` | Cancelled | Request was cancelled. | Cancellation note. |

## Stage transition rules
- New requests start at `request_received`.
- `blocked` can be entered from any active status when required information, payment, approval, supplier answer, document, or issue resolution is missing.
- `cancelled` can be entered from any active status with a cancellation note.
- Warehouse, inspection, labeling/packaging, Rocket Growth preparation, customs/shipping, and inbound-complete statuses should not appear unless the preceding operational milestone exists or an admin records a reason.
- `completed` requires final customer-visible summary.

## Evidence artifact types
| Artifact | Customer-visible? | Notes |
|---|---:|---|
| Request summary | yes | Captured from quote intake. |
| Quote assumptions | yes | Avoid treating assumptions as guarantees. |
| Operator notes | no | Internal-only. |
| Customer-visible note | yes | Safe summary drafted by admin/operator. |
| Warehouse receipt count | yes | Must be recorded as observed count, not guarantee of final condition. |
| Inspection checklist | yes | Scope-limited to observed checks. |
| Photo evidence | yes, when approved | Use owner-approved or customer-specific evidence only. |
| Label/barcode record | yes | Confirm work performed/prepared, not platform acceptance. |
| Packing list/carton notes | yes | Use as preparation evidence. |
| Customs/shipping document checklist | yes | Coordination/readiness only. |
| Blocker reason | yes | Customer-safe reason and next action. |
| Audit log | admin-only | Deferred implementation requirement. |

## Operation boundary guidance
- Do not claim customs clearance, KC certification, origin approval, Coupang approval, platform acceptance, exact delivery date, or legal outcome.
- Do not model 1688 API, scraping, browser extension, session/cookie reuse, or customer credential capture until separately approved.
- Use "preparation", "coordination", "readiness", and "evidence" for uncertain or partner-dependent work.
- Keep customer status labels simple and aligned with the quote intake contract.

## Open owner inputs
- Which statuses are supported immediately at launch versus planned after operations confirmation?
- Which evidence artifacts can be uploaded, stored, and shown to customers?
- Which tasks are performed by NEEDS TRADE staff, partners, suppliers, warehouses, brokers, or carriers?
- Which compliance documents are safe to list publicly?
