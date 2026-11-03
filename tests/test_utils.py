import json
from unittest.mock import patch

import pytest

from src.utils import load_transactions


@patch("json.load")
@patch("builtins.open")
def test_load_transactions_handles_invalid_json(mock_open, mock_load):
    mock_open.return_value = mock_open

    mock_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

    result = load_transactions("data/broken.json")

    assert result == []
    mock_open.assert_called_once_with("data/broken.json", "r", encoding="utf-8")
    mock_load.assert_called_once()


@patch("json.load")
@patch("builtins.open")
def test_load_transactions_returns_empty_list_when_data_is_not_a_list(mock_open, mock_load):
    mock_open.return_value = mock_open

    mock_load.return_value = {"total": 12345, "currency": "RUB"}

    result = load_transactions("data/not_list.json")

    assert result == []
    mock_open.assert_called_once_with("data/not_list.json", "r", encoding="utf-8")
    mock_load.assert_called_once()


@patch("json.load")
@patch("builtins.open")
def test_load_transactions_returns_valid_list(mock_open, mock_load):
    mock_open.return_value = mock_open
    mock_load.return_value = [
        {"amount": 100, "currency": "RUB"},
        {"amount": 50, "currency": "USD"},
    ]

    result = load_transactions("data/operations.json")

    assert result == [
        {"amount": 100, "currency": "RUB"},
        {"amount": 50, "currency": "USD"},
    ]
    mock_open.assert_called_once_with("data/operations.json", "r", encoding="utf-8")
    mock_load.assert_called_once()
