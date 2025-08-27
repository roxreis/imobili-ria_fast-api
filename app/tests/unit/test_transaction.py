import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.service.transaction import TransactionService
from app.schemas import TransactionCreate

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def transaction_service(mock_db):
    return TransactionService(mock_db)

def test_create_transaction_service_valid(transaction_service):
    data = TransactionCreate(property_code="ABC123", sale_value=1000.00)
    mock_transaction = MagicMock()
    transaction_service.repository.create_transaction = MagicMock(return_value=mock_transaction)
    result = transaction_service.create_transaction_service(data)
    assert result == mock_transaction

def test_create_transaction_service_invalid_sale_value(transaction_service):
    data = TransactionCreate(property_code="ABC123", sale_value=0)
    with pytest.raises(HTTPException):
        transaction_service.create_transaction_service(data)

def test_create_transaction_service_empty_property_code(transaction_service):
    data = TransactionCreate(property_code="", sale_value=1000.00)
    with pytest.raises(HTTPException):
        transaction_service.create_transaction_service(data)
