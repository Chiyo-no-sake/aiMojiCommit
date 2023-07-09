from aimojicommit.aimojicommit import aimojicommit
from aimojicommit.ConfigManager import ConfigManager
from aimojicommit.AIManager import AIManager
from aimojicommit.ChoicesManager import ChoicesManager
from aimojicommit.GitManager import GitManager
import pytest
from unittest.mock import patch, Mock

@pytest.mark.parametrize("is_git_installed, is_inside_repository", [(True, True), (False, False)])
@patch.object(ChoicesManager, "choose_commit_type")
@patch.object(AIManager, "get_model_info")
@patch.object(AIManager, "can_generate_commit_message")
@patch.object(AIManager, "generate_commit_message")
@patch.object(GitManager, "is_git_installed")
@patch.object(GitManager, "is_inside_repository")
@patch.object(GitManager, "get_diff_changes")
@patch.object(GitManager, "get_diff_stats")
@patch.object(ConfigManager, "get_openai_api_key")
@patch.object(ConfigManager, "get_openai_chat_model")
def test_aimojicommit(mock_get_openai_chat_model, mock_get_openai_api_key, mock_get_diff_stats, mock_get_diff_changes, mock_is_inside_repository, mock_is_git_installed, mock_generate_commit_message, mock_can_generate_commit_message, mock_get_model_info, mock_choose_commit_type, is_git_installed, is_inside_repository, monkeypatch, capsys):
    mock_is_git_installed.return_value = is_git_installed
    mock_is_inside_repository.return_value = is_inside_repository
    mock_get_diff_changes.return_value = "diffs"
    mock_get_diff_stats.return_value = "stats"
    mock_choose_commit_type.return_value = {"value": "commit_type"}
    mock_get_model_info.return_value = Mock(spec=AIManager)
    mock_can_generate_commit_message.return_value = True
    mock_generate_commit_message.return_value = "Commit message"
    mock_get_openai_api_key.return_value = "key"
    mock_get_openai_chat_model.return_value = "model"
  
    import builtins
    inputs = ["C"]
    builtins.input = Mock(side_effect=inputs)
    
    def mock_click_prompt(*args, **kwargs):
        return inputs.pop(0)
        
    monkeypatch.setattr("click.prompt", mock_click_prompt)
  
    with pytest.raises(SystemExit):
        aimojicommit()
    
    captured = capsys.readouterr()
    assert "🤖 Aimoji Commit" in captured.out
    
    if not is_git_installed:
        assert "Error: Git is not installed. Exiting." in captured.out
    elif not is_inside_repository:
        assert "Error: Not inside a git repository. Exiting." in captured.out