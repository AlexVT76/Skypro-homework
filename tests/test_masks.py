from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тестируем функцию маски карты"""
    assert get_mask_card_number("0000100000000010") == "0000 10** **** 0010"

    assert get_mask_card_number("") == "Не верный номер"

    assert get_mask_card_number("12345678901234567") == "Не верный номер"


def test_get_mask_account() -> None:
    """Тестируем функцию маски счета"""
    assert get_mask_account("987654321") == "**4321"

    assert get_mask_account("4321") == "**4321"

    assert get_mask_account("321") == "Не верный номер"
