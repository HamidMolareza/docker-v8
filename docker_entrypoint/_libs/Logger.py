import logging
from typing import Optional


class Logger:
    _logger: Optional[logging.Logger] = None

    @staticmethod
    def get(name: str):
        if Logger._logger is not None:
            Logger._logger = logging.getLogger(name)
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            Logger._logger.addHandler(console_handler)
        return Logger._logger

    @staticmethod
    def set_level(verbose: Optional[bool]):
        Logger._logger.setLevel(logging.DEBUG if verbose else logging.INFO)
