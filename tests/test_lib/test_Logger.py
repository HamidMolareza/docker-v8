import logging
import unittest

from docker_entrypoint._libs.Logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()

    def test_get(self):
        logger_obj = self.logger.get("test_logger_get") \
            .on_fail(lambda result: self.assertEqual(True, result.success)) \
            .value

        self.assertIsInstance(logger_obj, logging.Logger)

    def test_get_twice(self):
        logger_obj_1 = self.logger.get("test_logger_get_twice") \
            .on_fail(lambda result: self.assertEqual(True, result.success)) \
            .value

        logger_obj_2 = self.logger.get("test_logger_get_twice") \
            .on_fail(lambda result: self.assertEqual(True, result.success)) \
            .value

        self.assertIs(logger_obj_1, logger_obj_2)

    def test_set_level(self):
        logger_obj = self.logger.get("test_logger_set_level") \
            .on_fail(lambda result: self.assertEqual(True, result.success)) \
            .value

        self.logger.set_level(True, "test_logger_set_level") \
            .on_fail(lambda result: self.assertEqual(True, result.success))
        self.assertEqual(logger_obj.level, logging.DEBUG)

        self.logger.set_level(False, "test_logger_set_level") \
            .on_fail(lambda result: self.assertEqual(True, result.success))
        self.assertEqual(logger_obj.level, logging.INFO)

        # Test without name parameter
        self.logger.set_level(True) \
            .on_fail(lambda result: self.assertEqual(True, result.success))
        self.assertEqual(logger_obj.level, logging.DEBUG)

        self.logger.set_level(False) \
            .on_fail(lambda result: self.assertEqual(True, result.success))
        self.assertEqual(logger_obj.level, logging.INFO)


if __name__ == '__main__':
    unittest.main()
