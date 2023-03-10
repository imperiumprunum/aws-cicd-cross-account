import yaml

import cdk_root_pipeline.constants as constants


class ConfigLoader:
    PROJECT_NAME = None
    DEFAULT_BRANCH_NAME = None

    def __init__(self) -> None:
        self.config_path = constants.DEFAULT_COMPONENT_CONFIG_PATH
        self.content = self.load_cfg(self.config_path)

        self.setup = self.content.get("setup")
        ConfigLoader.PROJECT_NAME = self.setup["project_name"]
        ConfigLoader.DEFAULT_BRANCH_NAME = self.setup["default_branch_name"]
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


# enforce ConfigLoader.PROJECT_NAME on import
cc = ConfigLoader()
