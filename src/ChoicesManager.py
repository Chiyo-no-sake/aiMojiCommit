import pick
from ConfigManager import ConfigManager

class ChoicesManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def choose_commit_type(self):
        commit_types = self.config_manager.get_value("commit_types", [])
        options = [
            {"name": f"{type['prefix']}: {type['detail']}", "value": type['prefix']}
            for type in commit_types
        ]

        if not options:
            raise ValueError("No commit types found in the configuration.")

        title = "Choose a commit type"
        optionName, _ = pick.pick([option["name"] for option in options], title)

        option = next(option for option in options if option["name"] == optionName)

        return option

    def choose_option(self, title: str, options: list[str]) -> str:
        option, _ = pick.pick(options, title)
        return option
