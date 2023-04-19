import logging
import os
from typing import List, Optional

from on_rails import Result, ValidationError, def_result
from pylity import Path
from pylity.decorators.validate_func_params import validate_func_params
from schema import And, Or, Schema

from docker_entrypoint._libs.DockerEnvironments import DockerEnvironments
from docker_entrypoint._libs.ExitCodes import ExitCode
from docker_entrypoint._libs.ResultDetails.FailResult import FailResult
from docker_entrypoint._libs.utility import (class_properties_to_str,
                                             convert_code_to_result)


@validate_func_params(Schema({
    'logger': And(logging.Logger, error='logger is required and must be a logging.Logger object'),
    'program': And(And(str, error='The program must be a string'), And(str.strip, lambda s: len(s) > 0,
                   error='The program can not be empty or whitespace')),
    'files_and_dirs': Or(None, [str], error='files_and_dirs must be a list of strings or None'),
    'args': Or(None, [str], error='args must be a list of strings or None'),
}))
def command_run(logger: logging.Logger, program: str, files_and_dirs: Optional[List[str]] = None,
                args: Optional[List[str]] = None) -> Result:
    """
    Runs a javascript source with optional arguments and files/directories as input, and logs the output.

    :param logger: A logging.Logger object used for logging messages
    :type logger: logging.Logger

    :param program: The path to the JavaScript program that needs to be executed
    :type program: str

    :param files_and_dirs: The `files_and_dirs` parameter is a list of file paths and directory paths that
    the program will use as input. If this parameter is not provided, an empty list will be used
    :type files_and_dirs: Optional[List[str]]

    :param args: args is a list of command line arguments to be passed to the program being run.
    It is an optional parameter and defaults to an empty list if not provided
    :type args: Optional[List[str]]

    :return: a `Result` object. The `Result` object can either be a success or a failure.
    If it is a success, it returns `Result.ok()`. If it is a failure, it returns
    `Result.fail(FailResult(code=ExitCode.IO_ERROR))` or `result` depending on the value
    of `result` in the function.
    """

    if not os.path.isfile(program):
        return Result.fail(FailResult(code=ExitCode.IO_ERROR, message=f"File '{program}' does not exists."))

    files_and_dirs = files_and_dirs or []
    args = args or []

    result = Path.collect_files(files_and_dirs)
    if not result.success:
        if result.detail.is_instance_of(ValidationError):
            return Result.fail(FailResult(code=ExitCode.IO_ERROR, message=str(result.detail)))
        return result  # pragma: no cover
    files: List[str] = result.value

    if len(files) == 0:
        logger.warning("No file provided.")
        command = f"bash -c 'd8 {program}'"
        logger.debug(f"command: {command}")
        code = os.system(command)
        logger.debug(f"Return Code: {code}")
        return convert_code_to_result(code)

    final_code = 0
    logger.debug(f"Number of input files: {len(files)}")
    files.sort()
    for index, file in enumerate(files):
        logger.info(f"file {index + 1}: {file}")
        command = f"bash -c 'd8 {program} {' '.join(args)} < {file}'"
        logger.debug(f"command: {command}")
        code = os.system(command)
        logger.debug(f"Return Code: {code}")
        print('----------------------------------------------------------------')
        if code != 0:  # pragma: no cover
            final_code = code

    return convert_code_to_result(final_code)


@def_result()
@validate_func_params(schema=Schema({
    'logger': And(logging.Logger, error='logger is required and must be a logging.Logger object'),
    'args': Or(None, [str], error='args must be a list of strings or None'),
}))
def command_d8(logger: logging.Logger, args: Optional[List[str]] = None) -> Result:
    """
    Runs the D8 Shell with optional arguments and logs the command and a message for exiting the shell.

    :param logger: A logging.Logger object used for logging messages related to the execution of the command
    :type logger: logging.Logger

    :param args: args is a list of optional command line arguments that will be passed to the d8 command.
    It can be None or an empty list if no arguments are needed.
    :type args: Optional[List[str]]

    :return: a `Result` object that indicates success or failure of the command execution.
    """

    logger.debug(f"Command: d8 {' '.join(args)}")
    logger.info("Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell")

    code = os.system(f"d8 {' '.join(args)}")

    logger.debug(f"Return code: {code}")
    return convert_code_to_result(code)


