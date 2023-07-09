import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from aimojicommit.ConfigManager import ConfigManager

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.config_manager = ConfigManager()

    @patch("builtins.open", new_callable=mock_open, read_data="openai_api_key: test_key")
    @patch("os.path.exists", return_value=True)
    def test_get_openai_api_key(self, os_exists_mock, open_mock):
        self.config_manager.config = None
        self.config_manager.load_config()
        openai_key = self.config_manager.get_openai_api_key()
        self.assertEqual(openai_key, "test_key")

    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.load")
    def test_load_config(
        self, yaml_load_mock, open_mock, requests_get_mock, os_makedirs_mock, os_exists_mock
    ):
        mock_resp = MagicMock()
        mock_resp.iter_content.return_value = [b"{"]

        yaml_load_mock.return_value = {"test": "test_content"}

        requests_get_mock.return_value = mock_resp

        self.config_manager.load_config()
        self.assertIsNotNone(self.config_manager.config)
        os_exists_mock.assert_called()
        os_makedirs_mock.assert_called_with(self.config_manager.root_folder)
        yaml_load_mock.assert_called_once()
        open_mock.assert_called_with(self.config_manager.file_path, 'r')

    @patch("builtins.open", new_callable=mock_open)
    def test_save_config(self, open_mock):
        self.config_manager.root_folder = '/test/root/folder'
        self.config_manager.file_path = self.config_manager.root_folder + 'config.yaml'
        self.config_manager.config = {"test":"config"}
        self.config_manager.save_config()
        open_mock.assert_called_once_with("/test/root/folderconfig.yaml", "w")

    @patch("builtins.open", new_callable=mock_open, read_data="openai_api_key: test_key")
    @patch("os.path.exists", return_value=True)
    def test_set_openai_api_key(self, os_exists_mock, open_mock):
        test_key = "new_test_key"
        self.config_manager.config = None
        self.config_manager.load_config()
        self.config_manager.set_openai_api_key(test_key)

        self.assertEqual(self.config_manager.config["openai_api_key"], test_key)

if __name__ == '__main__':
    unittest.main()