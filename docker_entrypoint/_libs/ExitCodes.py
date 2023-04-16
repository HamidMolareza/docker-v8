class ExitCode:
    # Indicates that the program completed successfully without any errors.
    SUCCESS = 0

    # Indicates that there was an error or exception that occurred during the program execution that was not
    # covered by any other specific exit code.
    GENERAL_ERROR = 1

    # Indicates that the user invoked the program with incorrect arguments or used a shell command incorrectly.
    MISUSE_SHELL_BUILTINS = 2

    # Indicates that the user has provided incorrect or incomplete command-line arguments.
    COMMAND_LINE_SYNTAX_ERROR = 3

    # Indicates that the program was unable to perform an operation due to insufficient permissions or privileges.
    PERMISSION_DENIED = 4

    # Indicates that the program was unable to perform an I/O operation due to issues such as missing files,
    # disks full, or other similar errors.
    IO_ERROR = 5

    # Indicates that the program was aborted or terminated due to an unexpected error or interruption, such
    # as a system crash or a signal.
    PROGRAM_ABORTED = 6

    # Indicates that the program was compiled or executed on an incompatible machine architecture.
    INCORRECT_MACHINE_ARCHITECTURE = 7
