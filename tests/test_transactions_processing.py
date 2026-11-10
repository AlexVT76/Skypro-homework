import pytest

from src.transactions_processing import process_bank_operations, process_bank_search


def test_process_bank_search_returns_list(transactions_processing):
    result = process_bank_search(transactions_processing, "перевод")
    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)


def test_process_bank_search_case_insensitive(transactions_processing):
    # Ищем "перевод" — должны найти все варианты регистра
    result = process_bank_search(transactions_processing, "перевод")
    ids = {t["id"] for t in result}
    assert ids == {1, 3, 4, 6}


def test_process_bank_search_middle_substring(transactions_processing):
    result = process_bank_search(transactions_processing, "вклада")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_process_bank_search_no_match_empty_list(transactions_processing):
    assert process_bank_search(transactions_processing, "кредит") == []


def test_process_bank_search_empty_query_returns_all(transactions_processing):
    result = process_bank_search(transactions_processing, "")
    assert len(result) == len(transactions_processing)


def test_process_bank_search_missing_description_does_not_crash():
    # Транзакция без поля description
    txs = [{"id": 1, "amount": 100}]
    assert process_bank_search(txs, "перевод") == []


def test_process_bank_operations_counts_categories(transactions_processing):
    categories = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада"]
    stats = process_bank_operations(transactions_processing, categories)

    # Ожидаемые количества по нашим данным
    assert stats["Перевод организации"] == 3
    assert stats["Перевод с карты на карту"] == 1
    assert stats["Открытие вклада"] == 1


def test_process_bank_operations_counts_categories(transactions_processing):
    categories = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада"]
    stats = process_bank_operations(transactions_processing, categories)
    assert stats == {
        "Перевод организации": 3,
        "Перевод с карты на карту": 1,
        "Открытие вклада": 1,
    }


def test_process_bank_operations_unknown_category_counts_zero(transactions_processing):
    """Категория без совпадений попадает в результат со значением 0."""
    categories = ["Неизвестная категория", "Перевод организации"]
    stats = process_bank_operations(transactions_processing, categories)
    assert stats == {"Неизвестная категория": 0, "Перевод организации": 3}


def test_process_bank_operations_empty_transactions(transactions_processing):
    stats = process_bank_operations([], ["Перевод организации", "Открытие вклада"])
    assert stats == {"Перевод организации": 0, "Открытие вклада": 0}


def test_process_bank_operations_empty_categories(transactions_processing):
    """Пустой список категорий — пустой словарь."""
    assert process_bank_operations(transactions_processing, []) == {}
