from typing import Optional

import yaml

import cdk_root_pipeline.constants as constants


class ComponentConfig:

    def __init__(self, config_path: Optional[str] = constants.DEFAULT_COMPONENT_CONFIG_PATH) -> None:
        self.config_path = config_path
        self.content = self.load_cfg(self.config_path)

        self.setup = self.content.get("setup")
        self.resources = self.content.get("resources")

    def load_cfg(self, config_path: str):
        reader = open(config_path)
        content = reader.read()
        content_as_dict = yaml.safe_load(content)
        if self.config_valid(content):
            return content_as_dict
        else:
            raise InvalidConfigFileException

    @staticmethod
    def config_valid(config_content):
        # TODO: Implement config validation
        return True

    def __repr__(self) -> str:
        return str(self.content)


class InvalidConfigFileException(Exception):
    def __init__(self):
        super().__init__()
