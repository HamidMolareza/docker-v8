#!/usr/bin/env python3

import os

from on_rails import Result, def_result

from docker_entrypoint._libs.cli_parser import create_cli_parser
from docker_entrypoint._libs.commands import command_run
from docker_entrypoint._libs.docker_environments import DockerEnvironments
from docker_entrypoint._libs.ExitCodes import ExitCode
from docker_entrypoint._libs.Logger import Logger
from docker_entrypoint._libs.ResultDetails.FailResult import FailResult
from docker_entrypoint._libs.utility import (log_debug_class_properties,
                                             log_result)

logger = Logger.get(__name__)


def main():
    result = create_cli_parser() \
        .on_success(lambda parser: (parser.parse_known_args(), parser)) \
        .on_success(lambda values: run(values[0], values[1])) \
        .finally_tee(log_result)
    if result.success:
        raise SystemExit(0)
    else:
        raise SystemExit(result.code)


@def_result()
def run(arguments, parser) -> Result:
    known_params, args = arguments

    Logger.set_level(verbose=known_params.verbose)

    return DockerEnvironments.get_environments() \
        .on_success_tee(lambda environments:
                        log_debug_class_properties(logger, environments, "Environments")
                        .on_success(lambda: logger.debug(f"known params: {known_params}\nArgs: {args}"))
                        ) \
        .on_success(lambda environments: _run(known_params, args, parser, environments))


@def_result()
def _run(known_params, args, parser, environments) -> Result:
    args = args or []
    if not known_params.command:
        if known_params.version:
            logger.info(f"Program version: {environments.docker_version}")
            return Result.ok()

        # Print the list of available commands
        logger.debug("No command specified. Available commands:")
        parser.print_help()

        return Result.fail(FailResult(code=ExitCode.MISUSE_SHELL_BUILTINS))

    # Process the command
    if known_params.command == 'run':
        return command_run(logger, program=known_params.program, files_and_dirs=known_params.file,
                           directories=known_params.directory, args=args)
    if known_params.command == 'd8':
        logger.debug(f"Command: d8 {' '.join(args)}")
        logger.info("Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell")
        os.system(f"d8 {' '.join(args)}")
        return Result.ok()
    if known_params.command == 'help':
        result = "Use -h or --help for more information about commands\n"
        result += "Sample Usage:\n"
        result += f"\tdocker run --rm -it {environments.docker_name}\t: starts default d8 shell\n"
        result += f"\tdocker run --rm -it {environments.docker_name} shell\t: " \
                  "starts enhanced d8 shell with the given arguments\n"
        result += f"\tdocker run --rm -it {environments.docker_name} bash\t: " \
                  "starts a bash shell with the given arguments\n"
        result += f"\tdocker run --rm -it {environments.docker_name} --version\t: displays the program version\n"

        logger.info(result)
        return Result.ok()
    if known_params.command == 'shell':
        bash_command = ['sleep 0.5;', 'rlwrap', '-m', '-pgreen', 'd8'] + args

        command_str = f"bash -c '{' '.join(bash_command)}'"
        logger.debug(f"Command: {command_str}")
        logger.info("Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell")
        os.system(command_str)
    elif known_params.command == 'bash':
        bash_arguments = args
        command_str = f"bash {' '.join(bash_arguments)}"
        logger.debug(f"Command: {command_str}")
        os.system(command_str)
    else:
        print(f'Unknown command: {known_params.command}')
        parser.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass  # Ignore keyboard interrupt
