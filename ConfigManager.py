import yaml
from injector import inject

class ConfigManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = None

    def load_config(self) -> None:
        with open(self.file_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get_value(self, key: str, default: Any = None) -> Any:
        if self.config is None:
            self.load_config()
        return self.config.get(key, default)

    def set_value(self, key: str, value: Any) -> None:
        if self.config is None:
            self.load_config()
        self.config[key] = value

    def save_config(self) -> None:
        with open(self.file_path, "w") as file:
            yaml.dump(self.config, file)


@inject
class ConfigManagerInjector(ConfigManager):
    def __init__(self, file_path: str):
        super().__init__(file_path)