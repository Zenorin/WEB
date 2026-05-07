# IA and Route Map

## IA principles
- Lead with quote conversion and service clarity.
- Keep legal/platform-sensitive claims bounded and evidence-based.
- Separate public marketing, customer workspace, and admin operations surfaces.
- Treat Rocket Growth as inbound preparation/support, not guaranteed platform approval.
- Keep extension, collectors, and 1688 automation out of the IA until separately approved.

## Public navigation
| Label | Route | Purpose | Primary CTA |
|---|---|---|---|
| Home | `/` | Establish NEEDS TRADE renewal positioning and route users to quote intake. | Start quote request |
| Services | `/services` | Show integrated service catalog and boundaries. | Select service for quote |
| Process | `/process` | Explain request-to-evidence operations lifecycle. | Request consultation |
| Rocket Growth | `/services/rocket-growth` | Explain China-side Coupang inbound preparation/support. | Request inbound prep quote |
| Quote | `/quote` | Capture product URL, bulk inquiry, OEM/ODM, inspection, compliance, and inbound-prep requests. | Submit request |
| Workspace | `/workspace` | Customer request tracking entry. | View request status |

## Public routes
| Route | Page role | Required sections | Guardrails |
|---|---|---|---|
| `/` | Renewal landing page | Hero, service overview, process preview, evidence preview, Rocket Growth preview, quote CTA, FAQ preview | No unsupported rank, approval, delivery, customs, KC, or platform claims. |
| `/services` | Service catalog | Category grid, service boundaries, evidence/output summary, quote CTA | State preparation/coordination boundaries clearly. |
| `/services/sourcing` | China sourcing and purchase agency | Product URL flow, supplier/quote assumptions, operator review steps, evidence examples | No automated 1688 crawling claim. |
| `/services/oem-odm` | OEM/ODM and sample planning | Spec intake, sample/production milestones, approval checkpoints, quote CTA | Do not promise factory outcome or certification. |
| `/services/production` | Goods production coordination | Production stages, quantity/status checkpoints, blocker handling | Do not claim production capacity until confirmed. |
| `/services/inspection-packaging` | Inspection, labeling, barcode, and packaging | Warehouse receipt, quantity check, photo evidence, label/barcode, carton/pallet prep | Do not imply inspection guarantees product quality beyond observed checks. |
| `/services/compliance` | Compliance/customs readiness guidance | Document checklist, responsibility boundaries, FAQ, contact CTA | No guaranteed customs clearance, KC approval, origin approval, or legal advice. |
| `/services/rocket-growth` | Coupang Rocket Growth inbound preparation support | China warehouse receipt, inspection, label/barcode, carton/pallet prep, document coordination, inbound handoff evidence | No guaranteed Coupang approval, delivery date, or platform acceptance. |
| `/process` | Operational lifecycle | Timeline/status model, evidence map, customer/admin handoff explanation | Match statuses to contracts and operations docs. |
| `/portfolio` | Evidence-safe examples | Approved cases, product categories, before/after evidence types | Use only owner-approved assets and original copy. |
| `/fee-guide` | Fee and estimate guidance | Service fee categories, quote assumptions, variables, contact CTA | Use ranges or inquiry model until exact fees are approved. |
| `/faq` | Decision support | Sourcing, OEM, inspection, Rocket Growth, compliance boundaries, workspace FAQ | Avoid legal/platform guarantees. |
| `/quote` | Request intake | Request type selector, product URL/bulk/OEM fields, service selector, quantity/channel, contact, consent, submit states | No credential collection. |

## Customer workspace routes
| Route | Page role | Required states |
|---|---|---|
| `/workspace` | Customer request overview with cards, filters, and next action summaries. | unauthenticated, loading, empty, populated, server-error, permission-denied |
| `/workspace/requests/:requestId` | Customer-facing request detail with status timeline, quote summary, evidence, blockers, and next actions. | loading, not-found, permission-denied, populated, blocked, completed, server-error |

## Admin routes
| Route | Page role | Required states |
|---|---|---|
| `/admin` | Internal request queue for triage and operational visibility. | unauthenticated, permission-denied, loading, empty, populated, server-error |
| `/admin/requests/:requestId` | Internal request detail for status updates, notes, evidence, blockers, and customer-visible update drafting. | loading, not-found, permission-denied, populated, validation-error, saved, server-error |

## Deferred routes
- `/extension/*`: blocked until extension permissions, message contracts, privacy review, and customer consent are approved.
- `/collectors/*`: blocked until collector contracts, anti-bot/compliance review, and session-boundary policy are approved.
- `/1688-search` or marketplace search routes: blocked until legal/API/session authority is confirmed.
- Payment, settlement, ERP, and full inventory routes: deferred beyond the first implementation target.

## Route-to-module ownership
| Surface | Module path | Workstream |
|---|---|---|
| Public web and workspace/admin shells | `apps/web` | `$project-frontend-design` |
| Quote intake API boundary | `apps/api` | `$project-backend-api` |
| Shared request/status contracts | `packages/contracts` | `$project-contracts` |
| Operation status rules | `packages/core` | `$project-core-pipeline` |
| Extension boundary | `apps/extension` | `$project-extension-bridge` |
| Collector boundary | `packages/collectors` | `$project-market-collectors` |
| Reference role analysis | `tools/reference-analysis` | `$project-reference-mapper` |
