import unittest

from on_rails import (Result, ValidationError, assert_error_detail,
                      assert_result, assert_result_with_type)

from docker_entrypoint._libs.utility import log_result
from tests._helpers import get_logger


class TestUtility(unittest.TestCase):
    # region log_result

    def test_log_result_not_give_logger(self):
        result = log_result(None, None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The logger is required.", expected_code=400)

    def test_log_result_give_success(self):
        logger, logging_stream = get_logger()

        result = Result.ok()
        func_result = log_result(logger, result)
        self.assertEqual(result, func_result)
        self.assertEqual("", logging_stream.getvalue())

    def test_log_result_give_success_with_value(self):
        logger, logging_stream = get_logger()

        func_result = log_result(logger, Result.ok("value"))
        assert_result(self, target_result=func_result, expected_success=True)
        self.assertEqual("[INFO] value\n", logging_stream.getvalue())

    # endregion


if __name__ == '__main__':
    unittest.main()
