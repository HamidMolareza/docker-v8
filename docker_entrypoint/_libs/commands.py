import logging
import os
from typing import List, Optional

from on_rails import Result, ValidationError, def_result
from pylity import Path

from docker_entrypoint._libs.docker_environments import DockerEnvironments
from docker_entrypoint._libs.ExitCodes import ExitCode
from docker_entrypoint._libs.ResultDetails.FailResult import FailResult


@def_result()
def command_run(logger: logging.Logger, program: str, files_and_dirs: Optional[List[str]],
                args: Optional[List[str]]) -> Result:
    if not os.path.isfile(program):
        logger.error(f"File {program} does not exists.")
        return Result.fail(FailResult(code=ExitCode.IO_ERROR))

    files_and_dirs = files_and_dirs or []
    args = args or []

    result = Path.collect_files(files_and_dirs)
    if not result.success:
        if result.detail.is_instance_of(ValidationError):
            logger.error(result)
            return Result.fail(FailResult(code=ExitCode.IO_ERROR))
        return result
    files: List[str] = result.value

    if len(files) == 0:
        logger.warning("No file provided.")
        os.system(f"bash -c 'd8 {program}'")
        return Result.ok()

    for index, file in enumerate(files):
        logger.info(f"file {index + 1}: {file}")
        os.system(f"bash -c 'd8 {program} {' '.join(args)} < {file}'")
        print('----------------------------------------------------------------')
    return Result.ok()


@def_result()
def command_d8(logger: logging.Logger, args: Optional[List[str]]) -> Result:
    logger.debug(f"Command: d8 {' '.join(args)}")
    logger.info("Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell")
    os.system(f"d8 {' '.join(args)}")
    return Result.ok()


@def_result()
def command_shell(logger: logging.Logger, args: Optional[List[str]]) -> Result:
    default_options = ['--harmony', '--allow-natives-syntax']
    bash_command = ['sleep 0.5;', 'rlwrap', '-m', '-pgreen', 'd8'] + default_options + args

    command_str = f"bash -c '{' '.join(bash_command)}'"
    logger.debug(f"Command: {command_str}")
    logger.info(f"Default options: {default_options}")
    logger.info("Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell")
    os.system(command_str)
    return Result.ok()


@def_result()
def command_bash(logger: logging.Logger, args: Optional[List[str]]) -> Result:
    command_str = f"bash {' '.join(args)}"
    logger.debug(f"Command: {command_str}")
    logger.info("Running bash command. Use --help to see other commands.")
    os.system(command_str)
    return Result.ok()


@def_result()
def command_samples(logger: logging.Logger, environments: DockerEnvironments) -> Result:
    result = "Use -h or --help for more information about commands.\n"
    result += "Samples:\n"
    result += f"\tdocker run --rm -it {environments.docker_name} run " \
              f"/samples/say-hello.js -f /samples/sample-inputs/0.txt -d /samples/sample-inputs\n"
    result += f"\tdocker run --rm -it {environments.docker_name} shell\t: " \
              "starts enhanced d8 shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name} d8\t: " \
              f"starts default d8 shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name} bash\t: " \
              "starts a bash shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name}\t: starts a bash shell with the given arguments\n"
    result += f"\tdocker run --rm -it {environments.docker_name} --version\t: displays the program version\n"

    logger.info(result)
    return Result.ok()
