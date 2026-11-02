import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()


API_URL = "https://api.apilayer.com/currency_data/convert"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:

    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        print("[DEBUG] get_exchange_rate: no API key, returning None")
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

        rate = float(result)

        return rate

    except (RequestException, ValueError, KeyError) as e:

        return None


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> float:
    op = transaction.get("operationAmount") or {}
    amount_raw = op.get("amount")
    currency_obj = op.get("currency") or {}
    currency = str(currency_obj.get("code", "RUB")).upper()

    try:
        amount = float(amount_raw)
    except (TypeError, ValueError):

        return 0.0

    if currency == "RUB":

        return amount

    rate = get_exchange_rate(currency, "RUB")
    if rate is None:

        return 0.0

    result = amount * rate

    return result
