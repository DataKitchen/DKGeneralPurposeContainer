from unittest import TestCase
from unittest.mock import patch
from AnalyticContainerLibrary.ACBase import ACBase
from AnalyticContainerLibrary.ACSettings import (
    INSIDE_CONTAINER_FILE_MOUNT,
    INSIDE_CONTAINER_FILE_DIRECTORY,
    CONTAINER_OUTPUT_PROGRESS_FILE,
    CONTAINER_OUTPUT_LOG_FILE,
    CONTAINER_INPUT_CONFIG_FILE_NAME
)
import os
import shutil


class TestACBase(TestCase):

    _docker_share_path = os.path.join(os.getcwd(), 'docker-share')

    @classmethod
    def setUpClass(cls):
        """
        Clean leftovers from previous failed runs
        """
        try:
            shutil.rmtree(cls._docker_share_path)
        except Exception:
            pass

    def setUp(self):
        try:
            os.makedirs(self._docker_share_path)
        except Exception:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(self._docker_share_path)
        except Exception:
            pass

    @patch.dict('os.environ', {
        INSIDE_CONTAINER_FILE_MOUNT: os.getcwd(),
        INSIDE_CONTAINER_FILE_DIRECTORY: "docker-share",
        CONTAINER_OUTPUT_PROGRESS_FILE: "progress.json",
        CONTAINER_OUTPUT_LOG_FILE: "ac_logger.log ",
        CONTAINER_INPUT_CONFIG_FILE_NAME: "config.json"
    })
    def test_valid_config(self):

        ac_base = ACBase()

        self.assertFalse(ac_base.valid_config())

        with open(os.path.join(self._docker_share_path, 'config.json'), 'w') as f:
            f.write('{}')

        ac_base = ACBase()

        self.assertTrue(ac_base.valid_config())

    @patch.dict('os.environ', {
        INSIDE_CONTAINER_FILE_MOUNT: os.getcwd(),
        INSIDE_CONTAINER_FILE_DIRECTORY: "docker-share",
        CONTAINER_OUTPUT_PROGRESS_FILE: "progress.json",
        CONTAINER_OUTPUT_LOG_FILE: "ac_logger.log ",
        CONTAINER_INPUT_CONFIG_FILE_NAME: "config.json"
    })
    def test_write_progress(self):

        with open(os.path.join(self._docker_share_path, 'config.json'), 'w') as f:
            f.write('{}')

        ac_base = ACBase()
        ac_base.set_progress('var1', 'value1')
        ac_base.write_progress()

        self.assertTrue(os.path.isfile(os.path.join(self._docker_share_path, 'progress.json')))
