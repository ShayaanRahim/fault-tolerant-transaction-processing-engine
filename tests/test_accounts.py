from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_fetch_account():
    resp = client.post("/accounts", json={"name": "test-acct", "type": "liability"})
    assert resp.status_code == 201

    account_id = resp.json()["id"]

    got = client.get(f"/accounts/{account_id}")
    assert got.status_code == 200
    assert got.json()["name"] == "test-acct"
    # no ledger entries exist yet, so balance must be exactly zero
    assert got.json()["balance"] == "0"


def test_missing_account_returns_404():
    resp = client.get("/accounts/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404