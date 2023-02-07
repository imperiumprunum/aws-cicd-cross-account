from aws_cdk import (
    Stack,
    aws_codecommit,
    aws_codepipeline,
    aws_codepipeline_actions,
    aws_codebuild,
    aws_iam
)
from constructs import Construct

from cdk_root_pipeline.component_config import ComponentConfig


class CdkRootPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # =====================END OF INIT=======================================

    def create_code_commit(self, resource_id: str, repo_name: str):
        my_repo = aws_codecommit.Repository(
            self,
            id=resource_id,
            repository_name=repo_name,
            description=f"Bootstrap CodeCommit repository.",
        )
        return my_repo

    def __init_pipeline(
            self, component: ComponentConfig, repo: aws_codecommit.Repository
    ) -> None:
        # Create pipeline
        pipeline = aws_codepipeline.Pipeline(
            self,
            id=component.get_resource_name(resource_type="pipeline"),
            pipeline_name=component.get_resource_name(resource_type="pipeline"),
            cross_account_keys=False,
        )

        # Create pipeline trigger - listen for commit in my_repo on specified branch
        source_output = aws_codepipeline.Artifact("SourceArtifact")
        branch_name = self.resolve_branch_name(component.environment)

        source_action = aws_codepipeline_actions.CodeCommitSourceAction(
            action_name=f"{branch_name}-on-commit",
            branch=branch_name,
            repository=repo,
            output=source_output,
        )
        pipeline.add_stage(stage_name="Source", actions=[source_action])

        my_project = self.create_code_build(
            resource_id=component.get_resource_name(resource_type="cb"),
            project_name=component.get_resource_name(resource_type="cb"),
            env_vars={
                'environment': aws_codebuild.BuildEnvironmentVariable(value=component.environment),
                'component': aws_codebuild.BuildEnvironmentVariable(value=component.component_name)
            }
        )
        my_project.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=["*"],
                resources=["*"]))

        build_action = self.create_code_build_action(
            action_name="CodeBuild",
            project=my_project,
            action_artifact_trigger=source_output
        )

        pipeline.add_stage(stage_name="Build", actions=[build_action])