@def_result()
@validate_func_params(schema=Schema({
    'logger': And(logging.Logger, error='logger is required and must be a logging.Logger object'),
    'args': Or(None, [str], error='args must be a list of strings or None'),
}))
def command_shell(logger: logging.Logger, args: Optional[List[str]] = None) -> Result:
    """
    This function runs a shell with default options and optional arguments, using the D8 Shell.

    :param logger: A logging.Logger object used for logging messages
    :type logger: logging.Logger

    :param args: args is a list of optional arguments that can be passed to the command_shell function.
    These arguments will be added to the default_options list and used as options for the D8 Shell command
    :type args: Optional[List[str]]
    """

    default_options = ['--harmony', '--allow-natives-syntax']
    bash_command = ['sleep 0.5;', 'rlwrap', '-m', '-pgreen', 'd8'] + default_options + args

    command_str = f"bash -c '{' '.join(bash_command)}'"
    logger.debug(f"Command: {command_str}")

    logger.info(f"Default options: {default_options}")
    logger.info("Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell")

    code = os.system(command_str)

    logger.debug(f"Return code: {code}")
    return convert_code_to_result(code)


@def_result()
@validate_func_params(schema=Schema({
    'logger': And(logging.Logger, error='logger is required and must be a logging.Logger object'),
    'args': Or(None, [str], error='args must be a list of strings or None'),
}))
def command_bash(logger: logging.Logger, args: Optional[List[str]] = None) -> Result:
    """
    Runs a bash command with optional arguments and logs the command and its execution.

    :param logger: A logging.Logger object used for logging messages
    :type logger: logging.Logger

    :param args: args is a list of strings that represent the arguments to be passed to the bash command.
    These arguments will be joined together with spaces to form the full command string that will be executed.
    :type args: Optional[List[str]]
    """

    command_str = f"bash {' '.join(args)}"
    logger.debug(f"Command: {command_str}")
    logger.info("Running bash command. Use --help to see other commands.")

    code = os.system(command_str)

    logger.debug(f"Return code: {code}")
    return convert_code_to_result(code)


@def_result()
@validate_func_params(schema=Schema({
    'logger': And(logging.Logger, error='logger is required and must be a logging.Logger object'),
    'environments': And(DockerEnvironments,
                        error='environments is required and must be an instance of `DockerEnvironments`')
}))
def command_samples(logger: logging.Logger, environments: DockerEnvironments) -> Result:
    """
    The function provides sample commands for using Docker image.

    :param logger: A logging.Logger object used for logging messages
    :type logger: logging.Logger

    :param environments: The `environments` parameter is an object of type `DockerEnvironments`, which likely contains
    information about the Docker environment being used, such as the Docker image name
    :type environments: DockerEnvironments
    """

    result = "Use -h or --help for more information about commands.\n"
    result += "Samples:\n"
    result += f"\tdocker run --rm -it {environments.docker_name} run " \
              f"/samples/say-hello.js -f /samples/sample-inputs/0.txt -d /samples/sample-inputs :\t" \
              f"Execute sample javascript with sample inputs\n"
    result += f"\tdocker run --rm -it -v $PWD:/solution {environments.docker_name} run " \
              f"/solution/program.js -d /solution/sample-inputs :\t" \
              f"Execute your local javascript program with your local inputs\n"
    result += f"\tdocker run --rm -it {environments.docker_name} shell :\t" \
              "starts enhanced d8 shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name} d8 :\t" \
              f"starts default d8 shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name} bash :\t" \
              "starts a bash shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name} :\tstarts a bash shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name} --version :\tdisplays the program version\n"

    logger.info(result)
    return Result.ok()


@def_result()
@validate_func_params(schema=Schema({
    'logger': And(logging.Logger, error='logger is required and must be a logging.Logger object'),
    'environments': And(DockerEnvironments,
                        error='environments is required and must be an instance of `DockerEnvironments`')
}))
def command_about(logger: logging.Logger, environments: DockerEnvironments) -> Result:
    """
    This function logs information about the Docker like maintainer, version, built date, etc.

    :param logger: A logging.Logger object used for logging messages
    :type logger: logging.Logger

    :param environments: The function takes this parameter as an argument and returns a log message with
    information about the program or application being executed
    :type environments: DockerEnvironments
    """

    return class_properties_to_str(environments, title="About") \
        .on_success(lambda about_message: logger.info(about_message))
