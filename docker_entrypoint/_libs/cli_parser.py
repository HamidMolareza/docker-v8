import argparse

from on_rails import Result, def_result

from docker_entrypoint._libs.utility import D8_Recommended_OPTIONS


@def_result()
def create_cli_parser() -> Result[argparse.ArgumentParser]:
    """
    This function creates a command-line interface parser with sub-parsers for different commands and their arguments.

    :return: Returning a `Result` object that contains an `argparse.ArgumentParser` object.
    """

    # Define the main parser
    parser = argparse.ArgumentParser(description='The d8 docker entrypoint')
    parser.add_argument('--version', action='store_true', help='show program version')
    parser.add_argument('--debug', action='store_true', help='show logs at debug level')

    # Create a sub-parser for the 'run' command
    run_parser = argparse.ArgumentParser(add_help=False)
    run_parser.add_argument('program', type=str, help='The javascript program to execute')
    run_parser.add_argument('-f', '--file', type=str, action='append', help='Input file(s)')
    run_parser.add_argument('-d', '--directory', type=str, action='append', help='Input directory(s)')

    # Create a sub-parser for the 'shell' command
    shell_parser = argparse.ArgumentParser(add_help=False)
    for option, help_msg in D8_Recommended_OPTIONS.items():
        shell_parser.add_argument(option, action='store_true', help=help_msg)

    # Create a sub-parser for the 'bash' command
    bash_parser = argparse.ArgumentParser(add_help=False)

    # Create a sub-parser for the 'd8' command
    d8_parser = argparse.ArgumentParser(add_help=False)
    for option, help_msg in D8_Recommended_OPTIONS.items():
        d8_parser.add_argument(option, action='store_true', help=help_msg)

    # Create a sub-parser for the 'samples' command
    samples_parser = argparse.ArgumentParser(add_help=False)

    # Create a sub-parser for the 'about' command
    about_parser = argparse.ArgumentParser(add_help=False)

    # Add sub-parsers for the commands
    subparsers = parser.add_subparsers(dest='command')

    # Add sub-parsers for the sub-commands
    subparsers.add_parser('run', parents=[run_parser],
                          help='Execute a javascript program with arguments')
    subparsers.add_parser('shell', parents=[shell_parser],
                          help='Execute an enhanced d8 shell with arguments')
    subparsers.add_parser('d8', parents=[d8_parser], help='Default d8 shell')
    subparsers.add_parser('bash', parents=[bash_parser], help='Execute a bash shell with arguments')
    subparsers.add_parser('samples', parents=[samples_parser], help='Show samples')
    subparsers.add_parser('about', parents=[about_parser], help='Show About message')

    return Result.ok(parser)
