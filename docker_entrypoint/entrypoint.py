import logging
from typing import List, Optional

from on_rails import Result, def_result
from pylity.decorators.validate_func_params import validate_func_params
from schema import And, Or, Schema

from docker_entrypoint._libs.cli_parser import create_cli_parser
from docker_entrypoint._libs.commands import (command_about, command_bash,
                                              command_d8, command_run,
                                              command_samples, command_shell)
from docker_entrypoint._libs.DockerEnvironments import DockerEnvironments
from docker_entrypoint._libs.ExitCodes import ExitCode
from docker_entrypoint._libs.Logger import Logger
from docker_entrypoint._libs.ResultDetails.FailResult import FailResult
from docker_entrypoint._libs.utility import class_properties_to_str, log_result


def main(args: Optional[List[str]] = None, logger: Optional[logging.Logger] = None) -> int:
    """
    This is a main function that creates a command-line interface parser, parses the arguments, runs the program, and logs
    the result.
    """

    result = _inner_main(args, logger)

    if not result.success and result.detail and not result.detail.is_instance_of(FailResult):
        print(repr(result))  # Print unexpected error

    if result.success:
        return 0
    return result.code()


@def_result()
@validate_func_params(schema=Schema({
    'logger': Or(None, logging.Logger, error='The logger must be None or type of logging.Logger'),
    'args': Or(None, [str], error='The args must be None or be a list of strings'),
}))
def _inner_main(args: Optional[List[str]] = None, logger: Optional[logging.Logger] = None) -> Result:
    if not logger:
        logger = Logger.get(__name__) \
            .on_fail_break_function() \
            .value

    return create_cli_parser() \
        .on_success(lambda parser: (parser.parse_known_args(args), parser)) \
        .on_success(lambda values: run(values[0], values[1], logger)) \
        .finally_tee(lambda prev_result: log_result(logger, prev_result)
                     .on_fail(lambda res: logger.error("An error occurred while logging Result.\n"
                                                       f"Current Error: {res}\n"
                                                       f"Previous Result: {prev_result}"))
                     ) \
        .on_fail_new_detail(lambda prev_result: FailResult(code=prev_result.code())) \
        .on_success_new_detail(None)


@def_result()
@validate_func_params(schema=Schema({
    'arguments': And(lambda param: param is not None, error='The arguments is required'),
    'parser': And(lambda param: param is not None, error='The parser is required'),
    'logger': And(logging.Logger, error='The logger is required and must be type of logging.Logger'),
}))
def run(arguments, parser, logger: logging.Logger) -> Result:
    """
    This function runs a command with given arguments and logs information about Docker environments and known parameters.

    :param arguments: The `arguments` parameter is a tuple containing two elements: `known_params` and `args`.
    `known_params` is a namespace object containing the parsed command-line arguments that were recognized by the parser,
    while `args` is a list of positional arguments that were not recognized by the parser

    :param parser: `parser` is an instance of the `argparse.ArgumentParser` class, which is used to define and parse
    command-line arguments for the script. It is typically used to define the expected arguments and options, and to
    generate help messages and usage information

    :param logger: The logger parameter is an instance of the logging.Logger class, which is used for logging messages
    during the execution of the run function. It allows the function to output messages of different levels (e.g. debug,
    info, warning, error) to a specified output stream
    :type logger: logging.Logger
    """

    known_params, args = arguments

    return Logger.set_level(debug=known_params.debug) \
        .on_success(lambda: DockerEnvironments.get_environments()) \
        .on_success_tee(lambda environments:
                        (logger.debug(class_properties_to_str(environments, "Environments")),
                         logger.debug(f"known params: {known_params}\nArgs: {args}"))
                        ) \
        .on_success(lambda environments: _run(known_params, args, parser, environments, logger))


@def_result()
def _run(known_params, args, parser, environments: DockerEnvironments, logger: logging.Logger) -> Result:
    """
    Processes commands and arguments passed to it and executes the corresponding command function.

    :param known_params: `known_params` is a named tuple that contains the parsed command line arguments and
    options that are known to the program. It is used to determine which command to execute and what arguments
    to pass to that command.

    :param args: `args` is a list of additional arguments passed to the program.
    It is used in the `_run` function to pass additional arguments to the specific command being executed

    :param parser: `parser` is an instance of the `argparse.ArgumentParser` class, which is used to define
    and parse command-line arguments. It is used to define the expected arguments and options for the
    command-line interface of the program

    :param environments: `environments` is an object of type `DockerEnvironments`, which is a class that
    contains information about the Docker environment being used by the program.
    :type environments: DockerEnvironments
    """

    args = args or []
    if not known_params.command:
        if known_params.version:
            logger.info(f"Program Version: {environments.docker_version}")
            return Result.ok()

        # Print the list of available commands
        parser.print_help()
        return Result.fail(detail=FailResult(code=ExitCode.MISUSE_SHELL_BUILTINS, message="No command specified."))

    # Process the command
    known_params.command = known_params.command.lower()
    if known_params.command == 'run':
        files_and_dirs = known_params.file or []
        files_and_dirs += known_params.directory or []
        return command_run(logger, program=known_params.program, files_and_dirs=files_and_dirs, args=args)
    if known_params.command == 'd8':
        return command_d8(logger, args)
    if known_params.command == 'shell':
        return command_shell(logger, args)
    if known_params.command == 'bash':
        return command_bash(logger, args)
    if known_params.command == 'samples':
        return command_samples(logger, environments)
    if known_params.command == 'about':
        return command_about(logger, environments)

    return Result.ok()  # pragma: no cover


# `if __name__ == '__main__':` is a common Python idiom that checks whether the current script is being
# run as the main program or if it is being imported as a module into another program. If the script is
# being run as the main program, then the `main()` function is called, which is the entry point of the program.
# If the script is being imported as a module, then the `main()` function is not called, and the module can be
# used as a library by other programs.
if __name__ == '__main__':  # pragma: no cover
    code = main()
    raise SystemExit(code)
