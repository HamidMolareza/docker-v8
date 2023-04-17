import unittest

from docker_entrypoint._libs.ResultDetails.FailResult import FailResult


class TestFailResult(unittest.TestCase):
    def test_init(self):
        detail = FailResult(5, message="message")
        assert detail.title == "Operation failed with code 5."
        assert detail.message == "message"

    def test_init_message_is_optional(self):
        detail = FailResult(5)
        assert detail.title == "Operation failed with code 5."
        self.assertIsNone(detail.message)

    def test_str_without(self):
        string = str(FailResult(5))
        self.assertEqual("Operation failed with code 5.", string)

        string = str(FailResult(5, message="message"))
        self.assertEqual("Operation failed with code 5.\nmessage\n", string)


if __name__ == '__main__':
    unittest.main()
