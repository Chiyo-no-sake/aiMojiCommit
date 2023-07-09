import click
from aimojicommit.ChoicesManager import ChoicesManager
from aimojicommit.ConfigManager import ConfigManager
from aimojicommit.GitManager import GitManager
from aimojicommit.AIManager import AIManager, Model
from aimojicommit import constants

def model_id(model: Model):
    return model.id

def setup_config(config_manager: ConfigManager, ai_manager: AIManager):
    openai_key = config_manager.get_openai_api_key()
    chat_model = config_manager.get_openai_chat_model()
    if openai_key is None:
        set_key(None, config_manager)
    if chat_model is None:
        set_model(None, config_manager, ai_manager)


def set_key(key: str or None, config_manager: ConfigManager = None):
    if not key:
        key = click.prompt("Please enter your OpenAI API key", type=str)

    config_manager.set_openai_api_key(key)


def set_model(model: str or None, config_manager: ConfigManager = None, ai_manager: AIManager = None):
    models = ai_manager.list_available_models()

    if model is None:
        model = ChoicesManager(config_manager).choose_option(
            "Please choose an OpenAI chat model (*-16k suggested)", list(map(model_id, models))
        )

    if model not in list(map(model_id, models)):
        click.echo("Error: Model not found.")
        raise click.Abort()

    config_manager.set_openai_chat_model(model)


@click.group(invoke_without_command=True)
@click.option("-t", "--commit-type", help="Specify the commit type", default=None)
def aimojicommit(commit_type):
    click.echo("🤖 Aimoji Commit")

    if not GitManager.is_git_installed():
        click.echo("Error: Git is not installed. Exiting.")
        raise click.Abort()

    if not GitManager.is_inside_repository():
        click.echo("Error: Not inside a git repository. Exiting.")
        raise click.Abort()

    config_manager = ConfigManager()
    config_manager.load_config()
    click.echo(f"Loaded config from {config_manager.file_path}")

    choices_manager = ChoicesManager(config_manager)
    ai_manager = AIManager(config_manager)
    setup_config(config_manager, ai_manager)

    diffs = GitManager.get_diff_changes()
    stats = GitManager.get_diff_stats()

    if len(diffs) == 0 or len(stats) == 0:
        click.echo("Error: No changes added to commit. Exiting.")
        raise click.Abort()

    # Optionally ask for the commit type
    if not commit_type:
        commit_type = choices_manager.choose_commit_type()

    # Check if there is a preconfigured commit message
    merge_msg = GitManager.get_merge_commit_message()
    if merge_msg is not None and len(merge_msg) > 0:
        click.echo(f"Found preconfigured merge commit message: {merge_msg}")
        reply = click.prompt(
            "Do you want to use this message? (Y/n)",
            default="Y",
            show_choices=True,
            type=click.Choice(["Y", "n"]),
        )
        if reply == "Y":
            GitManager.commit_with_message(merge_msg)
            raise click.Abort()

    model_id = config_manager.get_openai_chat_model()
    model = ai_manager.get_model_info(model_id)

    # No preconfigured commit message, so generate
    can_gen = ai_manager.can_generate_commit_message(model, stats, diffs, commit_type)
    if not can_gen:
        click.echo(
            "Changes are too large to generate a commit message. Opening editor."
        )
        GitManager.commit_with_message(commit_type['value'])
    else:
        need_regenerate = True
        while need_regenerate:
            commit_msg = ai_manager.generate_commit_message(
                model, stats, diffs, commit_type['value']
            )
            click.echo(f"Generated commit message: {commit_msg}")
            reply = click.prompt(
                "Continue, regenerate or quit?",
                default="C",
                show_choices=True,
                type=click.Choice(["C", "r", "q"]),
            )
            if reply == "C":
                GitManager.commit_with_message(commit_msg)
                need_regenerate = False
            elif reply == "r":
                need_regenerate = True
            elif reply == "q":
                raise click.Abort()
            else:
                click.echo("Error: Invalid choice.")
                raise click.Abort()


@aimojicommit.command("set-model")
@click.argument("model", default=None)
def set_model_cmd(model):
    config_manager = ConfigManager()
    config_manager.load_config()
    ai_manager = AIManager(config_manager)
    set_model(model, config_manager, ai_manager)


@aimojicommit.command("set-key")
@click.argument("key", default=None)
def set_key_cmd(key):
    config_manager = ConfigManager()
    config_manager.load_config()
    set_key(key, config_manager)


if __name__ == "__main__":
    aimojicommit()
