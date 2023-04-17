import io
import logging
import unittest
from typing import Optional

from docker_entrypoint._libs.ResultDetails.FailResult import FailResult


def assert_fail_result_detail(test_class: unittest.TestCase, result: FailResult,
                              expected_code: int, expected_message: Optional[str] = None):
    test_class.assertIsInstance(result, FailResult, "Result must be instance of FailResult")
    test_class.assertEqual(expected_code, result.code)
    test_class.assertEqual(expected_message, result.message)


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logging_stream = io.StringIO()
    stream_handler = logging.StreamHandler(logging_stream)
    stream_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

    logger.addHandler(stream_handler)
    return logger, logging_stream
