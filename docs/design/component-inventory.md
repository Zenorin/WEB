# Component Inventory

## Landing
- `HeroSection` — primary value proposition, reassurance of China sourcing/OEM/logistics support, and a quote CTA.
- `ServiceCards` — distinct cards for China sourcing, OEM/ODM, goods production, inspection/packaging, compliance, Rocket Growth inbound prep.
- `ProcessTimeline` — visual sequence showing request, quote, supplier coordination, inspection, packaging, and inbound readiness.
- `TrustEvidenceStrip` — customer trust markers, evidence concepts, and service transparency.
- `QuoteCTASection` — quote intake call-to-action repeated after the service overview.
- `FAQPreview` — summary of common questions and guidance to the detailed FAQ route.

## Forms
- `QuoteRequestForm` — multi-step or single-page intake for product URL, bulk inquiry, or sample request.
- `ProductUrlInput` — URL field for product sourcing inquiries.
- `BulkInquiryInput` — Excel or batch inquiry description field.
- `RequestedServiceSelector` — checkboxes or cards for sourcing, OEM, inspection, Rocket Growth, and compliance.
- `QuantityInput` — required quantity or order scale.
- `ContactFields` — name, company, phone, email, preferred response method.
- `RemarksField` — product description, target market, desired timeline, and special requirements.
- `SubmitStateBanner` — success, validation error, or form guidance messaging.

## Workspace / status
- `RequestStatusCard` — current request phase, estimated next steps, and reviewer notes.
- `StatusTimeline` — lifecycle progression from request received to completed/cancelled.
- `QuoteSummaryPanel` — captured request details, requested services, and operator comments.
- `EvidencePhotoPanel` — inspection/photo evidence and inbound preparation attachments.
- `BlockerNotice` — clearly surfaced blockers, missing documents, or next action requirements.
- `NextActionPanel` — customer-facing guidance on what to expect next.

## Admin
- `AdminStatusBoard` — internal request queue and stage overview.
- `AdminRequestDetail` — request metadata, operator notes, evidence upload placeholders, and status transition controls.
- `AdminActionList` — task list for quote review, supplier sourcing, inspection scheduling, and inbound coordination.

## Required states
- `loading`
- `empty`
- `validation-error`
- `server-error`
- `success`
- `disabled`
- `permission-denied`
- `unauthenticated`
