import unittest

from docker_entrypoint._libs.ResultDetails.FailResult import FailResult


class TestFailResult(unittest.TestCase):
    def test_init(self):
        detail = FailResult(5, message="message")
        assert detail.title == "Operation failed with code 5."
        assert detail.message == "message"


if __name__ == '__main__':
    unittest.main()
