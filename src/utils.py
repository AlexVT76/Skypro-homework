import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False


log_file = "logs/utils.log"

file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    logger.debug("Попытка загрузки транзакций из файла: %s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.warning("Файл содержит не список (тип: %s), возвращаем пустой список", type(data).__name__)
            return []

        logger.info("Успешно загружено %d транзакций из %s", len(data), file_path)
        return data

    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path, exc_info=True)
        return []
    except json.JSONDecodeError as e:
        logger.error("Ошибка декодирования JSON в файле %s: %s", file_path, e, exc_info=True)
        return []
    except OSError as e:
        logger.error("Ошибка ввода-вывода при чтении файла %s: %s", file_path, e, exc_info=True)
        return []
