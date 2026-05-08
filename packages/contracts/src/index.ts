export const QUOTE_REQUEST_TYPES = [
  "product_url",
  "bulk_excel",
  "oem_odm_sample",
  "rocket_growth_inbound",
  "inspection_photo_evidence",
  "general_consultation",
] as const;

export type QuoteRequestType = (typeof QUOTE_REQUEST_TYPES)[number];

export const SALES_CHANNELS = [
  "coupang",
  "rocket_growth",
  "smartstore",
  "retail",
  "corporate",
  "other",
] as const;

export type SalesChannel = (typeof SALES_CHANNELS)[number];

export const REQUESTED_SERVICES = [
  "china_sourcing",
  "purchase_agency",
  "bulk_excel_inquiry",
  "oem_odm",
  "sample_request",
  "production_coordination",
  "inspection_photo_evidence",
  "labeling_barcode_packaging",
  "china_warehouse",
  "customs_readiness",
  "shipping_inbound_coordination",
  "rocket_growth_inbound_prep",
  "general_consultation",
] as const;

export type RequestedService = (typeof REQUESTED_SERVICES)[number];

export const OPERATION_STATUSES = [
  "request_received",
  "reviewing",
  "supplier_discovery",
  "quote_preparing",
  "quote_sent",
  "sample_requested",
  "sample_reviewing",
  "production_pending",
  "production_running",
  "china_warehouse_received",
  "inspection_running",
  "labeling_packaging",
  "customs_shipping",
  "rocket_growth_inbound_prep",
  "inbound_complete",
  "completed",
  "blocked",
  "cancelled",
] as const;

export type OperationStatus = (typeof OPERATION_STATUSES)[number];

export const OPERATION_STAGES = [
  "intake",
  "supplier_discovery",
  "quote",
  "sample",
  "production",
  "china_warehouse",
  "inspection",
  "labeling_packaging",
  "compliance_support",
  "shipping_inbound",
  "completion",
  "blocked",
  "cancelled",
] as const;

export type OperationStage = (typeof OPERATION_STAGES)[number];

export const OPERATION_EVIDENCE_TYPES = [
  "request_summary",
  "supplier_candidate",
  "quote_assumption",
  "sample_photo",
  "sample_review_note",
  "production_schedule",
  "warehouse_receipt_count",
  "inspection_checklist",
  "inspection_photo",
  "defect_note",
  "label_barcode_record",
  "packing_carton_note",
  "pallet_preparation_note",
  "customs_document_checklist",
  "shipping_coordination_note",
  "rocket_growth_inbound_checklist",
  "customer_visible_note",
  "blocker_reason",
  "completion_summary",
] as const;

export type OperationEvidenceType = (typeof OPERATION_EVIDENCE_TYPES)[number];

export const ROCKET_GROWTH_INBOUND_STATUSES = [
  "not_started",
  "requirements_reviewing",
  "china_warehouse_received",
  "quantity_checking",
  "inspection_photo_evidence",
  "labeling_barcode_packaging",
  "carton_pallet_preparation",
  "document_coordination",
  "inbound_handoff_ready",
  "inbound_support_complete",
  "blocked",
  "cancelled",
] as const;

export type RocketGrowthInboundStatus = (typeof ROCKET_GROWTH_INBOUND_STATUSES)[number];

export interface QuoteRequestInput {
  requesterName: string;
  requesterCompany?: string;
  contact: string;
  preferredContactMethod?: "email" | "phone" | "chat";
  requestTypes: QuoteRequestType[];
  requestedServices: RequestedService[];
  salesChannels?: SalesChannel[];
  productUrl?: string;
  productName?: string;
  productDescription?: string;
  quantity?: number;
  itemCount?: number;
  bulkFileIntent?: boolean;
  oemSampleNotes?: string;
  rocketGrowthInboundNotes?: string;
  inspectionPhotoEvidenceNotes?: string;
  generalConsultationNotes?: string;
  targetTimeline?: string;
  evidenceRequested?: OperationEvidenceType[];
}

export interface QuoteRequestValidationIssue {
  field: string;
  code:
    | "required"
    | "invalid_value"
    | "unsupported_field"
    | "forbidden_secret_like_field"
    | "forbidden_secret_like_value";
  message: string;
}

export interface QuoteRequestEnvelope {
  requestId: string;
  accepted: boolean;
  status: OperationStatus;
  createdAt: string;
  updatedAt: string;
  input: QuoteRequestInput;
  validationIssues: QuoteRequestValidationIssue[];
}

export interface OperationEvidence {
  id: string;
  type: OperationEvidenceType;
  title: string;
  description?: string;
  createdAt: string;
  customerVisible: boolean;
  source: "customer" | "operator" | "partner" | "system";
  status?: OperationStatus;
  metadata?: Record<string, string | number | boolean | null>;
}

