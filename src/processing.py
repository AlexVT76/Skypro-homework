from typing import Any


def filter_by_state(operations: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_operations: list[dict[str, Any]] = []
    for operation in operations:
        if operation.get("state") == state:
            filtered_operations.append(operation)

    return filtered_operations
