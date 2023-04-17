import logging
import os
import tempfile
import unittest

from on_rails import (ValidationError, assert_error_detail,
                      assert_result_with_type)

from docker_entrypoint._libs.commands import command_run
from docker_entrypoint._libs.ExitCodes import ExitCode
from docker_entrypoint._libs.ResultDetails.FailResult import FailResult
from tests._helpers import assert_fail_result_detail, get_logger


class TestCommands(unittest.TestCase):

    # region command_run

    def test_command_run_not_give_logger(self):
        result = command_run(None, None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The logger is required.", expected_code=400)

    def test_command_run_give_invalid_program(self):
        result = command_run(logging.getLogger(), "invalid")

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=FailResult)
        assert_fail_result_detail(self, result.detail, expected_code=ExitCode.IO_ERROR,
                                  expected_message="File 'invalid' does not exists.")

    def test_command_run_give_invalid_list(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "program.js")
            with open(file, "w") as f:
                f.write("")

            result = command_run(logging.getLogger(), file, "not list")
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
            assert_error_detail(self, result.detail, expected_title="The 'files_and_dirs' parameter is not valid.",
                                expected_message="Expected get list of strings but got str.",
                                expected_code=400)

            result = command_run(logging.getLogger(), file, None, "not list")
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
            assert_error_detail(self, result.detail, expected_title="The 'args' parameter is not valid.",
                                expected_message="Expected get list of strings but got str.",
                                expected_code=400)

    def test_command_run_give_invalid_path(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "program.js")
            with open(file, "w") as f:
                f.write("")

            result = command_run(logging.getLogger(), file, ["invalid path"])
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=FailResult)
            assert_fail_result_detail(self, result.detail, expected_code=ExitCode.IO_ERROR,
                                      expected_message="Title: File or directory is not valid.\n"
                                                       "Message: The (invalid path) is not valid.\n"
                                                       "Code: 400\n")

    def test_command_run_no_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "program.js")
            with open(file, "w") as f:
                f.write("")

            logger, logging_stream = get_logger()

            result = command_run(logger, file)

            expected_log = f"[WARNING] No file provided.\n" \
                           f"[DEBUG] command: bash -c 'd8 {file}'\n" \
                           f"[DEBUG] Return Code: {result.code()}\n"
            self.assertEqual(expected_log, logging_stream.getvalue())

    def test_command_run_give_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file1 = os.path.join(tmp_dir_name, "program.js")
            with open(file1, "w") as f:
                f.write("")
            file2 = os.path.join(tmp_dir_name, "program2.js")
            with open(file2, "w") as f:
                f.write("")

            logger, logging_stream = get_logger()

            result = command_run(logger, file1, [file1, file1, file2])

            expected_log = "[DEBUG] Number of input files: 2\n" \
                           f"[INFO] file 1: {file1}\n" \
                           f"[DEBUG] command: bash -c 'd8 {file1}  < {file1}'\n" \
                           f"[DEBUG] Return Code: {result.code()}\n" \
                           f"[INFO] file 2: {file2}\n" \
                           f"[DEBUG] command: bash -c 'd8 {file1}  < {file2}'\n" \
                           f"[DEBUG] Return Code: {result.code()}\n"
            self.assertEqual(expected_log, logging_stream.getvalue())

    # endregion


if __name__ == '__main__':
    unittest.main()
