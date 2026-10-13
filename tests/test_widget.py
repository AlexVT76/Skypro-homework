import pytest

from src.widget import get_date, mask_account_card


def test_get_date(make_iso: str) -> None:

    result = get_date(make_iso)

    assert result == "11.03.24"


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("", "Не верные данные"),
    ],
)
def test_mask_account_card(text: str, expected: str) -> None:
    assert mask_account_card(text) == expected
