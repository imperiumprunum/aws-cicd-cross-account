import pytest
import os
import pprint

from cdk_root_pipeline.component_config import ComponentConfig


@pytest.fixture
def component_config():
    #return ComponentConfig(config_path=f'{os.getcwd()}/tests/config_test.yml')
    return ComponentConfig()


def test_component_config(component_config):
    print(f" ComponentConfig: {component_config.content}")
    assert isinstance(component_config.content, dict)
