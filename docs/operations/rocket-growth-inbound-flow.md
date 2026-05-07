# Rocket Growth Inbound Flow

## Positioning
Use "Rocket Growth inbound preparation/support" until operational authority is verified. The renewal must not claim guaranteed Coupang approval, official platform outcome, customs clearance, KC certification, or delivery date.

## Scope interpretation
For NEEDS TRADE, Rocket Growth planning means China-side preparation and coordination:
- China warehouse or partner warehouse receipt.
- Quantity and SKU checks.
- Inspection/photo evidence where supported.
- Label and barcode work based on customer-provided or approved requirements.
- Carton, pallet, packing, wrapping, and packing-list preparation where supported.
- Export/import coordination notes and document readiness.
- Coupang logistics center inbound support and handoff evidence without approval guarantees.

## Customer inputs
| Input | Purpose |
|---|---|
| Target sales channel | Identify Coupang/Rocket Growth intent or another channel. |
| Product/SKU details | Determine SKU, quantity, variation, and evidence needs. |
| Barcode/label requirements | Prepare label/barcode work from approved requirements. |
| Dimensions and weight | Support carton, pallet, shipping, and document planning. |
| Carton/pallet configuration | Plan packing and inbound preparation tasks. |
| Desired timing | Inform planning only; not a guaranteed delivery date. |
| Compliance/document questions | Identify readiness blockers or coordination needs. |
| Photo/evidence expectations | Define what customer wants to see after receipt or inspection. |

## Operator tasks
| Task | Status mapping | Evidence |
|---|---|---|
| Record inbound-prep request | `request_received` / `reviewing` | Request summary and missing information. |
| Confirm SKU/quantity assumptions | `quote_preparing` | Quote assumptions and required inputs. |
| Receive goods in China warehouse | `china_warehouse_received` | Receipt count, SKU note, warehouse photos. |
| Check quantity and visible condition | `inspection_running` | Inspection checklist, photos, defect notes. |
| Prepare labels/barcodes/cartons/pallets | `labeling_packaging` | Label/barcode record, packing photos, carton/pallet notes. |
| Coordinate inbound preparation | `rocket_growth_inbound_prep` | Inbound checklist, packing list, handoff notes. |
| Coordinate customs/shipping documents | `customs_shipping` | Document checklist and shipment coordination notes. |
| Complete preparation/handoff evidence | `inbound_complete` | Final preparation summary and approved evidence. |

## Flow states
1. `request_received`
2. `reviewing`
3. `quote_preparing`
4. `quote_sent`
5. `china_warehouse_received`
6. `inspection_running`
7. `labeling_packaging`
8. `rocket_growth_inbound_prep`
9. `customs_shipping`
10. `inbound_complete`
11. `completed`

`blocked` and `cancelled` may interrupt the flow when customer inputs, documents, supplier responses, payment/approval, or operational issues stop progress.

## Evidence requirements
- `china_warehouse_received`: receipt counts, warehouse photos, SKU/quantity confirmation note.
- `inspection_running`: visible-condition checklist, quantity check, photo evidence, defect/blocker notes.
- `labeling_packaging`: label/barcode application notes, carton or pallet configuration, packing photos.
- `rocket_growth_inbound_prep`: inbound preparation checklist, packing list, coordination notes.
- `customs_shipping`: export/import document readiness notes and shipping coordination status.
- `inbound_complete`: final handoff evidence and preparation completion note.

## Claim boundaries
- Completion of inspection, labeling, packing, or handoff evidence does not mean Coupang has approved or accepted inbound inventory.
- Customs/shipping coordination does not guarantee clearance, certification, or exact delivery.
- Customer-provided label/barcode/spec requirements must be treated as inputs, not platform validation.
- Any future claim of official partnership, guaranteed acceptance, or direct platform integration requires business owner evidence and legal/compliance review.

## Deferred automation
- Automated Coupang or 1688 credential use is forbidden in this planning slice.
- Browser extension import, supplier crawling, and marketplace search widgets remain deferred.
- File upload and evidence storage require separate privacy, retention, access-control, and security decisions.
