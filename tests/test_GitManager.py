import unittest
import subprocess
from unittest.mock import patch
from aimojicommit.GitManager import GitManager

class TestGitManager(unittest.TestCase):

    @patch('subprocess.check_output')
    def test_is_git_installed(self, mock_subprocess):
        mock_subprocess.return_value = b'git'
        result = GitManager.is_git_installed()
        self.assertTrue(result)

    @patch('subprocess.check_output')
    def test_is_not_git_installed(self, mock_subprocess):
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'cmd')
        result = GitManager.is_git_installed()
        self.assertFalse(result)

    @patch('subprocess.check_output')
    def test_is_inside_repository(self, mock_subprocess):
        mock_subprocess.return_value = b'true'
        result = GitManager.is_inside_repository()
        self.assertTrue(result)

    @patch('subprocess.check_output')
    def test_is_not_inside_repository(self, mock_subprocess):
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'cmd')
        result = GitManager.is_inside_repository()
        self.assertFalse(result)

    @patch('subprocess.check_output')
    def test_get_diff_stats(self, mock_subprocess):
        mock_subprocess.return_value = b'test stats'
        result = GitManager.get_diff_stats()
        self.assertEqual(result, 'test stats')

    @patch('subprocess.check_output')
    def test_get_diff_changes(self, mock_subprocess):
        mock_subprocess.return_value = b'test changes'
        result = GitManager.get_diff_changes()
        self.assertEqual(result, 'test changes')

if __name__ == '__main__':
    unittest.main()