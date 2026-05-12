from datetime import UTC, datetime
import re
from typing import Any

from fastapi import FastAPI, Request

app = FastAPI(title="Project API")


QUOTE_REQUEST_TYPES = [
    "product_url",
    "bulk_excel",
    "oem_odm_sample",
    "rocket_growth_inbound",
    "inspection_photo_evidence",
    "general_consultation",
]

SALES_CHANNELS = [
    "coupang",
    "rocket_growth",
    "smartstore",
    "retail",
    "corporate",
    "other",
]

REQUESTED_SERVICES = [
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
]

OPERATION_EVIDENCE_TYPES = [
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
]

DEFAULT_QUOTE_REQUEST_INPUT = {
    "requesterName": "",
    "contact": "",
    "requestTypes": [],
    "requestedServices": [],
}

OPTIONAL_QUOTE_INPUT_FIELDS = [
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
]

FORBIDDEN_FIELD_RE = re.compile(
    r"(?:api[_-]?key|access[_-]?token|auth[_-]?token|bearer|cookie|credential|"
    r"password|passwd|private[_-]?key|secret|session)",
    re.IGNORECASE,
)
FORBIDDEN_VALUE_RE = re.compile(
    r"(?:bearer\s+[a-z0-9._-]+|cookie\s*:|set-cookie|api[_-]?key\s*[:=]|"
    r"access[_-]?token\s*[:=]|password\s*[:=]|session(?:id)?\s*[:=])",
    re.IGNORECASE,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/quote-requests")
async def create_quote_request(request: Request) -> dict[str, Any]:
    envelope = create_quote_request_envelope(await request.json())

    if envelope["accepted"]:
        return {"ok": True, "data": envelope, "requestId": envelope["requestId"]}

    return {
        "ok": False,
        "error": {
            "code": "validation_failed",
            "message": "Quote request validation failed.",
            "issues": envelope["validationIssues"],
        },
        "requestId": envelope["requestId"],
    }


def create_quote_request_envelope(input_value: Any, now: str | None = None) -> dict[str, Any]:
    timestamp = now or datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validation_issues = validate_quote_request_input(input_value)
    request_id = f"quote_{re.sub(r'[^0-9A-Za-z]', '', timestamp)}"

    return {
        "requestId": request_id,
        "accepted": len(validation_issues) == 0,
        "status": "request_received",
        "createdAt": timestamp,
        "updatedAt": timestamp,
        "input": normalize_quote_request_input(input_value),
        "validationIssues": validation_issues,
    }


def normalize_quote_request_input(input_value: Any) -> dict[str, Any]:
    raw = as_record(input_value)
    normalized = {
        **DEFAULT_QUOTE_REQUEST_INPUT,
        "requesterName": as_string(raw.get("requesterName")) or DEFAULT_QUOTE_REQUEST_INPUT["requesterName"],
        "contact": as_string(raw.get("contact")) or DEFAULT_QUOTE_REQUEST_INPUT["contact"],
        "requestTypes": as_string_array(raw.get("requestTypes"), QUOTE_REQUEST_TYPES),
        "requestedServices": as_string_array(raw.get("requestedServices"), REQUESTED_SERVICES),
    }

    for field in [
        "requesterCompany",
        "productUrl",
        "productName",
        "productDescription",
        "oemSampleNotes",
        "rocketGrowthInboundNotes",
        "inspectionPhotoEvidenceNotes",
        "generalConsultationNotes",
        "targetTimeline",
    ]:
        value = as_string(raw.get(field))
        if value:
            normalized[field] = value

    if raw.get("preferredContactMethod") in ["email", "phone", "chat"]:
        normalized["preferredContactMethod"] = raw["preferredContactMethod"]

    quantity = as_positive_integer(raw.get("quantity"))
    if quantity is not None:
        normalized["quantity"] = quantity

    item_count = as_positive_integer(raw.get("itemCount"))
    if item_count is not None:
        normalized["itemCount"] = item_count

    bulk_file_intent = as_boolean(raw.get("bulkFileIntent"))
    if bulk_file_intent is not None:
        normalized["bulkFileIntent"] = bulk_file_intent

    sales_channels = as_string_array(raw.get("salesChannels"), SALES_CHANNELS)
    if sales_channels:
        normalized["salesChannels"] = sales_channels

    evidence_requested = as_string_array(raw.get("evidenceRequested"), OPERATION_EVIDENCE_TYPES)
    if evidence_requested:
        normalized["evidenceRequested"] = evidence_requested

    return normalized


def validate_quote_request_input(input_value: Any) -> list[dict[str, str]]:
    raw = as_record(input_value)
    normalized = normalize_quote_request_input(raw)
    issues = collect_secret_like_issues(input_value)

    if not normalized["requesterName"]:
        issues.append({"field": "requesterName", "code": "required", "message": "Requester name is required."})

    if not normalized["contact"]:
        issues.append({"field": "contact", "code": "required", "message": "Contact is required."})

    if len(normalized["requestedServices"]) == 0:
        issues.append(
            {
                "field": "requestedServices",
                "code": "required",
                "message": "At least one requested service is required.",
            }
        )

    if "product_url" in normalized["requestTypes"] and not normalized.get("productUrl"):
        issues.append(
            {
                "field": "productUrl",
                "code": "required",
                "message": "Product URL is required for product URL inquiries.",
            }
        )

    if (
        "bulk_excel" in normalized["requestTypes"]
        and normalized.get("bulkFileIntent") is not True
        and normalized.get("itemCount") is None
    ):
        issues.append(
            {
                "field": "bulkFileIntent",
                "code": "required",
                "message": "Bulk Excel inquiries require bulk file intent or item count.",
            }
        )

    if (
        "oem_odm_sample" in normalized["requestTypes"]
        or "rocket_growth_inbound" in normalized["requestTypes"]
    ) and normalized.get("quantity") is None:
        issues.append(
            {
                "field": "quantity",
                "code": "required",
                "message": "Quantity is required for OEM/ODM sample and Rocket Growth inbound requests.",
            }
        )

    for key, value in raw.items():
        if key not in DEFAULT_QUOTE_REQUEST_INPUT and key not in OPTIONAL_QUOTE_INPUT_FIELDS:
            issues.append(
                {
                    "field": key,
                    "code": "unsupported_field",
                    "message": "Unsupported fields are not accepted by the quote intake contract.",
                }
            )

        if isinstance(value, str) and len(value) != len(value.strip()):
            issues.append(
                {
                    "field": key,
                    "code": "invalid_value",
                    "message": "String fields must not rely on leading or trailing whitespace.",
                }
            )

    return issues


def collect_secret_like_issues(value: Any, path: str = "") -> list[dict[str, str]]:
    if isinstance(value, list):
        issues = []
        for index, item in enumerate(value):
            issues.extend(collect_secret_like_issues(item, f"{path}[{index}]"))
        return issues

    if isinstance(value, dict):
        issues = []
        for key, child in value.items():
            field_path = f"{path}.{key}" if path else str(key)
            if FORBIDDEN_FIELD_RE.search(str(key)):
                issues.append(
                    {
                        "field": field_path,
                        "code": "forbidden_secret_like_field",
                        "message": "Secret-like fields are not accepted by the quote intake contract.",
                    }
                )
            issues.extend(collect_secret_like_issues(child, field_path))
        return issues

    if isinstance(value, str) and FORBIDDEN_VALUE_RE.search(value):
        return [
            {
                "field": path or "$",
                "code": "forbidden_secret_like_value",
                "message": "Secret-like values are not accepted by the quote intake contract.",
            }
        ]

    return []


def as_record(input_value: Any) -> dict[str, Any]:
    return input_value if isinstance(input_value, dict) else {}


def as_string(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) else None


def as_string_array(value: Any, allowed: list[str]) -> list[str]:
    if not isinstance(value, list):
        return []

    out = []
    for item in value:
        if isinstance(item, str) and item in allowed and item not in out:
            out.append(item)
    return out


def as_positive_integer(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    return value if isinstance(value, int) and value > 0 else None


def as_boolean(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None
