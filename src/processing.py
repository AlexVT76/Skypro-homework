from typing import Any


def filter_by_state(operations: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_operations: list[dict[str, Any]] = []
    for operation in operations:
        if operation.get("state") == state:
            filtered_operations.append(operation)

    return filtered_operations

def sort_by_date(operations: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Сортирует список словарей по значению ключа 'date'"""
    return sorted(operations, key=lambda operation: operation.get('date', ''), reverse=reverse)

