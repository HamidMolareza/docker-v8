import logging
import os
import tempfile
import unittest

from docker_entrypoint.entrypoint import main
from tests._helpers import get_logger


class TestEntrypoint(unittest.TestCase):
    def test_main_invalid_inputs(self):
        code = main([1, 2, 3])
        assert code == 400

        code = main('not list')
        assert code == 400

        code = main([], 'not logger type')
        assert code == 400

    def test_main_empty_args(self):
        # default logger
        code = main([])
        assert code == 2

        logger, logging_stream = get_logger()
        code = main([], logger)
        assert code == 2
        self.assertIn('[ERROR] Operation failed with code 2.\n'
                      'No command specified.\n\n', logging_stream.getvalue())

    def test_main_base_flags(self):
        logger, logging_stream = get_logger()
        logger.setLevel(logging.INFO)
        code = main(['--version'], logger)
        assert code == 0
        self.assertEqual('[INFO] Program Version: latest\n', logging_stream.getvalue())

        logger, logging_stream = get_logger()
        code = main(['--debug'], logger)
        assert code == 2
        self.assertEqual('[DEBUG] success: True\n'
                         'Value: Environments:\n'
                         '\tmaintainer: No Data!\n'
                         '\tdocker_version: latest\n'
                         '\tbuild_date: No Data!\n'
                         '\tvcs_url: No Data!\n'
                         '\tbug_report: No Data!\n'
                         '\tdocker_name: No Data!\n\n\n'
                         '[DEBUG] known params: Namespace(command=None, debug=True, version=False)\n'
                         'Args: []\n'
                         '[ERROR] Operation failed with code 2.\n'
                         'No command specified.\n\n', logging_stream.getvalue())

    def test_main_run_command(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            program_file = os.path.join(tmp_dir_name, "program.js")
            with open(program_file, "w") as f:
                f.write("")
            file1 = os.path.join(tmp_dir_name, "file1.txt")
            with open(file1, "w") as f:
                f.write("")
            dir1 = os.path.join(tmp_dir_name, 'dir')
            os.mkdir(dir1)
            file2 = os.path.join(dir1, "file2.txt")
            with open(file2, "w") as f:
                f.write("")

            try:
                main(['run'])
            except SystemExit as e:
                assert e.code == 2  # program param is required

            logger, logging_stream = get_logger()
            code = main('run invalid_program_path'.split(' '), logger)
            self.assertIn(f"[ERROR] Operation failed with code {code}.\n"
                          "File 'invalid_program_path' does not exists.\n", logging_stream.getvalue())

            logger, logging_stream = get_logger()
            code = main(f'--debug run {program_file}'.split(' '), logger)
            self.assertIn("[WARNING] No file provided.\n"
                          f"[DEBUG] command: bash -c 'd8 {program_file}'\n"
                          f"[DEBUG] Return Code: {code}\n"
                          f"[ERROR] Operation failed with code {code}.\n", logging_stream.getvalue())

            logger, logging_stream = get_logger()
            code = main(f'--debug run {program_file} -f invalid'.split(' '), logger)
            self.assertIn(
                "[DEBUG] known params: Namespace(command='run', debug=True, directory=None, "
                f"file=['invalid'], program='{program_file}', version=False)\n"
                "Args: []\n"
                f"[ERROR] Operation failed with code {code}.\n"
                "Title: File or directory is not valid.\n"
                "Message: The (invalid) is not valid.\n", logging_stream.getvalue())

            logger, logging_stream = get_logger()
            code = main(f'--debug run {program_file} -f {file1}'.split(' '), logger)
            self.assertIn(
                f"[DEBUG] known params: Namespace(command='run', debug=True, directory=None, file=['{file1}'], program='{program_file}', version=False)\n"
                "Args: []\n"
                "[DEBUG] Number of input files: 1\n"
                f"[INFO] file 1: {file1}\n"
                f"[DEBUG] command: bash -c 'd8 {program_file}  < {file1}'\n"
                f"[DEBUG] Return Code: {code}\n"
                f"[ERROR] Operation failed with code {code}.", logging_stream.getvalue())

            logger, logging_stream = get_logger()
            code = main(f'--debug run {program_file} arg1 arg2 -f {file1}'.split(' '), logger)
            self.assertIn(
                f"[DEBUG] known params: Namespace(command='run', debug=True, directory=None, file=['{file1}'], program='{program_file}', version=False)\n"
                "Args: ['arg1', 'arg2']\n"
                "[DEBUG] Number of input files: 1\n"
                f"[INFO] file 1: {file1}\n"
                f"[DEBUG] command: bash -c 'd8 {program_file} arg1 arg2 < {file1}'\n"
                f"[DEBUG] Return Code: {code}\n"
                f"[ERROR] Operation failed with code {code}.", logging_stream.getvalue())

            logger, logging_stream = get_logger()
            code = main(f'--debug run {program_file} -f {file1} -d invalid'.split(' '), logger)
            self.assertIn(
                f"[DEBUG] known params: Namespace(command='run', debug=True, directory=['invalid'], file=['{file1}'], program='{program_file}', version=False)\n"
                "Args: []\n"
                f"[ERROR] Operation failed with code {code}.\n"
                "Title: File or directory is not valid.\n"
                "Message: The (invalid) is not valid.\n", logging_stream.getvalue())

            logger, logging_stream = get_logger()
            code = main(f'--debug run {program_file} -f {file1} -d {dir1}'.split(' '), logger)
            self.assertIn(
                f"[DEBUG] known params: Namespace(command='run', debug=True, directory=['{dir1}'], file=['{file1}'], program='{program_file}', version=False)\n"
                "Args: []\n"
                "[DEBUG] Number of input files: 2\n"
                f"[INFO] file 1: {file2}\n"
                f"[DEBUG] command: bash -c 'd8 {program_file}  < {file2}'\n"
                f"[DEBUG] Return Code: {code}\n"
                f"[INFO] file 2: {file1}\n"
                f"[DEBUG] command: bash -c 'd8 {program_file}  < {file1}'\n"
                f"[DEBUG] Return Code: {code}\n"
                f"[ERROR] Operation failed with code {code}.", logging_stream.getvalue())

    def test_main_shell_command(self):
        logger, logging_stream = get_logger()
        logger.setLevel(logging.INFO)
        code = main('shell'.split(' '), logger)
        self.assertIn("[INFO] Default options: ['--harmony', '--allow-natives-syntax']\n"
                      "[INFO] Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell\n"
                      f"[ERROR] Operation failed with code {code}.\n", logging_stream.getvalue())

        logger, logging_stream = get_logger()
        code = main('--debug shell'.split(' '), logger)
        self.assertIn(
            "[DEBUG] known params: Namespace(allow_natives_syntax=False, command='shell', debug=True, "
            "harmony=False, log_gc=False, log_timer_events=False, print_bytecode=False, print_opt_code=False, "
            "prof=False, trace=False, trace_deopt=False, trace_ic=False, trace_opt=False, version=False)\n"
            "Args: []\n"
            "[DEBUG] Command: bash -c 'sleep 0.5; rlwrap -m -pgreen d8 --harmony --allow-natives-syntax'\n"
            "[INFO] Default options: ['--harmony', '--allow-natives-syntax']\n"
            "[INFO] Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell\n"
            f"[DEBUG] Return code: {code}\n"
            f"[ERROR] Operation failed with code {code}.\n", logging_stream.getvalue())

        logger, logging_stream = get_logger()
        code = main('--debug shell -a arg1 arg2'.split(' '), logger)
        self.assertIn("Args: ['-a', 'arg1', 'arg2']\n"
                      "[DEBUG] Command: bash -c 'sleep 0.5; rlwrap -m -pgreen d8 --harmony --allow-natives-syntax -a arg1 arg2'\n"
                      "[INFO] Default options: ['--harmony', '--allow-natives-syntax']\n"
                      "[INFO] Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell\n"
                      f"[DEBUG] Return code: {code}\n"
                      f"[ERROR] Operation failed with code {code}.\n", logging_stream.getvalue())

    def test_main_bash_command(self):
        logger, logging_stream = get_logger()
        code = main('--debug bash -a arg1 arg2'.split(' '), logger)
        self.assertIn("[DEBUG] known params: Namespace(command='bash', debug=True, version=False)\n"
                      "Args: ['-a', 'arg1', 'arg2']\n"
                      "[DEBUG] Command: bash -a arg1 arg2\n"
                      "[INFO] Running bash command. Use --help to see other commands.\n"
                      f"[DEBUG] Return code: {code}\n"
                      f"[ERROR] Operation failed with code {code}.\n", logging_stream.getvalue())

    def test_main_d8_command(self):
        logger, logging_stream = get_logger()
        code = main('--debug d8 -a arg1 arg2'.split(' '), logger)
        self.assertIn("Args: ['-a', 'arg1', 'arg2']\n"
                      "[DEBUG] Command: d8 -a arg1 arg2\n"
                      "[INFO] Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell\n"
                      f"[DEBUG] Return code: {code}\n"
                      f"[ERROR] Operation failed with code {code}.", logging_stream.getvalue())

    def test_main_samples_command(self):
        code = main('samples'.split(' '))
        assert code == 0

    def test_main_about_command(self):
        code = main('--debug about'.split(' '))
        assert code == 0

    def test_main_invalid_command(self):
        try:
            main('--debug invalid-command'.split(' '))
        except SystemExit as e:
            assert e.code == 2  # program param is required


if __name__ == '__main__':
    unittest.main()
