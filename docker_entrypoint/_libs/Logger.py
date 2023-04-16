import logging
from typing import Optional


class Logger:
    """
    The singleton `Logger` class provides methods to create and configure a logger object for
    logging messages with a specified name and level.
    """

    _logger: Optional[logging.Logger] = None

    @staticmethod
    def get(name: str):
        """
        Returns a logger object with a specified name and adds a console handler to it if it doesn't already
        exist.

        :param name: The name parameter is a string that represents the name of the logger.
        It is used to identify the logger instance and differentiate it from other loggers
        :type name: str

        :return: the logger object created by the `logging.getLogger(name)` method.
        """

        if Logger._logger is None:
            Logger._logger = logging.getLogger(name)
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            Logger._logger.addHandler(console_handler)
        return Logger._logger

    @staticmethod
    def set_level(debug: Optional[bool], name: Optional[str] = None):
        """
        This function sets the logging level of a logger to either DEBUG or INFO based on
        the value of the debug parameter.

        :param debug: The `debug` parameter is a boolean flag that indicates whether the logging level
        should be set to `DEBUG` or `INFO`. If `debug` is `True`, the logging level will be set to `DEBUG`,
        otherwise it will be set to `INFO`
        :type debug: Optional[bool]

        :param name: The `name` parameter is an optional string that represents the name of the logger.
        :type name: Optional[str]
        """

        Logger.get(name).setLevel(logging.DEBUG if debug else logging.INFO)
