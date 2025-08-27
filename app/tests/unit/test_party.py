import pytest
from unittest.mock import MagicMock
from pydantic import ValidationError
from fastapi import HTTPException
from app.service.party import PartyService
from app.schemas import PartyCreate

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_transaction_concrete():
    mock = MagicMock()
    mock.get_transaction_service.return_value.status = "CREATED"
    return mock

@pytest.fixture
def party_service(mock_db, mock_transaction_concrete):
    return PartyService(mock_db, mock_transaction_concrete)

def test_add_party_valid(party_service):
    data = PartyCreate(
        transaction_id="uuid-transacao",
        type="SELLER",
        name="Fulano",
        cpf_cnpj="123.456.789-09",
        email="fulano@example.com"
    )
    mock_party = MagicMock()
    party_service.repository.create_party = MagicMock(return_value=mock_party)
    party_service.repository.find_party_by_cpf_or_email = MagicMock(return_value=None)
    result = party_service.add_party_service(data)
    assert result == mock_party

def test_add_party_invalid_email_format():
    # Passar um email no formato inválido
    with pytest.raises(ValidationError) as excinfo:
        PartyCreate(
            transaction_id="uuid-transacao",
            type="SELLER",
            name="Fulano",
            cpf_cnpj="12345678909",
            email="invalid-email"
        )
    errors = excinfo.value.errors()
    assert any(error['loc'] == ('email',) and error['msg'].startswith('value is not a valid email address') for error in errors)

def test_remove_party_success(party_service):
    mock_party = MagicMock()
    mock_party.transaction_id_fk = "uuid-transacao"
    party_service.repository.get_party_by_id = MagicMock(return_value=mock_party)
    party_service.transaction_concrete.get_transaction_service = MagicMock(return_value=MagicMock(status="CREATED"))
    party_service.repository.delete = MagicMock()
    party_service.remove_party("party-id")
    party_service.repository.delete.assert_called_once_with(mock_party)

def test_remove_party_not_found(party_service):
    party_service.repository.get_party_by_id = MagicMock(return_value=None)
    with pytest.raises(HTTPException):
        party_service.remove_party("nonexistent-id")

def test_remove_party_approved_transaction(party_service):
    mock_party = MagicMock()
    mock_party.transaction_id_fk = "uuid-transacao"
    party_service.repository.get_party_by_id = MagicMock(return_value=mock_party)
    party_service.transaction_concrete.get_transaction_service = MagicMock(return_value=MagicMock(status="APPROVED"))
    with pytest.raises(HTTPException):
        party_service.remove_party("party-id")
