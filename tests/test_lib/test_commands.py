import logging
import os
import tempfile
import unittest

from on_rails import (ValidationError, assert_error_detail, assert_result,
                      assert_result_with_type)

from docker_entrypoint._libs.commands import (command_about, command_bash,
                                              command_d8, command_run,
                                              command_samples, command_shell)
from docker_entrypoint._libs.DockerEnvironments import DockerEnvironments
from docker_entrypoint._libs.ExitCodes import ExitCode
from docker_entrypoint._libs.ResultDetails.FailResult import FailResult
from tests._helpers import assert_fail_result_detail, get_logger


class TestCommands(unittest.TestCase):

    # region command_run

    def test_command_run_not_give_logger(self):
        result = command_run(None, None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="logger is required and must be a logging.Logger object",
                            expected_code=400)

    def test_command_run_give_invalid_program(self):
        result = command_run(logging.getLogger(), None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_code=400,
                            expected_title='One or more validation errors occurred',
                            expected_message="The program must be a string")

        result = command_run(logging.getLogger(), 5)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_code=400,
                            expected_title='One or more validation errors occurred',
                            expected_message="The program must be a string")

        result = command_run(logging.getLogger(), '')
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_code=400,
                            expected_title='One or more validation errors occurred',
                            expected_message="The program can not be empty or whitespace")

        result = command_run(logging.getLogger(), '    ')
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_code=400,
                            expected_title='One or more validation errors occurred',
                            expected_message="The program can not be empty or whitespace")

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
            assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                                expected_message="files_and_dirs must be a list of strings or None",
                                expected_code=400)

            result = command_run(logging.getLogger(), file, None, "not list")
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
            assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                                expected_message="args must be a list of strings or None",
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

    def test_command_run_give_files_and_args(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "program.js")
            with open(file, "w") as f:
                f.write("")

            logger, logging_stream = get_logger()

            result = command_run(logger, file, [file], ['arg1', 'arg2'])

            expected_log = "[DEBUG] Number of input files: 1\n" \
                           f"[INFO] file 1: {file}\n" \
                           f"[DEBUG] command: bash -c 'd8 {file} arg1 arg2 < {file}'\n" \
                           f"[DEBUG] Return Code: {result.code()}\n"
            self.assertEqual(expected_log, logging_stream.getvalue())

    # endregion

    # region command_d8

    def test_command_d8_not_give_logger(self):
        result = command_d8(None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="logger is required and must be a logging.Logger object",
                            expected_code=400)

    def test_command_d8_give_invalid_list(self):
        result = command_d8(logging.getLogger(), "not list")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="args must be a list of strings or None",
                            expected_code=400)

    def test_command_d8_with_args(self):
        logger, logging_stream = get_logger()
        result = command_d8(logger, ['arg1', 'arg2'])

        expected_log = "[DEBUG] Command: d8 arg1 arg2\n" \
                       f"[INFO] Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell\n" \
                       f"[DEBUG] Return code: {result.code()}\n"
        self.assertEqual(expected_log, logging_stream.getvalue())

    # endregion

    # region command_shell

    def test_command_shell_not_give_logger(self):
        result = command_shell(None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="logger is required and must be a logging.Logger object",
                            expected_code=400)

    def test_command_shell_give_invalid_list(self):
        result = command_shell(logging.getLogger(), "not list")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="args must be a list of strings or None",
                            expected_code=400)

    def test_command_shell_with_args(self):
        logger, logging_stream = get_logger()
        result = command_shell(logger, ['arg1', 'arg2'])

        expected_log = "[DEBUG] Command: bash -c 'sleep 0.5; rlwrap -m -pgreen d8 --harmony --allow-natives-syntax arg1 arg2'\n" \
                       "[INFO] Default options: ['--harmony', '--allow-natives-syntax']\n" \
                       "[INFO] Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell\n" \
                       f"[DEBUG] Return code: {result.code()}\n"
        self.assertEqual(expected_log, logging_stream.getvalue())

    # endregion

    # region command_bash

    def test_command_bash_not_give_logger(self):
        result = command_bash(None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="logger is required and must be a logging.Logger object",
                            expected_code=400)

    def test_command_bash_give_invalid_list(self):
        result = command_bash(logging.getLogger(), "not list")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="args must be a list of strings or None",
                            expected_code=400)

    def test_command_bash_with_args(self):
        logger, logging_stream = get_logger()
        result = command_bash(logger, ['arg1', 'arg2'])

        expected_log = "[DEBUG] Command: bash arg1 arg2\n" \
                       "[INFO] Running bash command. Use --help to see other commands.\n" \
                       f"[DEBUG] Return code: {result.code()}\n"
        self.assertEqual(expected_log, logging_stream.getvalue())

    # endregion

    # region command_samples

    def test_command_samples_not_give_logger(self):
        result = command_samples(None, DockerEnvironments.get_environments().value)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="logger is required and must be a logging.Logger object",
                            expected_code=400)

    def test_command_samples_not_give_environments(self):
        result = command_samples(logging.getLogger(), None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="environments is required and must be an instance of `DockerEnvironments`",
                            expected_code=400)

    def test_command_samples_ok(self):
        logger, logging_stream = get_logger()
        result = command_samples(logger, DockerEnvironments.get_environments().value)

        assert_result(self, result, expected_success=True)

        expected_log = "[INFO] Use -h or --help for more information about commands.\n" \
                       "Samples:\n" \
                       "\tdocker run --rm -it No Data! run /samples/say-hello.js -f /samples/sample-inputs/0.txt -d " \
                       "/samples/sample-inputs :\tExecute sample javascript with sample inputs\n" \
                       "\tdocker run --rm -it -v $PWD:/solution No Data! run /solution/program.js -d " \
                       "/solution/sample-inputs :\tExecute your local javascript program with your local inputs\n" \
                       "\tdocker run --rm -it No Data! shell :\tstarts enhanced d8 shell with the given arguments\n" \
                       "\tdocker run --rm -it No Data! d8 :\tstarts default d8 shell with the given arguments\n" \
                       "\tdocker run --rm -it No Data! bash :\tstarts a bash shell with the given arguments\n" \
                       "\tdocker run --rm -it No Data! :\tstarts a bash shell with the given arguments\n" \
                       "\tdocker run --rm -it No Data! --version :\tdisplays the program version\n\n"
        self.assertEqual(expected_log, logging_stream.getvalue())

    # endregion

    # region command_about

    def test_command_about_not_give_logger(self):
        result = command_about(None, DockerEnvironments.get_environments().value)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="logger is required and must be a logging.Logger object",
                            expected_code=400)

    def test_command_about_not_give_environments(self):
        result = command_about(logging.getLogger(), None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="environments is required and must be an instance of `DockerEnvironments`",
                            expected_code=400)

    def test_command_about_ok(self):
        logger, logging_stream = get_logger()
        result = command_about(logger, DockerEnvironments.get_environments().value)

        assert_result(self, result, expected_success=True)

        expected_log = "[INFO] About:\n" \
                       "\tmaintainer: No Data!\n" \
                       "\tdocker_version: latest\n" \
                       "\tbuild_date: No Data!\n" \
                       "\tvcs_url: No Data!\n" \
                       "\tbug_report: No Data!\n" \
                       "\tdocker_name: No Data!\n\n"
        self.assertEqual(expected_log, logging_stream.getvalue())

    # endregion


if __name__ == '__main__':
    unittest.main()
