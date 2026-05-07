# China Sourcing Operations Model

## Principle
Customer-visible operations must be represented as explicit statuses and evidence artifacts. Do not imply a service is operational until the business owner confirms the process and responsibility.

## Status lifecycle
- `request_received` — Inquiry accepted and recorded.
- `reviewing` — Operator is reviewing requested services and customer details.
- `quote_preparing` — Quote estimation is in progress.
- `quote_sent` — Quote has been delivered to the customer.
- `sample_requested` — OEM/sample request has been initiated.
- `production_pending` — Production planning or supplier confirmation is pending.
- `production_running` — Production is underway with supplier coordination.
- `china_warehouse_received` — Goods have been received at the China warehouse.
- `inspection_running` — Inspection or quality check is in progress.
- `labeling_packaging` — Labeling, barcode, or packaging work is in progress.
- `rocket_growth_inbound_prep` — Rocket Growth inbound preparation is underway.
- `customs_shipping` — Customs/shipping coordination is in progress.
- `inbound_complete` — Inbound preparation or delivery evidence has been completed.
- `completed` — Request lifecycle is complete.
- `blocked` — Request is paused due to missing information or issue resolution.
- `cancelled` — Request has been cancelled.

## Status-to-evidence map
| Stage | Customer label | Evidence |
|---|---|---|
| request_received | Request received | Request summary and service selection |
| reviewing | Under review | Operator note and questions |
| quote_preparing | Quote preparing | Supplier assumptions, estimate details |
| quote_sent | Quote sent | Quote document or estimate summary |
| sample_requested | Sample request initiated | Sample specs and supplier confirmation |
| production_pending | Production pending | Supplier agreement or production plan |
| production_running | Production running | Production progress notes |
| china_warehouse_received | China warehouse received | Receipt count and warehouse photos |
| inspection_running | Inspection running | Inspection photos, checklists, results |
| labeling_packaging | Labeling/packaging | Label, barcode, carton/prep evidence |
| rocket_growth_inbound_prep | Rocket Growth prep | Inbound preparation checklist and evidence |
| customs_shipping | Customs/shipping | Document list, shipment status notes |
| inbound_complete | Inbound complete | Handover evidence and receipt confirmation |
| completed | Completed | Final summary and completion note |
| blocked | Blocked | Blocker reason and required action |
| cancelled | Cancelled | Cancellation note and refund guidance if applicable |

## Evidence requirements
- `request_received`: capture service intent, contact details, and request category.
- `quote_sent`: store quote details or attached estimate summary.
- `china_warehouse_received`: capture warehouse receipt counts and photo evidence.
- `inspection_running`: capture inspection checklist results and photo evidence.
- `labeling_packaging`: capture labeling, barcode, and packaging evidence.
- `rocket_growth_inbound_prep`: capture inbound preparation checklist and any coordination notes.
- `customs_shipping`: capture customs document status and shipping notes.
- `inbound_complete`: capture final inbound evidence and delivery readiness confirmation.

## Operation boundary guidance
- Do not claim customs clearance, KC certification, or platform approval without explicit business confirmation.
- Do not model automation contracts for 1688 or extension scraping until approved.
- Keep customer status labels simple and aligned with operational phases.
