import logging
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False


log_file ="logs\ transaction_reader.log"

file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV .
    Возвращает список словарей.
    """
    logger.debug("Попытка чтения CSV-файла через pandas: %s", file_path)
    try:
        df = pd.read_csv(file_path, dtype=str)
        transactions = df.to_dict(orient="records")
        logger.info("Успешно считано %d транзакций из CSV: %s", len(transactions), file_path)
        return transactions
    except FileNotFoundError:
        logger.error("CSV-файл не найден: %s", file_path, exc_info=True)
        return []
    except Exception as e:
        logger.error("Ошибка при чтении CSV через pandas: %s — %s", file_path, e, exc_info=True)
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel .
    Возвращает список словарей.
    """
    logger.debug("Попытка чтения Excel-файла через pandas: %s", file_path)
    try:

        df = pd.read_excel(file_path, dtype=str)
        transactions = df.to_dict(orient="records")
        logger.info("Успешно считано %d транзакций из Excel: %s", len(transactions), file_path)
        return transactions
    except FileNotFoundError:
        logger.error("Excel-файл не найден: %s", file_path, exc_info=True)
        return []
    except Exception as e:
        logger.error("Ошибка при чтении Excel через pandas: %s — %s", file_path, e, exc_info=True)
        return []
