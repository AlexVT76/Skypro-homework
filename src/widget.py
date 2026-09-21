import re
from datetime import datetime
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(text: str) -> str:
    """ Функция обрабатывающая информацию и о картах и о считах"""
    text = str(text)
    account_card = re.search(r"^([A-Za-zА-Яа-я\s]+)\s*(\d+)$", text)
    if account_card:
        letters = account_card.group(1)
        digits = account_card.group(2)
        if letters.lower() == "счет":
            return f"{letters} {get_mask_account(digits)}"
        else:
            return f"{letters} {get_mask_card_number(digits)}"
    else:
        return f"Не верные данные"


def get_date(date_iso: str) -> str:
    """Функция форматирования даты"""
    date_obj = datetime.fromisoformat(date_iso).date()
    formatted = date_obj.strftime("%d.%m.%y")
    return formatted