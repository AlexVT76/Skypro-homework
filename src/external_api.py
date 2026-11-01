import os

import requests
from dotenv import load_dotenv

load_dotenv()
from typing import Any, Dict, Optional

from requests.exceptions import RequestException

API_URL = "https://api.apilayer.com/currency_data/convert"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        return None

    params = {
        "from": base_currency.upper(),
        "to": target_currency.upper(),
        "amount": 1,
    }
    headers = {"apikey": api_key}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)

        if response.status_code == 403:
            return None
        if not response.ok:
            return None

        data = response.json()

        if data.get("success") is False:
            return None

        result = data.get("result")
        if result is None:
            return None

        return float(result)

    except (RequestException, ValueError, KeyError):
        return None


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> float:
    """Принимает транзакцию  и возвращает сумму в рублях (float)"""
    amount = transaction.get("amount", 0)
    currency = str(transaction.get("currency", "RUB")).upper()

    if currency == "RUB":
        return float(amount)

    rate = get_exchange_rate(currency, "RUB")
    if rate is None:

        return 0.0

    return float(amount * rate)
