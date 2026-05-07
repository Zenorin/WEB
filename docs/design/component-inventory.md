# Component Inventory

## Design principles
- Components should support dense, practical service evaluation and request conversion.
- Use original NEEDS TRADE copy and owner-approved assets only.
- Components must expose customer/admin boundaries clearly.
- Every route must support loading, empty, error, success, disabled, unauthenticated, and permission-denied states where relevant.

## Public layout components
| Component | Role | Key content | States |
|---|---|---|---|
| `SiteHeader` | Primary navigation and quote entry | Services, Process, Rocket Growth, Quote, Workspace | default, mobile-open |
| `FooterBoundaryNotice` | Trust/contact/footer boundary | Contact placeholders, policy links, service disclaimer | default |
| `HeroSection` | Renewal proposition and conversion | Integrated China sourcing/OEM/inbound preparation positioning | default |
| `ServiceCategoryGrid` | Service taxonomy | Sourcing, OEM/ODM, production, inspection/packaging, compliance readiness, Rocket Growth prep | loading, populated |
| `ServiceBoundaryCallout` | Claim guardrail | What NEEDS TRADE supports, coordinates, and does not guarantee | default |
| `ProcessTimeline` | Status lifecycle preview | Request, quote, supplier/sample, warehouse, inspection, packaging, inbound prep, shipping, complete | loading, populated |
| `EvidencePreviewStrip` | Evidence expectations | Receipt count, inspection photos, label/barcode, packing list, blocker notes | empty, populated |
| `RocketGrowthPrepPanel` | Rocket Growth-specific conversion | China-side receipt, quantity check, labels, packing, inbound coordination | default |
| `FAQPreview` | Reduce conversion hesitation | Fees, timing, inspection, compliance boundaries, workspace | loading, populated |
| `QuoteCTASection` | Repeated conversion | Request type prompt and CTA | default, disabled |

## Service detail components
| Component | Role |
|---|---|
| `ServiceHero` | Service-specific summary and quote CTA with guardrail text. |
| `ServiceScopeList` | Supported tasks, coordination tasks, deferred tasks, and unsupported guarantees. |
| `ServiceEvidenceList` | Evidence/output examples for the selected service. |
| `ServiceProcessSteps` | Customer-safe process steps mapped to operational statuses. |
| `ServiceRequirementsChecklist` | Inputs required from customer before quote review. |
| `ServiceFAQList` | Service-specific questions with boundary-safe answers. |

## Quote intake components
| Component | Role | Validation |
|---|---|---|
| `QuoteRequestForm` | Main intake wrapper | submit disabled until minimum required fields are valid |
| `RequestTypeSelector` | Product URL, bulk inquiry, OEM/ODM, inspection/evidence, Rocket Growth prep | at least one request path |
| `ProductUrlInput` | Source product URL | optional unless selected path requires URL |
| `BulkInquiryInput` | Multi-SKU or Excel description placeholder | optional text now; file upload deferred until storage approval |
| `OemSpecFields` | Concept, material, size, packaging, sample notes | optional unless OEM/ODM selected |
| `InboundPrepFields` | SKU, label/barcode, carton/pallet, target channel, timing | optional unless Rocket Growth selected |
| `RequestedServiceSelector` | Service category multi-select | at least one service |
| `QuantityInput` | Requested quantity | positive integer when present |
| `SalesChannelSelector` | Coupang, Smartstore, retail, corporate, other | optional |
| `ContactFields` | Name, company, email, phone, preferred contact | name, email, preferred contact required |
| `EvidenceExpectationField` | Photo/checklist/evidence needs | optional |
| `ComplianceQuestionField` | Customs/KC/origin/document questions | optional and advisory |
| `ConsentNotice` | Privacy and no-credential boundary | must not request passwords, cookies, or tokens |
| `SubmitStateBanner` | Result or validation feedback | validation-error, submitting, success, server-error |

## Customer workspace components
| Component | Role | Visibility |
|---|---|---|
| `WorkspaceRequestList` | Customer request cards and filters | customer-only |
| `RequestStatusCard` | Current stage and next action | customer-safe fields only |
| `StatusTimeline` | Lifecycle from request received to completion/cancelled | customer-safe labels |
| `QuoteSummaryPanel` | Request details, selected services, quote status | customer-safe fields only |
| `EvidenceGallery` | Photos/documents/checklists approved for customer view | hides internal-only files |
| `BlockerNotice` | Missing info or issue requiring action | customer-visible blocker reason |
| `NextActionPanel` | What customer should do or expect next | customer-visible instructions |
| `WorkspaceEmptyState` | No requests yet | points to quote route |

## Admin components
| Component | Role | Guardrails |
|---|---|---|
| `AdminRequestQueue` | Internal triage list with status filters | admin-only |
| `AdminRequestDetail` | Full request metadata and operations context | protects secrets and internal-only fields |
| `AdminStatusTransitionControls` | Move request through allowed statuses | validates legal transitions |
| `OperatorNotesPanel` | Internal notes and assumptions | never shown directly to customer |
| `EvidenceManager` | Upload/link approved evidence artifacts | file storage implementation deferred |
| `BlockerEditor` | Set blocker reason and customer next action | separates internal note from public message |
| `CustomerUpdateDraft` | Draft customer-visible update | requires review before send in future slice |
| `AdminAuditPlaceholder` | Future audit trail surface | no production audit claim until implemented |

## Required UI states
- `loading`: data is being fetched or submitted.
- `empty`: no requests, no evidence, or no service examples are available.
- `validation-error`: user input fails contract validation.
- `server-error`: request failed or service is unavailable.
- `success`: quote request submitted or admin save completed.
- `disabled`: action blocked until required fields/permissions are ready.
- `permission-denied`: authenticated user lacks access.
- `unauthenticated`: login is required for workspace/admin routes.
- `not-found`: request ID or route object does not exist.
- `blocked`: operation is paused due to missing information or issue resolution.

## Deferred component candidates
- `FileUploadDropzone`: requires approved file storage, retention, virus scanning, and privacy policy.
- `ChatThread`: requires notification, retention, and moderation rules.
- `PaymentSummary`: requires payment provider and settlement policy.
- `ExtensionImportButton`: requires extension approval and message contract.
- `MarketplaceSearchWidget`: requires approved API/legal authority and session-boundary review.
