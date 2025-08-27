from fastapi.testclient import TestClient
from app.main import app  # ajuste para sua app FastAPI real
import pytest

client = TestClient(app)

def test_create_commission_valid():
    data = {
        "transaction_id": "some-valid-uuid",
        "percentage": 5.0
    }
    response = client.post("/commissions/", json=data)
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json.get("transaction_id") == data["transaction_id"]
    assert 0 < resp_json.get("percentage") <= 100

def test_create_commission_invalid_sale_value(mocker):
    # Simule que a transação tem valor 0 para disparar erro
    mocker.patch("app.service.CommissionService.get_calculate_commission", side_effect=Exception("Invalid sale value"))
    data = {
        "transaction_id": "some-valid-uuid",
        "percentage": 5.0
    }
    response = client.post("/commissions/", json=data)
    assert response.status_code == 400

def test_create_commission_invalid_percentage():
    data = {
        "transaction_id": "some-valid-uuid",
        "percentage": 150  # inválido
    }
    response = client.post("/commissions/", json=data)
    assert response.status_code == 400

def test_pay_commission_success(mocker):
    mock_commission = {"commission_id": "id", "paid": False}
    mocker.patch("app.service.CommissionService.pay_commission", return_value={**mock_commission, "paid": True})
    response = client.post("/commissions/id/pay")
    assert response.status_code == 200
    assert response.json().get("paid") is True

def test_pay_commission_not_found(mocker):
    mocker.patch("app.service.CommissionService.pay_commission", side_effect=Exception("Commission not found"))
    response = client.post("/commissions/nonexistent-id/pay")
    assert response.status_code == 404
