import pytest
from aimojicommit.ChoicesManager import ChoicesManager
from unittest.mock import patch

# Mock `pick.pick` method which is an external dependency
@patch('pick.pick', return_value=('feat: New Feature', 0))
def test_choose_commit_type(mock_pick):
    from aimojicommit.ConfigManager import ConfigManager
    config_manager = ConfigManager()

    # Mock the get_value function to return test values instead of the real ones
    with patch.object(config_manager, 'get_value', return_value=[{'prefix': 'feat', 'detail': 'New Feature'}]):
        choices_manager = ChoicesManager(config_manager)
        result = choices_manager.choose_commit_type()
        assert result['value'] == 'feat'

    # Check if pick.pick is called once with the right arguments
    mock_pick.assert_called_once_with(
        ["feat: New Feature"], 
        "Choose a commit type"
    )

@patch('pick.pick', return_value=('test_option', 0))
def test_choose_option(mock_pick):
    from aimojicommit.ConfigManager import ConfigManager
    config_manager = ConfigManager()
    choices_manager = ChoicesManager(config_manager)

    options = ['test_option']
    title = 'Choose an option'
    result = choices_manager.choose_option(title, options)
    assert result == 'test_option'

    # Check if pick.pick is called once with the right arguments
    mock_pick.assert_called_once_with(
        options, 
        title
    )