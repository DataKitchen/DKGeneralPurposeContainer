import unittest
import json
import os

PROGRESS_FILE = "docker-share/ac_progress.json"
LOGGER_FILE = "docker-share/ac_logger.log"


class TestContainer(unittest.TestCase):
    def test_progress_json(self):

        self.assertTrue(os.path.isfile(LOGGER_FILE))

        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
        except ValueError as e:
            self.fail(f"not json:{e}")

        self.assertIn("start-time", data)
        self.assertIn("container-return-status", data)
        self.assertIn("end-time", data)
        self.assertIn("test_var", data)
        self.assertEqual("received message: hello world", data.get("test_var"))
        self.assertEqual("completed_success", data.get("container-return-status"))

    def test_log_present(self):

        self.assertTrue(os.path.isfile(LOGGER_FILE))

        stat = os.stat(LOGGER_FILE)

        self.assertNotEqual(0, stat.st_size)
