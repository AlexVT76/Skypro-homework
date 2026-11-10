import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Возвращает операции, в описании которых встречается заданная строка.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        transaction
        for transaction in data
        if transaction.get("description") is not None
        and pattern.search(str(transaction["description"]))
    ]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Считает количество операций для каждой категории из списка categories.
    """
    counter = Counter(
        str(transaction.get("description", ""))
        for transaction in data
        if transaction.get("description") is not None
    )
    return {
        category: sum(
            count
            for description, count in counter.items()
            if re.search(re.escape(str(category)), description, re.IGNORECASE)
        )
        for category in categories
    }