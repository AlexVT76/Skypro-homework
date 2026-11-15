"""Главная точка входа: меню, фильтрация и вывод транзакций."""
from src.transactions_processing  import process_bank_search
from src.transaction_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    load_transactions_from_json,
)


VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}
DATE_FORMAT = "%d.%m.%Y"


def format_transaction(transaction: dict) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    date = str(transaction.get("date", ""))[:10]
    if date:
        try:
            from datetime import datetime

            date = datetime.strptime(date, "%Y-%m-%d").strftime(DATE_FORMAT)
        except ValueError:
            pass

    lines = [date, str(transaction.get("description", "Без описания"))]
    from_ = transaction.get("from")
    to = transaction.get("to")
    if from_ or to:
        arrow = f"{from_} -> {to}" if from_ and to else (from_ or to)
        lines.append(str(arrow))
    amount = transaction.get("amount", transaction.get("operationAmount", {}).get("amount", "?"))
    currency = transaction.get(
        "currency_name",
        transaction.get("operationAmount", {}).get("currency", {}).get("name", ""),
    )
    lines.append(f"Сумма: {amount} {currency}".strip())
    return "\n".join(lines)


def ask_yes_no(question: str) -> bool:
    """Задаёт вопрос с ответом Да/Нет, повторяет при некорректном вводе."""
    while True:
        answer = input(question + " Да/Нет\nПользователь: ").strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print("Пожалуйста, ответьте Да или Нет.")


def choose_status() -> str:
    """Запрашивает статус, пока пользователь не введёт корректный."""
    while True:
        print(
            'Введите статус, по которому необходимо выполнить фильтрацию. '
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        status = input("Пользователь: ").strip().upper()
        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        print(f'Статус операции "{status}" недоступен.')


def load_transactions() -> list[dict]:
    """Выводит меню выбора файла и читает транзакции."""
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями. "
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )
    choice = input("Пользователь: ").strip()
    path = input("Введите имя файла: ").strip()

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return load_transactions_from_json(path)
    if choice == "2":
        print("Для обработки выбран CSV-файл.")
        return read_transactions_from_csv(path)
    if choice == "3":
        print("Для обработки выбран XLSX-файл.")
        return read_transactions_from_excel(path)
    print("Такого пункта меню нет.")
    return load_transactions()


def main() -> None:
    """Основная логика программы."""
    transactions = load_transactions()

    # Фильтрация по статусу (регистронезависимая)
    status = choose_status()
    transactions = [
        t for t in transactions if str(t.get("state", "")).upper() == status
    ]

    # Сортировка по дате
    if ask_yes_no("Отсортировать операции по дате?"):
        direction = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        reverse = direction == "по убыванию"
        transactions = sorted(
            transactions,
            key=lambda t: str(t.get("date", "")),
            reverse=reverse,
        )

    # Только рублёвые транзакции
    if ask_yes_no("Выводить только рублевые транзакции?"):
        transactions = [
            t
            for t in transactions
            if str(
                t.get("currency_name", t.get("operationAmount", {}).get("currency", {}).get("name", ""))
            ).upper() == "РУБ"
        ]

    # Поиск по слову в описании
    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search = input("Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, search)

    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for transaction in transactions:
        print(format_transaction(transaction))

if __name__ == "__main__":
    main()