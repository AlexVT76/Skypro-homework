def filter_by_currency(transactions, currency):
    """Функция возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной"""
    return (x for x in transactions if x["operationAmount"]["currency"]["code"] == currency)


def transaction_descriptions(transactions):
    """Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        if transaction["description"]:
            yield transaction["description"]


def card_number_generator(start, end):
    """Функция-генератор номера карты"""
    card_number: str = "0000000000000000"

    for iteration in range(int(end + 1) - int(start)):

        start = str(int(start))
        form_cards: str = ""

        card_number = "0" * (len(card_number) - len(start)) + start
        start = str(int(start) + 1)

        for i, num in enumerate(card_number):
            if i > 3 and i % 4 == 0:
                form_cards += " "
            form_cards += num

        yield form_cards
