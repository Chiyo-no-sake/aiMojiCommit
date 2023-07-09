import yaml
import os
import requests
from pathlib import Path
from aimojicommit import constants

class ConfigManager:
    def __init__(self):
        homedir = str(Path.home())
        self.root_folder = os.path.join(homedir, constants.aimoji_root_folder_name)
        self.file_path = os.path.join(self.root_folder, constants.config_file_name)
        self.config = None


    def load_config(self) -> None:
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)

        if not os.path.exists(self.file_path):
            resp = requests.get(constants.remote_default_config_url, stream=True)
            with open(self.file_path, 'wb') as file:
                for chunk in resp.iter_content(chunk_size=1024):
                    file.write(chunk)
        
        with open(self.file_path, "r") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def get_value(self, key: str, default = None):
        if self.config is None:
            self.load_config()
        return self.config.get(key, default)

    def get_commit_types(self):
        if self.config is None:
            self.load_config()
        return self.get_value('commit_types')

    def get_openai_api_key(self):
        if self.config is None:
            self.load_config()
        return self.get_value('openai_api_key')
    
    def set_openai_api_key(self, key: str):
        if self.config is None:
            self.load_config()
        self.config['openai_api_key'] = key
        self.save_config()

    def get_openai_chat_model(self):
        if self.config is None:
            self.load_config()
        return self.get_value('openai_chat_model')
    
    def set_openai_chat_model(self, model: str):
        if self.config is None:
            self.load_config()
        self.config['openai_chat_model'] = model
        self.save_config()

    def save_config(self) -> None:
        with open(self.file_path, "w") as file:
            yaml.dump(self.config, file)