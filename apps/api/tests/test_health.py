from fastapi.testclient import TestClient

from app.main import app, create_quote_request_envelope, health, normalize_quote_request_input


client = TestClient(app)


def valid_product_url_payload() -> dict[str, object]:
    return {
        "requesterName": "Kim Seller",
        "contact": "seller@example.com",
        "requestTypes": ["product_url"],
        "requestedServices": ["china_sourcing", "purchase_agency"],
        "productUrl": "https://fixtures.example/product/123",
        "quantity": 100,
    }


def issue_fields(response_body: dict[str, object]) -> set[tuple[str, str]]:
    issues = response_body["error"]["issues"]  # type: ignore[index]
    return {(issue["field"], issue["code"]) for issue in issues}


def test_health() -> None:
    assert health()["status"] == "ok"


def test_health_endpoint_still_passes() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_product_url_quote_request_returns_success_envelope() -> None:
    response = client.post("/api/quote-requests", json=valid_product_url_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["requestId"].startswith("quote_")
    assert body["data"]["requestId"] == body["requestId"]
    assert body["data"]["accepted"] is True
    assert body["data"]["status"] == "request_received"
    assert body["data"]["validationIssues"] == []
    assert body["data"]["input"]["requesterName"] == "Kim Seller"
    assert body["data"]["input"]["contact"] == "seller@example.com"
    assert body["data"]["input"]["productUrl"] == "https://fixtures.example/product/123"


def test_deterministic_envelope_matches_contract_id_and_timestamp_shape() -> None:
    envelope = create_quote_request_envelope(valid_product_url_payload(), now="2026-05-12T00:00:00.000Z")

    assert envelope["requestId"] == "quote_20260512T000000000Z"
    assert envelope["createdAt"] == "2026-05-12T00:00:00.000Z"
    assert envelope["updatedAt"] == "2026-05-12T00:00:00.000Z"
    assert envelope["accepted"] is True


def test_normalization_trims_basic_string_fields() -> None:
    payload = valid_product_url_payload()
    payload["requesterName"] = "  Kim Seller  "
    payload["contact"] = " seller@example.com "
    payload["productUrl"] = " https://fixtures.example/product/123 "

    normalized = normalize_quote_request_input(payload)

    assert normalized["requesterName"] == "Kim Seller"
    assert normalized["contact"] == "seller@example.com"
    assert normalized["productUrl"] == "https://fixtures.example/product/123"


def test_missing_requester_name_returns_validation_issue() -> None:
    payload = valid_product_url_payload()
    payload["requesterName"] = " "

    response = client.post("/api/quote-requests", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert ("requesterName", "required") in issue_fields(body)


def test_product_url_without_product_url_returns_validation_issue() -> None:
    payload = valid_product_url_payload()
    payload.pop("productUrl")

    response = client.post("/api/quote-requests", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert ("productUrl", "required") in issue_fields(body)


def test_bulk_excel_without_file_intent_or_item_count_returns_validation_issue() -> None:
    payload = valid_product_url_payload()
    payload["requestTypes"] = ["bulk_excel"]
    payload.pop("productUrl")
    payload.pop("quantity")

    response = client.post("/api/quote-requests", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert ("bulkFileIntent", "required") in issue_fields(body)


def test_rocket_growth_inbound_without_quantity_returns_validation_issue() -> None:
    payload = valid_product_url_payload()
    payload["requestTypes"] = ["rocket_growth_inbound"]
    payload["requestedServices"] = ["rocket_growth_inbound_prep"]
    payload.pop("productUrl")
    payload.pop("quantity")

    response = client.post("/api/quote-requests", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert ("quantity", "required") in issue_fields(body)


def test_secret_like_field_name_is_rejected() -> None:
    payload = valid_product_url_payload()
    payload["sessionToken"] = "fixture-only"

    response = client.post("/api/quote-requests", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert ("sessionToken", "forbidden_secret_like_field") in issue_fields(body)


def test_secret_like_value_is_rejected() -> None:
    payload = valid_product_url_payload()
    payload["productDescription"] = "password=fixture-secret"

    response = client.post("/api/quote-requests", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert ("productDescription", "forbidden_secret_like_value") in issue_fields(body)


def test_unknown_top_level_field_is_rejected_without_mock_success() -> None:
    payload = valid_product_url_payload()
    payload["platformGuarantee"] = "approved"

    response = client.post("/api/quote-requests", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "validation_failed"
    assert ("platformGuarantee", "unsupported_field") in issue_fields(body)
