import logging
import os
from typing import List, Optional

from on_rails import Result, def_result
from pylity import Path

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

    files: List[str] = Path.collect_files(files_and_dirs).on_fail_break_function().value
    for file in files:
        os.system(f"bash -c 'd8 {program} {' '.join(args)} < {file}'")
    return Result.ok()
