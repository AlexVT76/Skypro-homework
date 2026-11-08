from unittest.mock import patch

import pandas as pd

from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel


def test_read_transactions_from_csv_success(caplog):
    caplog.set_level(10)  # DEBUG и выше
    mock_df = pd.DataFrame([
        {"id": "89531", "state": "EXECUTED", "date": "2024-01-01", "amount": "1000"}
    ])

    with patch("pandas.read_csv", return_value=mock_df):
        result = read_transactions_from_csv("fake.csv")

    assert len(result) == 1
    assert result[0]["id"] == "89531"
    assert any("Успешно считано 1 транзакций" in record.message for record in caplog.records)


def test_read_transactions_from_excel_success(caplog):
    caplog.set_level(10)
    mock_df = pd.DataFrame([
        {"id": "89532", "state": "CANCELED", "date": "2024-01-02", "amount": "500"}
    ])

    with patch("pandas.read_excel", return_value=mock_df):
        result = read_transactions_from_excel("fake.xlsx")

    assert len(result) == 1
    assert result[0]["state"] == "CANCELED"
    assert any("Успешно считано 1 транзакций" in record.message for record in caplog.records)