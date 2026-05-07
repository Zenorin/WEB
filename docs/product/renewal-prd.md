# NEEDS TRADE Renewal PRD

## Classification
Planning and reference-analysis package for the NEEDS TRADE web renewal. This slice does not implement UI, API, extension, collector, or automation code.

## Product goal
Renew NEEDS TRADE into a conversion-first website and planning baseline for an integrated China sourcing, OEM/ODM, inspection, customs-readiness, warehouse, and Coupang Rocket Growth inbound preparation operation platform.

## Business interpretation
- NEEDS TRADE is a renewal target, not a finished product.
- Reference pages inform role, IA, service flow, customer journey, evidence patterns, and conversion flow only.
- Rocket Growth means China-side warehouse receipt, inspection, quantity check, photo evidence, label/barcode work, carton or pallet preparation, export/import coordination, and Coupang logistics center inbound support.
- Do not claim guaranteed Coupang approval, customs clearance, KC certification, delivery date, or platform outcome unless the business owner confirms it later.
- First implementation should be the web renewal with quote/request intake plus customer/admin workspace boundaries.
- Extension, collectors, and automated 1688 crawling remain deferred and guarded.

## Target users
- Coupang Rocket Growth and marketplace sellers preparing inventory sourced from China.
- Smartstore and retail sellers requesting China sourcing, purchase agency, or bulk SKU support.
- Brand owners planning OEM/ODM, goods production, samples, packaging, or private-label products.
- Corporate buyers ordering promotional goods or branded merchandise.
- NEEDS TRADE operators who triage quotes, supplier coordination, warehouse receipt, inspections, evidence, and inbound preparation.
- Admin/manager users who need visibility into request status, blockers, and customer-facing evidence.

## Goals
- Make NEEDS TRADE's renewed service scope understandable from the first public screen.
- Convert visitors into quote/request submissions with enough operational detail for review.
- Define customer workspace boundaries for request tracking, status, evidence, blockers, and next actions.
- Define admin workspace boundaries for triage, status transitions, operator notes, evidence upload, and blocker management.
- Document operational states and evidence artifacts before implementation.
- Keep all reference analysis clean-room and independently expressed.

## Non-goals
- No UI/product code in this planning slice.
- No copied reference source, exact copy, image assets, icons, tracking, hidden text, cookies, sessions, or credentials.
- No real API keys, passwords, customer credentials, platform tokens, or private cookies.
- No guarantee claims for Coupang approval, customs clearance, KC certification, delivery date, or marketplace outcomes.
- No extension, collector, 1688 automation, browser scraping, payment, ERP, or production file-storage implementation in the first slice.

## Confirmed capabilities
- NEEDS TRADE has an existing public site with service, portfolio, purchase agency, and mypage navigation.
- Existing purchase agency content points to a workspace concept and supports purchase agency, delivery agency, bulk Excel registration, and inventory management at a role level.
- The local repository contains clean-room planning, module routing, contracts, operations, and scaffold guidance.

## Planned capabilities
- Public renewal site with landing, service routes, process explanation, Rocket Growth preparation route, quote CTA, FAQ/fee/portfolio placeholders, and evidence-safe content.
- Quote intake for product URL, bulk inquiry, OEM/ODM sample request, inspection/evidence request, compliance-readiness question, and Rocket Growth inbound preparation.
- Customer workspace boundary for request status, evidence, blocker notes, and next action guidance.
- Admin workspace boundary for request triage, quote review, operator notes, status changes, evidence management, and blocker resolution.
- Operations model for sourcing, production, warehouse receipt, inspection, labeling/packaging, Rocket Growth preparation, customs/shipping coordination, and completion.

## Assumptions requiring owner confirmation
- Whether NEEDS TRADE directly operates China warehouses or coordinates partner warehouses.
- Which inspection, labeling, barcode, packing, pallet, document, and inbound support tasks are available today.
- Which customs, KC, origin, and compliance activities can be described as owned, coordinated, or advisory.
- Which fee model, contact channels, workspace features, and evidence attachments can be exposed publicly.
- Which portfolio/customer examples and visual evidence are approved for publication.

