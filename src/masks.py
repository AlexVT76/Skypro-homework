def get_mask_card_number(card_number: str) -> str:
    """Функция возвращающая маску номера карты"""
    card_number = str(card_number)
    if len(card_number) == 16:
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    else:
        return f"Не верный номер"


def get_mask_account(account: str) -> str:
    """Функция возвращающая маску номера счета"""
    account = str(account)
    if len(account) >= 4:
        return f"**{account[-4:]}"
    else:
        return f"Не верный номер"
