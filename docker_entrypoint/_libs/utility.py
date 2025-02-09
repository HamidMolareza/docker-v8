import logging
from typing import Callable, Optional

from on_rails import Result, ValidationError, def_result, try_func
from pylity import String
from pylity.decorators.validate_func_params import validate_func_params
from schema import And, Or, Schema, SchemaError

from docker_entrypoint._libs.DockerEnvironments import DockerEnvironments
from docker_entrypoint._libs.ResultDetails.FailResult import FailResult

D8_Recommended_OPTIONS = {
    '--harmony': 'Enables support for some of the experimental ES6 features that are not yet fully standardized',
    '--allow-natives-syntax': 'Enables the use of V8-specific syntax in JavaScript code',
    '--trace-opt': 'Enables logging of V8\'s optimization process',
    '--print-bytecode': 'Prints the generated bytecode for JavaScript functions',
    '--print-opt-code': 'Prints the generated optimized machine code for JavaScript functions',
    '--trace': 'Enables detailed logging of V8 internals',
    '--log-timer-events': 'Enables logging of timer events',
    '--log-gc': 'Enables logging of garbage collection events',
    '--prof': 'Enables CPU profiling',
    '--trace-deopt': 'Enables logging of V8\'s deoptimization process',
    '--trace-ic': 'Enables logging of inline caching events',
}


@def_result()
@validate_func_params(schema=Schema({
    'logger': And(logging.Logger, error='The logger is required and must be type of logging.'),
    'result': And(Result, error='The result is required and must be type of Result.'),
}))
def log_result(logger: logging.Logger, result: Result) -> Result:
    """
    Logs unexpected errors. Results that isn't success and isn't type of FailResult

    :param logger: The logger parameter is an instance of the logging.Logger class, which is used for
    logging messages in the application.
    :type logger: logging.Logger

    :param result: The `result` parameter is an instance of the `Result` class
    :type result: Result
    """

    if result.success:
        if result.value is not None:
            logger.info(result if result.detail else result.value)
        return Result.ok()

    if result.detail is None:
        return Result.ok()  # No data to display

    if isinstance(result.detail, FailResult):
        logger.error(str(result.detail))
        return Result.ok()
    log_error(logger, result)
    return Result.ok()


@def_result()
@validate_func_params(schema=Schema({
    'logger': And(logging.Logger, error='The logger is required and must be type of logging.'),
    'fail_result': And(Result, lambda result: not result.success,
                       error='The fail_result is required and must be type of Result.fail()'),
}))
def log_error(logger: logging.Logger, fail_result: Result) -> Result:
    """
    This function logs an error message and returns a support message if a failure result is encountered.

    :param logger: The logger parameter is an instance of the logging.Logger class.
    :type logger: logging.Logger

    :param fail_result: `fail_result` is an instance of the `Result` class that represents a failed operation.
    It contains information about the failure, such as an error message or exception
    :type fail_result: Result
    """

    logger.error(f"An error occurred:\n{repr(fail_result.detail)}\n")
    return get_support_message() \
        .on_success(lambda support_message:
                    logger.info(f"Please report this error to help others who use this program.\n{support_message}")
                    )


@def_result()
def get_support_message() -> Result[str]:
    """
    This function returns a support message based on the available Docker environments.

    :return: A Result object containing a string message.
    """

    return DockerEnvironments.get_environments() \
        .on_success(lambda environments: _get_support_message(environments))


@def_result()
@validate_func_params(schema=Schema({
    'environments': And(DockerEnvironments,
                        error='environments is required and must be an instance of `DockerEnvironments`')
}))
def _get_support_message(environments: DockerEnvironments) -> Result[str]:
    return Result.ok(value="Support:\n"
                           f"\tMaintainer: {environments.maintainer}\n"
                           f"\tDocker Version: {environments.docker_version}\n"
                           f"\tBuild Date: {environments.build_date}\n"
                           f"\tRepository: {environments.vcs_url}\n"
                           f"\tReport Bug: {environments.bug_report}\n"
                     )


@def_result()
@validate_func_params(schema=Schema({
    'class_object': And(object, lambda param: param is not None,
                        error='The class object is required and must be an instance of a class'),
    'title': Or(None, And(str, lambda s: len(s.strip()) > 0, error='The title must be None or non-empty string'))
}))
def class_properties_to_str(class_object, title: Optional[str] = None) -> Result[str]:
    """
    The function converts the properties of a class object to a string format with an optional title.

    :param class_object: The object of the class whose properties need to be converted to a string
    :type class_object: object

    :param title: The title parameter is an optional string that can be passed to provide additional context or
    information in the resulting string. If no title is provided, the resulting string will only contain the class
    properties
    :type title: Optional[str]

    :return: a Result object that contains a string value. The string value contains the properties of the input class
    object formatted as key-value pairs. If a title is provided, it is included at the beginning of the string. If there
    is an error, a Result object with a ValidationError message is returned.
    """

    has_message = not String.is_none_or_empty(title)
    result = f"{title}:\n" if has_message else ""
    tab = '\t' if has_message else ''
    for key, value in vars(class_object).items():
        result += f"{tab}{key}: {value}\n"
    return Result.ok(value=result)


@def_result()
@validate_func_params(schema=Schema({
    'code': And(int, error='The code is required and must be integer')
}))
def convert_code_to_result(code: int) -> Result:
    """
    The function converts a code to a Result object, returning an OK result if the code is 0 and a FailResult object
    otherwise.

    :param code: an integer representing the result code of an operation
    :type code: int
    """

    if code == 0:
        return Result.ok()
    return Result.fail(FailResult(code=code))


@def_result()
@validate_func_params(schema=Schema({
    'validation_func': And(lambda x: callable(x), error='The validation_func is required and must be a function')
}))
def try_validation(validation_func: Callable) -> Result:
    """
    It executes the validation_func function. If an SchemaError is raised, it returns the error result
    with ValidationError. If there is an exception other than SchemaError, it returns the error details
    from the ErrorDetail type. If successful, it returns Result.ok().

    :param validation_func: The parameter `validation_func` is a callable function that returns schema.Schema and
    maybe raise an exception like SchemaError. For example: lambda: schema.validate(...)
    :type validation_func: Callable

    :return: The function `try_validation` returns a `Result` object. If the `try_func` call within the function
    `try_validation` raises a `SchemaError` exception, the function returns a `Result` object with a `ValidationError`
    message. Otherwise, it returns the `Result` object returned by the `try_func` call.
    """

    result = try_func(validation_func)
    if result.success:
        return result

    if result.detail and result.detail.exception and isinstance(result.detail.exception, SchemaError):
        return Result.fail(ValidationError(message=str(result.detail.exception)))
    return result