export interface OperationTimelineEvent {
  id: string;
  status: OperationStatus;
  stage: OperationStage;
  happenedAt: string;
  customerVisible: boolean;
  message?: string;
  evidenceIds?: string[];
}

export interface OperationRecord {
  operationId: string;
  quoteRequestId: string;
  status: OperationStatus;
  stage: OperationStage;
  requestedServices: RequestedService[];
  salesChannels?: SalesChannel[];
  timeline: OperationTimelineEvent[];
  evidence: OperationEvidence[];
  blockerReason?: string;
  customerVisibleNote?: string;
  operatorNotes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface RocketGrowthInboundChecklistItem {
  id: string;
  label: string;
  status: "not_started" | "in_progress" | "blocked" | "complete" | "not_applicable";
  required: boolean;
  evidenceTypes: OperationEvidenceType[];
  customerVisible: boolean;
  blockerReason?: string;
}

export interface RocketGrowthInboundRecord {
  inboundId: string;
  quoteRequestId: string;
  status: RocketGrowthInboundStatus;
  operationStatus: OperationStatus;
  sku?: string;
  productName?: string;
  quantity: number;
  salesChannel: Extract<SalesChannel, "coupang" | "rocket_growth">;
  checklist: RocketGrowthInboundChecklistItem[];
  evidence: OperationEvidence[];
  createdAt: string;
  updatedAt: string;
  customerVisibleNote?: string;
  blockerReason?: string;
}

const TERMINAL_OPERATION_STATUSES = ["completed", "cancelled"] as const satisfies readonly OperationStatus[];

const DEFAULT_QUOTE_REQUEST_INPUT: QuoteRequestInput = {
  requesterName: "",
  contact: "",
  requestTypes: [],
  requestedServices: [],
};

const FORBIDDEN_FIELD_RE = /(?:api[_-]?key|access[_-]?token|auth[_-]?token|bearer|cookie|credential|password|passwd|private[_-]?key|secret|session)/i;
const FORBIDDEN_VALUE_RE = /(?:bearer\s+[a-z0-9._-]+|cookie\s*:|set-cookie|api[_-]?key\s*[:=]|access[_-]?token\s*[:=]|password\s*[:=]|session(?:id)?\s*[:=])/i;

function asString(value: unknown): string | undefined {
  return typeof value === "string" ? value.trim() : undefined;
}

function asStringArray<T extends string>(value: unknown, allowed: readonly T[]): T[] {
  if (!Array.isArray(value)) return [];
  const allowedSet = new Set<string>(allowed);
  const out: T[] = [];
  for (const item of value) {
    if (typeof item === "string" && allowedSet.has(item) && !out.includes(item as T)) {
      out.push(item as T);
    }
  }
  return out;
}

function asPositiveInteger(value: unknown): number | undefined {
  return typeof value === "number" && Number.isInteger(value) && value > 0 ? value : undefined;
}

function asBoolean(value: unknown): boolean | undefined {
  return typeof value === "boolean" ? value : undefined;
}

function asRecord(input: unknown): Record<string, unknown> {
  return input !== null && typeof input === "object" && !Array.isArray(input)
    ? (input as Record<string, unknown>)
    : {};
}

function collectSecretLikeIssues(value: unknown, path = ""): QuoteRequestValidationIssue[] {
  if (Array.isArray(value)) {
    return value.flatMap((item, index) => collectSecretLikeIssues(item, `${path}[${index}]`));
  }

  if (value !== null && typeof value === "object") {
    return Object.entries(value as Record<string, unknown>).flatMap(([key, child]) => {
      const fieldPath = path ? `${path}.${key}` : key;
      const keyIssue: QuoteRequestValidationIssue[] = FORBIDDEN_FIELD_RE.test(key)
        ? [
            {
              field: fieldPath,
              code: "forbidden_secret_like_field",
              message: "Secret-like fields are not accepted by the quote intake contract.",
            },
          ]
        : [];
      return [...keyIssue, ...collectSecretLikeIssues(child, fieldPath)];
    });
  }

  if (typeof value === "string" && FORBIDDEN_VALUE_RE.test(value)) {
    return [
      {
        field: path || "$",
        code: "forbidden_secret_like_value",
        message: "Secret-like values are not accepted by the quote intake contract.",
      },
    ];
  }

  return [];
}

export function normalizeQuoteRequestInput(input: unknown): QuoteRequestInput {
  const raw = asRecord(input);
  const normalized: QuoteRequestInput = {
    ...DEFAULT_QUOTE_REQUEST_INPUT,
    requesterName: asString(raw.requesterName) ?? DEFAULT_QUOTE_REQUEST_INPUT.requesterName,
    contact: asString(raw.contact) ?? DEFAULT_QUOTE_REQUEST_INPUT.contact,
    requestTypes: asStringArray(raw.requestTypes, QUOTE_REQUEST_TYPES),
    requestedServices: asStringArray(raw.requestedServices, REQUESTED_SERVICES),
  };

  const optionalStringFields = [
    "requesterCompany",
    "productUrl",
    "productName",
    "productDescription",
    "oemSampleNotes",
    "rocketGrowthInboundNotes",
    "inspectionPhotoEvidenceNotes",
    "generalConsultationNotes",
    "targetTimeline",
  ] as const;

  for (const field of optionalStringFields) {
    const value = asString(raw[field]);
    if (value) normalized[field] = value;
  }

  if (
    raw.preferredContactMethod === "email" ||
    raw.preferredContactMethod === "phone" ||
    raw.preferredContactMethod === "chat"
  ) {
    normalized.preferredContactMethod = raw.preferredContactMethod;
  }

  const quantity = asPositiveInteger(raw.quantity);
  if (quantity !== undefined) normalized.quantity = quantity;

  const itemCount = asPositiveInteger(raw.itemCount);
  if (itemCount !== undefined) normalized.itemCount = itemCount;

  const bulkFileIntent = asBoolean(raw.bulkFileIntent);
  if (bulkFileIntent !== undefined) normalized.bulkFileIntent = bulkFileIntent;

  const salesChannels = asStringArray(raw.salesChannels, SALES_CHANNELS);
  if (salesChannels.length > 0) normalized.salesChannels = salesChannels;

  const evidenceRequested = asStringArray(raw.evidenceRequested, OPERATION_EVIDENCE_TYPES);
  if (evidenceRequested.length > 0) normalized.evidenceRequested = evidenceRequested;

  return normalized;
}

export function validateQuoteRequestInput(input: unknown): QuoteRequestValidationIssue[] {
  const raw = asRecord(input);
  const normalized = normalizeQuoteRequestInput(raw);
  const issues = collectSecretLikeIssues(input);

  if (!normalized.requesterName) {
    issues.push({ field: "requesterName", code: "required", message: "Requester name is required." });
  }

  if (!normalized.contact) {
    issues.push({ field: "contact", code: "required", message: "Contact is required." });
  }

  if (normalized.requestedServices.length === 0) {
    issues.push({
      field: "requestedServices",
      code: "required",
      message: "At least one requested service is required.",
    });
  }

  if (normalized.requestTypes.includes("product_url") && !normalized.productUrl) {
    issues.push({
      field: "productUrl",
      code: "required",
      message: "Product URL is required for product URL inquiries.",
    });
  }

  if (
    normalized.requestTypes.includes("bulk_excel") &&
    normalized.bulkFileIntent !== true &&
    normalized.itemCount === undefined
  ) {
    issues.push({
      field: "bulkFileIntent",
      code: "required",
      message: "Bulk Excel inquiries require bulk file intent or item count.",
    });
  }

  if (
    (normalized.requestTypes.includes("oem_odm_sample") ||
      normalized.requestTypes.includes("rocket_growth_inbound")) &&
    normalized.quantity === undefined
  ) {
    issues.push({
      field: "quantity",
      code: "required",
      message: "Quantity is required for OEM/ODM sample and Rocket Growth inbound requests.",
    });
  }

  for (const [key, value] of Object.entries(raw)) {
    if (!(key in DEFAULT_QUOTE_REQUEST_INPUT) && !isKnownOptionalQuoteInputField(key)) {
      issues.push({
        field: key,
        code: "unsupported_field",
        message: "Unsupported fields are not accepted by the quote intake contract.",
      });
    }

    if (typeof value === "string" && value.length !== value.trim().length) {
      issues.push({
        field: key,
        code: "invalid_value",
        message: "String fields must not rely on leading or trailing whitespace.",
      });
    }
  }

  return issues;
}

export function createQuoteRequestEnvelope(input: unknown, now = new Date().toISOString()): QuoteRequestEnvelope {
  const normalizedInput = normalizeQuoteRequestInput(input);
  const validationIssues = validateQuoteRequestInput(input);
  const requestId = `quote_${now.replace(/[^0-9A-Za-z]/g, "")}`;

  return {
    requestId,
    accepted: validationIssues.length === 0,
    status: "request_received",
    createdAt: now,
    updatedAt: now,
    input: normalizedInput,
    validationIssues,
  };
}

export function isTerminalOperationStatus(status: OperationStatus): boolean {
  return TERMINAL_OPERATION_STATUSES.includes(status as (typeof TERMINAL_OPERATION_STATUSES)[number]);
}

function isKnownOptionalQuoteInputField(key: string): key is Exclude<keyof QuoteRequestInput, keyof typeof DEFAULT_QUOTE_REQUEST_INPUT> {
  return [
    "requesterCompany",
    "preferredContactMethod",
    "salesChannels",
    "productUrl",
    "productName",
    "productDescription",
    "quantity",
    "itemCount",
    "bulkFileIntent",
    "oemSampleNotes",
    "rocketGrowthInboundNotes",
    "inspectionPhotoEvidenceNotes",
    "generalConsultationNotes",
    "targetTimeline",
    "evidenceRequested",
  ].includes(key);
}
