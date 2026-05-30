"""End-to-end wiring tests for the product API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app
from app.services.product_service import get_product_service


def make_client() -> TestClient:
    # Reset the singleton so each test starts with an empty in-memory store.
    get_product_service.cache_clear()
    return TestClient(create_app())


def test_health() -> None:
    client = make_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_product_crud_flow() -> None:
    client = make_client()
    payload = {"name": "Widget", "sku": "WID-1", "price": "9.99", "quantity": 5}

    created = client.post("/api/v1/products", json=payload)
    assert created.status_code == 201
    product_id = created.json()["id"]

    assert len(client.get("/api/v1/products").json()) == 1
    assert client.get(f"/api/v1/products/{product_id}").json()["name"] == "Widget"

    # Duplicate SKU is rejected.
    assert client.post("/api/v1/products", json=payload).status_code == 409

    updated = client.patch(f"/api/v1/products/{product_id}", json={"quantity": 10})
    assert updated.status_code == 200
    assert updated.json()["quantity"] == 10

    assert client.delete(f"/api/v1/products/{product_id}").status_code == 204
    assert client.get(f"/api/v1/products/{product_id}").status_code == 404
