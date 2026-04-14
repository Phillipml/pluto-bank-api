from __future__ import annotations

from decimal import Decimal
import importlib
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _reload_app_modules() -> None:
    modules_to_reload = [
        "app.main",
        "app.controllers.transactions",
        "app.controllers.user",
        "app.core.deps",
        "app.core.security",
        "app.models.transaction",
        "app.models.user",
        "app.db.database",
        "app.core.settings",
    ]
    for module_name in modules_to_reload:
        if module_name in sys.modules:
            del sys.modules[module_name]


@pytest.fixture
def client(tmp_path: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-with-32-plus-bytes")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")

    _reload_app_modules()
    app_module = importlib.import_module("app.main")

    with TestClient(app_module.app) as test_client:
        yield test_client


def _create_user(client: TestClient, email: str = "maria@example.com") -> dict:
    response = client.post(
        "/users/create",
        json={
            "name": "Maria Silva",
            "email": email,
            "password": "12345678",
        },
    )
    assert response.status_code == 201
    return response.json()


def _login_and_get_token(client: TestClient, email: str = "maria@example.com") -> str:
    response = client.post(
        "/users/login",
        data={"username": email, "password": "12345678"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_user_login_and_get_me(client: TestClient) -> None:
    created = _create_user(client)
    assert created["email"] == "maria@example.com"
    assert created["amount"] == 0.0

    token = _login_and_get_token(client)
    me_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200

    me = me_response.json()
    assert me["id"] == created["id"]
    assert me["email"] == created["email"]


def test_create_transaction_and_list_my_transactions(client: TestClient) -> None:
    _create_user(client, email="tx@example.com")
    token = _login_and_get_token(client, email="tx@example.com")
    auth_header = {"Authorization": f"Bearer {token}"}

    tx_response = client.post(
        "/transactions/",
        headers=auth_header,
        json={"value": "100.50", "description": "Deposito inicial"},
    )
    assert tx_response.status_code == 201
    tx_payload = tx_response.json()
    assert Decimal(str(tx_payload["transaction"]["value"])) == Decimal("100.50")
    assert tx_payload["user"]["amount"] == 100.5

    list_response = client.get("/transactions/me", headers=auth_header)
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert Decimal(str(items[0]["value"])) == Decimal("100.50")


def test_transaction_rejects_negative_balance(client: TestClient) -> None:
    _create_user(client, email="debit@example.com")
    token = _login_and_get_token(client, email="debit@example.com")

    response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={"value": "-1.00", "description": "Debito"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Saldo insuficiente"
