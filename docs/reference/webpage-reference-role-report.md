# Webpage Reference Role Report

## Purpose
This report records clean-room role observations for the NEEDS TRADE renewal planning slice. It is not a copy source for code, copywriting, layout, assets, or implementation details.

## Clean-room rule
- Use the reference pages only for role, IA, service-flow, evidence, customer journey, and conversion-flow understanding.
- Do not reuse HTML, CSS, JavaScript, images, icons, logos, hidden text, cookies, tracking snippets, slogans, exact marketing copy, class names, or internal implementation identifiers.
- Convert every observation into new NEEDS TRADE-specific requirements before implementation.

## Reference inventory
| Reference | URL | Access time | Observable role-level facts |
|---|---|---:|---|
| Existing NEEDS TRADE home | `https://www.needstrade.com` | 2026-05-07 UTC | Public navigation includes services, portfolio, purchase agency, and mypage. The home page positions NEEDS TRADE around OEM/promotional goods, shows a high-level plan/design/production/logistics sequence, includes portfolio previews, and routes visitors toward purchase agency. |
| Existing NEEDS TRADE purchase agency | `https://www.needstrade.com/purchaseAgency` | 2026-05-07 UTC | Purchase agency page presents a workspace CTA and a compact feature list covering purchase agency, delivery agency, bulk Excel registration, and inventory management. |
| Reference sourcing site | `https://sourcingchina.co.kr/` | 2026-05-07 UTC | Reference IA groups company, work/service introductions, OEM/ODM, cases, import process, Rocket Growth, goods production, purchase agency, usage guides, fee/help content, market guides, news, Q&A, and inquiry. It uses repeated inquiry/contact CTAs, process stages, service cards, trust/evidence blocks, FAQ-like sections, and 1688/search-related surface. |
| Reference Rocket Growth page | `https://sourcingchina.co.kr/ro_01/` | 2026-05-07 UTC | Rocket Growth content emphasizes China-side warehouse receipt, inspection, wrapping/labeling/barcode or pallet/carton preparation, shipping/document coordination, and inbound support. Some observed claims are stronger than NEEDS TRADE may currently support and must be softened into preparation/support language. |
| GitHub repo context | `https://github.com/Zenorin/WEB` and local `/workspaces/WEB` | 2026-05-07 UTC | Public GitHub page shows a minimal public repository context, while the local workspace contains planning, module routing, skillset, contracts, and scaffold docs for a clean-room web renewal. Local files are the implementation source of truth for this slice. |

## Observed facts
- NEEDS TRADE currently has public service, portfolio, purchase agency, and mypage navigation.
- NEEDS TRADE already hints at workspace-based purchase agency workflows and bulk Excel/product management concepts.
- The reference sourcing site uses broad service taxonomy: sourcing/purchase agency, OEM/ODM, production cases, import process, Rocket Growth, fees/guides, market guides, and inquiry.
- The reference pages rely on process explanation, trust/evidence sections, FAQ/contact reassurance, and repeated inquiry triggers.
- The Rocket Growth reference page describes operational preparation before or around inbound: warehouse receipt, inspection, quantity checks, packing/wrapping, barcode/label work, documentation, and logistics-center inbound coordination.
- The GitHub context does not provide a finished production app; the local repository should be treated as a renewal scaffold and planning baseline.

## Inferred NEEDS TRADE requirements
- Reframe NEEDS TRADE as an integrated China sourcing, OEM/ODM, inspection, customs-readiness, warehouse, and Coupang Rocket Growth inbound preparation platform.
- Keep the first implementation target to a public web renewal, quote/request intake, customer workspace boundaries, and admin workspace boundaries.
- Support quote intake paths for product URL inquiry, bulk/Excel inquiry, OEM/ODM sample inquiry, inspection/photo evidence request, and Rocket Growth inbound preparation request.
- Explain service phases as evidence-backed operations rather than unsupported guarantees.
- Keep extension, collectors, and automated 1688 crawling deferred unless a later approved slice defines permissions, session boundaries, compliance review, and API/legal authority.
- Use Rocket Growth wording as China-side preparation and coordination support only.

## Renewal decisions
- Public IA should lead with service clarity and quote conversion rather than a finished marketplace claim.
- Service taxonomy should include China sourcing/purchase agency, OEM/ODM, production coordination, inspection/photo evidence, labeling/barcode/packing, customs and compliance readiness guidance, warehouse handling, and Rocket Growth inbound preparation.
- Customer workspace should be described as a request/status/evidence surface, not as a credential-heavy platform in the first slice.
- Admin workspace should be described as internal triage, quote review, status update, evidence upload, and blocker management.
- Fee/pricing content should remain a guide or inquiry-based estimate until the business owner confirms exact fee rules.
- Any compliance, KC, customs, delivery, or Coupang outcome language must use boundary/disclaimer wording until confirmed by the business owner.

