import unittest

from docker_entrypoint.entrypoint import main


class TestEntrypoint(unittest.TestCase):
    def test_main_invalid_inputs(self):
        code = main([1, 2, 3])
        assert code == 400

        code = main([], 'not logger type')
        assert code == 400

    def test_main_empty_args(self):
        code = main([])
        assert code == 2

    def test_main_version(self):
        code = main(['--version'])
        assert code == 0


if __name__ == '__main__':
    unittest.main()
