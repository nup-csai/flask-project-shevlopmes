import logging
from typing import Optional
from datetime import datetime

class Logger:
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._logger is None:
            # Create logger
            self._logger = logging.getLogger('app_logger')
            self._logger.setLevel(logging.DEBUG)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # Create file handler
            file_handler = logging.FileHandler(f'app_{datetime.now().strftime("%Y%m%d")}.log')
            file_handler.setLevel(logging.INFO)

            # Create formatters
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )

            # Add formatters to handlers
            console_handler.setFormatter(console_formatter)
            file_handler.setFormatter(file_formatter)

            # Add handlers to logger
            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)