## Observable IA and CTA map
| Role | Clean-room observation | NEEDS TRADE renewal decision |
|---|---|---|
| Primary navigation | Existing/reference pages group services, portfolio/cases, purchase agency, guides, Q&A/contact, and account/workspace concepts. | Use concise navigation: Services, Rocket Growth, Process, Quote, Workspace. Add Portfolio/Fee/FAQ only when approved content exists. |
| Hero | Pages introduce a broad China trade or OEM proposition and show an inquiry path. | State NEEDS TRADE's integrated sourcing/OEM/inbound preparation scope in original language with a primary quote CTA. |
| Service taxonomy | Reference service pages segment sourcing, OEM/ODM, import process, Rocket Growth, guides, and fees. | Create original service pages for sourcing, OEM/ODM, production, inspection/packaging, compliance readiness, and Rocket Growth inbound preparation. |
| Process flow | Reference pages use staged timelines from consultation/request through supplier, warehouse, inspection, packing, shipping, and receipt. | Define NEEDS TRADE status lifecycle in contracts and operations docs, with customer-safe labels and evidence requirements. |
| Evidence/trust | Reference content highlights photos, checks, warehouse receipt, and communication. | Use evidence concepts: receipt counts, inspection checklist, packaging photos, label/barcode records, packing list, blocker notes. |
| Conversion | Inquiry/contact buttons repeat after service explanation. | Repeat quote CTA after hero, service groups, process explanation, Rocket Growth detail, and FAQ. |
| Workspace | Existing NEEDS TRADE purchase agency page implies workspace-based management. | Scope customer workspace as request tracking and evidence viewing; scope admin workspace as triage and status/evidence management. |

## Service taxonomy for renewal
- China sourcing and purchase agency: product URL inquiry, supplier discovery assumptions, quote review, purchase coordination, and status updates.
- OEM/ODM product development: concept/spec intake, sample request, material/packaging requirements, production coordination, and customer approvals.
- Goods production coordination: production plan, supplier milestones, quantity checks, and progress notes.
- Inspection and evidence: warehouse receipt counts, photo evidence, inspection checklist, defect/blocker notes, and customer feedback loop.
- Labeling, barcode, and packaging: label requirements, barcode application, carton preparation, pallet/carton configuration, packing photos, and handoff notes.
- Customs and compliance readiness: document checklist and coordination notes only; no guaranteed clearance, KC certification, origin approval, or legal outcome.
- Warehouse and shipment coordination: China warehouse receipt, consolidation, packing readiness, export/import coordination notes, and shipping handoff.
- Rocket Growth inbound preparation: Coupang-oriented China-side preparation, document/packing coordination, and inbound-support evidence without approval guarantees.

## Customer journey observations
1. Visitor arrives with a product idea, product URL, bulk SKU list, OEM concept, or Coupang inbound need.
2. Visitor scans service scope and confirms NEEDS TRADE can coordinate the relevant China-side work.
3. Visitor checks process/evidence expectations to understand what will be visible after request submission.
4. Visitor submits a quote/request intake form with product details, quantities, desired channel, requested services, and contact method.
5. Operator reviews the request, asks clarification questions, prepares quote assumptions, and updates status.
6. Customer receives quote/status/evidence updates in a workspace boundary once the implementation exists.
7. Admin users manage internal triage, blockers, evidence, and status transitions without exposing operational secrets.

## Clean-room reject list
- Exact slogans, hero headings, service copy, footer/contact phrasing, FAQ answers, or marketing claims from any reference page.
- Reference page HTML, CSS, JavaScript, class names, component names, animation timings, tracking snippets, analytics tags, embedded widgets, hidden text, or structured data.
- Logos, images, icons, screenshots, banners, portfolio visuals, diagrams, file names, or downloaded assets from the reference sites.
- Cookies, session values, credentials, customer account behavior, admin/login behavior, or private platform tokens.
- Strong claims observed in references that imply guaranteed Coupang acceptance, official platform approval, customs clearance, KC certification, delivery date, lowest cost, or rank/status superiority.
- 1688 automation, search federation, API access, or crawling behavior until separately approved with compliance and session-boundary review.

## Open questions
- Which services are directly operated by NEEDS TRADE versus partner-coordinated?
- Which countries, warehouses, and carriers are confirmed for operational claims?
- What specific Rocket Growth documents, labels, barcode formats, pallet/carton rules, and inbound handoff evidence can NEEDS TRADE support today?
- What customer workspace capabilities are approved for the first release: read-only status, evidence attachments, chat, quote approval, or file upload?
- What admin roles and permissions are required for operator, manager, and owner workflows?
- What fee model can be published safely: service categories, ranges, request-based quote, or exact tables?
- What approved brand assets, portfolio cases, customer examples, and evidence photos are available for the renewed site?

## Acceptance criteria
- Reference facts, inferred requirements, and NEEDS TRADE decisions remain separated.
- No exact reference copy, source, asset, hidden value, tracking snippet, or credential is reused.
- Rocket Growth is described as China-side inbound preparation/support only.
- Extension, collectors, and 1688 automation are deferred and guarded.
- The planning package routes first implementation to web renewal, quote intake, and workspace/admin boundaries.
