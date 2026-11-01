import os
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_transaction_to_rub, get_exchange_rate


@patch("src.external_api.requests.get")
def test_get_exchange_rate_returns_rate_from_api_response(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "info": {"quote": 80.67, "timestamp": 1793383926},
        "query": {"amount": 1, "from": "USD", "to": "RUB"},
        "result": 80.67,
        "success": True,
    }
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD", "RUB")
    assert rate == 80.67
    mock_get.assert_called_once()

    _, kwargs = mock_get.call_args
    assert kwargs["params"]["from"] == "USD"
    assert kwargs["params"]["to"] == "RUB"
    assert kwargs["params"]["amount"] == 1


@patch("src.external_api.requests.get")
def test_get_exchange_rate_returns_none_when_success_false(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": 99.99,
        "success": False,
    }
    mock_get.return_value = mock_response

    rate = get_exchange_rate("EUR", "RUB")
    assert rate is None


@patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": ""}, clear=True)
def test_get_exchange_rate_returns_none_when_no_api_key():
    with patch("src.external_api.requests.get") as mock_get:
        rate = get_exchange_rate("USD", "RUB")
        assert rate is None
        mock_get.assert_not_called()


def test_convert_to_rub_rub_amount_returned_as_is():
    tx = {"amount": 1000, "currency": "RUB"}
    result = convert_transaction_to_rub(tx)
    assert result == 1000.0


@patch("src.external_api.get_exchange_rate", return_value=90.5)
def test_convert_to_rub_converts_usd_correctly(mock_get_rate):
    tx = {"amount": 50, "currency": "USD"}
    result = convert_transaction_to_rub(tx)
    assert result == 4525.0
    mock_get_rate.assert_called_once_with("USD", "RUB")


@patch("src.external_api.get_exchange_rate", return_value=95.0)
def test_convert_to_rub_converts_eur_correctly(mock_get_rate):
    tx = {"amount": 40, "currency": "EUR"}
    result = convert_transaction_to_rub(tx)
    assert result == 3800.0
    mock_get_rate.assert_called_once_with("EUR", "RUB")


@patch("src.external_api.get_exchange_rate", return_value=None)
def test_convert_to_rub_returns_zero_when_rate_is_none(mock_get_rate):
    tx = {"amount": 200, "currency": "CNY"}
    result = convert_transaction_to_rub(tx)
    assert result == 0.0
    mock_get_rate.assert_called_once_with("CNY", "RUB")


@patch("src.external_api.get_exchange_rate", return_value=None)
def test_convert_to_rub_returns_zero_when_rate_unavailable(mock_get_rate):
    tx = {"amount": 100, "currency": "CHF"}
    result = convert_transaction_to_rub(tx)

    assert result == 0.0
    mock_get_rate.assert_called_once_with("CHF", "RUB")
