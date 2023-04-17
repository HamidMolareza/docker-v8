import argparse
import unittest

from docker_entrypoint._libs.cli_parser import create_cli_parser


class TestCliParser(unittest.TestCase):
    def test_create_cli_parser_ok(self):
        result = create_cli_parser()

        assert result.success
        assert isinstance(result.value, argparse.ArgumentParser)
        self.assertIsNone(result.detail)


if __name__ == '__main__':
    unittest.main()
