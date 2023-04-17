import logging
import unittest

from docker_entrypoint._libs.Logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()

    def test_logger_get(self):
        logger_obj = self.logger.get("test_logger_get")

        self.assertIsInstance(logger_obj, logging.Logger)
        self.assertEqual(logger_obj.name, "test_logger_get")
        self.assertEqual(len(logger_obj.handlers), 1)
        self.assertIsInstance(logger_obj.handlers[0], logging.StreamHandler)
        self.assertEqual(logger_obj.level, logging.INFO)

    def test_logger_get_twice(self):
        logger_obj_1 = self.logger.get("test_logger_get_twice")
        logger_obj_2 = self.logger.get("test_logger_get_twice")
        self.assertIs(logger_obj_1, logger_obj_2)

    def test_logger_set_level(self):
        logger_obj = self.logger.get("test_logger_set_level")
        self.assertEqual(logger_obj.level, logging.INFO)

        self.logger.set_level(True, "test_logger_set_level")
        self.assertEqual(logger_obj.level, logging.DEBUG)

        self.logger.set_level(False, "test_logger_set_level")
        self.assertEqual(logger_obj.level, logging.INFO)

        # Test without name parameter
        self.logger.set_level(True)
        self.assertEqual(logger_obj.level, logging.DEBUG)

        self.logger.set_level(False)
        self.assertEqual(logger_obj.level, logging.INFO)


if __name__ == '__main__':
    unittest.main()
