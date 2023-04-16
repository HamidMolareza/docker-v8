#!/usr/bin/env python3

from on_rails import Result, def_result

from docker_entrypoint._libs.cli_parser import create_cli_parser
from docker_entrypoint._libs.commands import (command_bash, command_d8,
                                              command_run, command_samples,
                                              command_shell)
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
        .on_fail_break_function() \
        .on_success(lambda values: run(values[0], values[1])) \
        .finally_tee(lambda prev_result: log_result(logger, prev_result))
    if result.success:
        raise SystemExit(0)
    else:
        raise SystemExit(result.code())


@def_result()
def run(arguments, parser) -> Result:
    known_params, args = arguments

    Logger.set_level(debug=known_params.debug)

    return DockerEnvironments.get_environments() \
        .on_success_tee(lambda environments:
                        log_debug_class_properties(logger, environments, "Environments")
                        .on_success(lambda: logger.debug(f"known params: {known_params}\nArgs: {args}"))
                        ) \
        .on_success(lambda environments: _run(known_params, args, parser, environments))


@def_result()
def _run(known_params, args, parser, environments: DockerEnvironments) -> Result:
    args = args or []
    if not known_params.command:
        if known_params.version:
            logger.info(f"Program Version: {environments.docker_version}")
            return Result.ok()

        # Print the list of available commands
        logger.debug("No command specified.")
        parser.print_help()
        return Result.fail(detail=FailResult(code=ExitCode.MISUSE_SHELL_BUILTINS))

    # Process the command
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

    # Other
    print(f'Unknown command: {known_params.command}')
    parser.print_help()
    return Result.ok()


if __name__ == '__main__':
    main()
