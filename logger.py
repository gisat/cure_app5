import logging
from logging import Logger
from pathlib import Path
from typing import Union


def set_logger(logger_name: str, log_file: Union[Path, str]) -> Logger:
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger