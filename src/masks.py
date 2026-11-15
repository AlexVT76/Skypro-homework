import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False


log_file = "logs\masks.log"

file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция возвращающая маску номера карты"""
    # Логируем вход (без полного номера!)
    logger.debug("get_mask_card_number вызван с аргументом длины %d", len(str(card_number)))

    card_number = str(card_number)
    if len(card_number) == 16:
        result = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.debug("get_mask_card_number: маска успешно создана")
        return result
    else:
        logger.warning("get_mask_card_number: неверный номер карты (длина %d)", len(card_number))
        return "Не верный номер"


def get_mask_account(account: str) -> str:
    """Функция возвращающая маску номера счета"""
    logger.debug("get_mask_account вызван с аргументом длины %d", len(str(account)))

    account = str(account)
    if len(account) >= 4:
        result = f"**{account[-4:]}"
        logger.debug("get_mask_account: маска успешно создана")
        return result
    else:
        logger.warning("get_mask_account: неверный номер счета (длина %d)", len(account))
        return "Не верный номер"
