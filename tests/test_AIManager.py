import unittest
from unittest.mock import patch, Mock
from aimojicommit.AIManager import AIManager, Model
from aimojicommit.ConfigManager import ConfigManager


class TestAIManager(unittest.TestCase):
    @patch("openai.Model.list")
    @patch("aimojicommit.ConfigManager.ConfigManager.get_openai_api_key")
    def test_list_available_models(self, mock_get_openai_api_key, mock_model_list):
        model = Model("test_model-16k", 16384)
        mock_model_list.return_value = Mock(data=[model])

        mock_get_openai_api_key.return_value = "dummy_key"  # Mocks getting the key

        config_manager = ConfigManager()
        ai_manager = AIManager(config_manager)

        models = ai_manager.list_available_models()

        # validate the function call
        mock_model_list.assert_called_once()
        mock_get_openai_api_key.assert_called_once()

        # check returned models
        assert len(models) == 1
        assert models[0].id == model.id
        assert models[0].max_tokens == model.max_tokens

    def test_can_generate_commit_message(self):
        config_manager = ConfigManager()
        model = Model(id="text-generator-16k", max_tokens=16384)
        stats = "test stats"
        diffs = "test diffs"
        commit_prefix = "feat"
        ai_manager = AIManager(config_manager)

        with patch.object(ai_manager, "get_prompt", return_value="short string"), patch(
            "tiktoken.encoding_for_model", return_value=Mock(encode=lambda x: x)
        ):
            can_generate = ai_manager.can_generate_commit_message(
                model, stats, diffs, commit_prefix
            )
            assert can_generate  # Because our mock input string is quite short

    @patch("openai.ChatCompletion.create")
    @patch("click.echo")
    @patch("aimojicommit.ConfigManager.ConfigManager.get_openai_api_key")
    def test_generate_commit_message(
        self, mock_get_openai_api_key, mock_echo, mock_chat_create
    ):
        model = Model("text-generator-16k", 16384)
        stats = "test stats"
        diffs = "test diffs"
        commit_prefix = "feat"

        config_manager = ConfigManager()
        ai_manager = AIManager(config_manager)

        mock_get_openai_api_key.return_value = "dummy_key"  # Mocks getting the key

        mock_response = Mock(
            choices=[Mock(message=Mock(content="##Message: my_commit_message"))]
        )
        mock_chat_create.return_value = mock_response

        commit_message = ai_manager.generate_commit_message(
            model, stats, diffs, commit_prefix
        )
        assert commit_message == "my_commit_message"

        mock_chat_create.reset_mock()

        mock_chat_create.side_effect = Exception("OpenAI error")
        with self.assertRaises(Exception) as error:
            ai_manager.generate_commit_message(model, stats, diffs, commit_prefix)
        assert str(error.exception) == "OpenAI error"


if __name__ == "__main__":
    unittest.main()
