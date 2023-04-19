import logging
from typing import Optional

from on_rails import Result, def_result
from pylity.decorators.validate_func_params import validate_func_params
from schema import And, Or, Schema


class Logger:
    """
    The singleton `Logger` class provides methods to create and configure a logger object for
    logging messages with a specified name and level.
    """

    _logger: Optional[logging.Logger] = None

    @staticmethod
    @def_result()
    @validate_func_params(schema=Schema({
        'name': Or(None, And(str, str.strip, lambda s: len(s) > 0),
                   error='The name must be None or a (non empty) string.')
    }))
    def get(name: Optional[str] = None) -> Result[logging.Logger]:
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
            Logger._logger.setLevel(logging.INFO)
        return Result.ok(Logger._logger)

    @staticmethod
    @def_result()
    @validate_func_params(schema=Schema({
        'debug': Or(None, bool, error='The debug must be None or boolean.'),
        'name': Or(None, And(str, str.strip, lambda s: len(s) > 0),
                   error='The name must be None or a (non empty) string.')
    }))
    def set_level(debug: Optional[bool], name: Optional[str] = None) -> Result:
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

        return Logger.get(name) \
            .on_success(lambda logger: logger.setLevel(logging.DEBUG if debug else logging.INFO))