## Core journeys
1. Product URL sourcing request
   - Visitor submits product URL, quantity, target channel, and requested services.
   - Operator reviews sourcing assumptions, supplier/product feasibility, and quote inputs.
2. Bulk or Excel request
   - Visitor describes or uploads a multi-SKU list later through an approved upload path.
   - Operator triages batch complexity, missing fields, and quote grouping.
3. OEM/ODM sample request
   - Visitor provides concept, specs, materials, packaging, target quantity, and sample needs.
   - Operator records sample milestones and production assumptions.
4. Inspection/photo evidence request
   - Visitor requests warehouse receipt, quantity check, inspection, defect notes, and photo evidence.
   - Operator attaches evidence and updates customer-facing status.
5. Rocket Growth inbound preparation request
   - Visitor provides SKU, barcode/labeling needs, carton or pallet configuration, target inbound channel, and timing.
   - Operator records preparation checklist, packing/document notes, and inbound coordination status.
6. Customer status tracking
   - Customer views status, evidence, blockers, and next actions without seeing internal notes or credentials.
7. Admin operations
   - Admin user manages triage, status transitions, evidence, blocker reasons, and next-step instructions.

## Service catalog
| Service | Public promise boundary | Evidence/output |
|---|---|---|
| China sourcing / purchase agency | Coordinate product sourcing and purchase request review. | Request summary, quote assumptions, supplier/product notes. |
| OEM/ODM | Coordinate sample/spec/production planning. | Sample specs, production plan notes, approval checkpoints. |
| Goods production | Track production coordination and milestone status. | Production notes, quantity expectations, issue/blocker records. |
| Inspection/photo evidence | Check receipt quantity and visible condition where supported. | Receipt counts, inspection checklist, photos, defect notes. |
| Labeling/barcode/packing | Prepare labels, barcode work, cartons, packing, or pallet instructions where supported. | Label/barcode records, packing photos, carton/pallet notes. |
| Customs/compliance readiness | Coordinate document readiness and advisory checkpoints. | Required-document checklist, coordination notes, blocker list. |
| Warehouse/shipping coordination | Track warehouse receipt and export/import handoff preparation. | Warehouse photos, receipt records, shipment/document status notes. |
| Rocket Growth inbound preparation | Prepare and coordinate China-side inbound support for Coupang-oriented workflows. | Inbound prep checklist, packing list, barcode/label evidence, handoff notes. |

## Public site scope
- Home: integrated service positioning, primary quote CTA, service categories, process, evidence, and guarded Rocket Growth summary.
- Services overview: all service categories with boundaries and quote entry points.
- Service detail routes: sourcing, OEM/ODM, production, inspection/packaging, compliance readiness, Rocket Growth inbound preparation.
- Quote route: request intake contract and validation states.
- Portfolio route: evidence-safe examples only after approved content exists.
- Fee guide route: estimate model or contact-for-quote guidance until exact fees are approved.
- FAQ route: scope, evidence, timelines, fees, compliance boundaries, and platform disclaimer guidance.

## Workspace scope
- Customer workspace: request list, status cards, status timeline, evidence list, quote summary, blockers, and next action guidance.
- Admin workspace: request queue, filters, request detail, status transition controls, operator notes, evidence management, blocker reason, and customer-visible update draft.
- Auth, permissions, notifications, file storage, and audit logs require later implementation slices and security review before production.

## First implementation target
1. Public web shell with routes and original copy structure.
2. Quote intake form UI aligned to `docs/contracts/quote-intake-contract.md`.
3. Customer workspace placeholder with safe status/evidence states.
4. Admin workspace placeholder with clear internal-only boundaries.

## Acceptance criteria
- Planning docs distinguish observed facts, inferred requirements, confirmed capabilities, planned capabilities, and open questions.
- Quote intake and operations docs define statuses, fields, evidence, and guardrails.
- IA and component inventory cover public, customer, and admin surfaces with loading/empty/error/success/permission states.
- WBS, command queue, and phase gates keep extension, collectors, and 1688 automation deferred.
- Validation commands pass or blockers are documented.
