from typing import Optional

from aws_cdk import Tags

import cdk_root_pipeline.constants as constants
from cdk_root_pipeline.component_config import ComponentConfig


def get_resource_name(
        resource_name: str,
        resource_type: str,
        environment: Optional[str] = None,
        component_name: Optional[str] = None,
        project_name: Optional[str] = ComponentConfig.PROJECT_NAME, ):
    if not environment and not component_name:
        return f"{resource_name}-{resource_type}-{project_name}"
    if component_name:
        return f"{environment}-{component_name}-{resource_name}-{resource_type}-{project_name}"
    return f"{environment}-{resource_name}-{resource_type}-{project_name}"


def get_resource_name_OLD(self, resource_type: str, resource_name: str = None):
    if not self.environment:
        raise ComponentConfigExceptions(
            f'Method get_resource_name requires parameter environment not equal to {self.environment}')
    if not resource_name and self.environment == 'global':
        # ex. ingestion-codecommit-thy, ingestion-YY-lambda-thy
        return f"{self.component_name}-{resource_type}-{self.project_name}"
    if not resource_name:
        # ex. dev-ingestion-codecommit-thy, dev-ingestion-YY-lambda-thy
        return f"{self.environment}-{self.component_name}-{resource_type}-{self.project_name}"
    else:
        # ex. dev-ingestion-mailloader-lambda-thy, dev-ingestion-YY-lambda-thy
        return f"{self.environment}-{self.component_name}-{resource_name}-{resource_type}-{self.project_name}"


class ComponentConfigExceptions(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __repr__(self):
        print(self.msg)


def tagged(func):
    # @decorator for adding tags to resources
    def wrapper(*args, **kwargs):
        resource = func(*args, **kwargs)
        Tags.of(resource).add('Owner', constants.OWNER)
        return resource

    return wrapper


def resolve_branch_name(environment: str) -> str:
    if environment == "dev":
        return "develop"
    if environment == "stg":
        return "stage"
    if environment == "prod":
        return "production"
    return "master"
