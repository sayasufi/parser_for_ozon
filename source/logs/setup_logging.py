import logging


def setup_logging(log_file):
    """Создаем функцию инициализирующую логгер"""
    # Создаем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    # Создаем форматтер для логов
    formatter = logging.Formatter("%(levelname)s\t%(asctime)s\t%(message)s")
    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(
        logging.Formatter("%(levelname)s - %(message)s")
    )
    logger.addHandler(stdout_handler)

    return logger
