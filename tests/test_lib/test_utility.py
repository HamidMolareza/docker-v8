import logging
import unittest

from on_rails import (ErrorDetail, Result, ValidationError,
                      assert_error_detail, assert_result,
                      assert_result_with_type)
from schema import SchemaError

from docker_entrypoint._libs.ResultDetails.FailResult import FailResult
from docker_entrypoint._libs.utility import (class_properties_to_str,
                                             convert_code_to_result,
                                             get_support_message, log_error,
                                             log_result, try_validation)
from tests._helpers import assert_fail_result_detail, get_logger


class TestUtility(unittest.TestCase):
    # region log_result

    def test_log_result_not_give_logger(self):
        result = log_result(None, None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The logger is required and must be type of logging.", expected_code=400)

    def test_log_result_give_none_result(self):
        result = log_result(logging.getLogger(), None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The result is required and must be type of Result.",
                            expected_code=400)

    def test_log_result_give_success(self):
        logger, logging_stream = get_logger()

        func_result = log_result(logger, Result.ok())
        assert_result(self, func_result, expected_success=True)
        self.assertEqual("", logging_stream.getvalue())

    def test_log_result_give_success_with_value(self):
        logger, logging_stream = get_logger()

        func_result = log_result(logger, Result.ok("value"))
        assert_result(self, target_result=func_result, expected_success=True)
        self.assertEqual("[INFO] value\n", logging_stream.getvalue())

    def test_log_result_expected_error(self):
        logger, logging_stream = get_logger()

        result = log_result(logger, Result.fail(FailResult(code=5, message="message")))
        assert_result(self, target_result=result, expected_success=True)
        self.assertEqual("[ERROR] Operation failed with code 5.\nmessage\n\n", logging_stream.getvalue())

    def test_log_result_unexpected_error(self):
        logger, logging_stream = get_logger()

        result = log_result(logger, Result.fail(ValidationError()))
        assert_result(self, target_result=result, expected_success=True)

        log_output = logging_stream.getvalue()
        self.assertIn("Title: One or more validation errors occurred\nCode: 400\nStack trace:",
                      log_output)
        self.assertIn("[INFO] Please report this error to help others who use this program.\n"
                      "Support:\n"
                      "\tMaintainer: No Data!\n"
                      "\tDocker Version: latest\n"
                      "\tBuild Date: No Data!\n"
                      "\tRepository: No Data!\n"
                      "\tReport Bug: No Data!",
                      log_output)

    def test_log_result_unexpected_error_without_detail(self):
        logger, logging_stream = get_logger()
        result = log_result(logger, Result.fail())

        assert_result(self, result, expected_success=True)
        assert logging_stream.getvalue() == ''

    # endregion

    # region log_error

    def test_log_error_not_give_logger(self):
        result = log_error(None, None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The logger is required and must be type of logging.", expected_code=400)

    def test_log_error_give_none_result(self):
        result = log_error(logging.getLogger(), None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The fail_result is required and must be type of Result.fail()",
                            expected_code=400)

    def test_log_error_give_success_result(self):
        result = Result.ok()
        func_result = log_error(logging.getLogger(), result)

        assert_result_with_type(self, func_result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, func_result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The fail_result is required and must be type of Result.fail()",
                            expected_code=400)

    def test_log_error(self):
        logger, logging_stream = get_logger()

        func_result = log_error(logger, Result.fail(ValidationError()))
        assert_result(self, target_result=func_result, expected_success=True)

        self.assertIn("[ERROR] An error occurred:\n"
                      "Title: One or more validation errors occurred\n"
                      "Code: 400\n"
                      "Stack trace:",
                      logging_stream.getvalue())
        self.assertIn("[INFO] Please report this error to help others who use this program.\n"
                      "Support:\n"
                      "\tMaintainer: No Data!\n"
                      "\tDocker Version: latest\n"
                      "\tBuild Date: No Data!\n"
                      "\tRepository: No Data!\n"
                      "\tReport Bug: No Data!",
                      logging_stream.getvalue())
        print(logging_stream.getvalue())

    # endregion

    # region get_support_message

    def test_get_support_message(self):
        result = get_support_message()
        assert_result(self, target_result=result, expected_success=True,
                      expected_value="Support:\n"
                                     "\tMaintainer: No Data!\n"
                                     "\tDocker Version: latest\n"
                                     "\tBuild Date: No Data!\n"
                                     "\tRepository: No Data!\n"
                                     "\tReport Bug: No Data!\n")

    # endregion

    # region class_properties_to_str

    def test_class_properties_to_str_give_none(self):
        result = class_properties_to_str(None)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The class object is required and must be an instance of a class",
                            expected_code=400)

    def test_class_properties_to_str_give_invalid_title(self):
        result = class_properties_to_str(self, ['not string'])
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The title must be None or non-empty string",
                            expected_code=400)

        result = class_properties_to_str(self, title="   ")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The title must be None or non-empty string",
                            expected_code=400)

    def test_class_properties_to_str_without_msg(self):
        class Fake:
            def __init__(self):
                self.prop1 = "prop1"
                self.prop2 = "prop2"

        result = class_properties_to_str(Fake())
        assert_result(self, result, expected_success=True, expected_value="prop1: prop1\nprop2: prop2\n")

    def test_class_properties_to_str_with_msg(self):
        class Fake:
            def __init__(self):
                self.prop1 = "prop1"
                self.prop2 = "prop2"

        result = class_properties_to_str(Fake(), title="message")
        assert_result(self, result, expected_success=True, expected_value="message:\n"
                                                                          "\tprop1: prop1\n"
                                                                          "\tprop2: prop2\n")

    # endregion

    # region convert_code_to_result

    def test_convert_code_to_result_invalid_code(self):
        result = convert_code_to_result(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The code is required and must be integer",
                            expected_code=400)

    def test_convert_code_to_result(self):
        result = convert_code_to_result(5)
        assert_fail_result_detail(self, result.detail, expected_code=5)

        result = convert_code_to_result(0)
        assert_result(self, result, expected_success=True)

    # endregion

    # region try_validation

    def test_try_validation_give_non_callable(self):
        result = try_validation('not callable')

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The validation_func is required and must be a function", expected_code=400)

    def test_try_validation_raise_validation_error(self):
        def validation_failed():
            raise SchemaError("fake")

        result = try_validation(validation_failed)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="fake", expected_code=400)

    def test_try_validation_raise_not_validation_error(self):
        exception = TypeError("fake")

        def validation_failed():
            raise exception

        result = try_validation(validation_failed)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are "
                                             "stored in the more_data field. At least one of the errors was "
                                             "an exception type, the first exception being stored in the "
                                             "exception field.",
                            expected_code=500,
                            expected_more_data=[exception], expected_exception=exception)

    def test_try_validation_not_raise_any_exception(self):
        result = try_validation(lambda: None)
        assert_result(self, result, expected_success=True)

    # endregion


if __name__ == '__main__':
    unittest.main()
