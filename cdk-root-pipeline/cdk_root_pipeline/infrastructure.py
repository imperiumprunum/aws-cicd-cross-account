from typing import Optional, Dict, List

from aws_cdk import (
    Stack,
    aws_codecommit,
    aws_codepipeline,
    aws_codepipeline_actions,
    aws_codebuild,
    aws_iam
)
from constructs import Construct

from cdk_root_pipeline.config_loader import ConfigLoader
import cdk_root_pipeline.utils as utils
import cdk_root_pipeline.constants as constants


class RootPipeline(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        repo_name = utils.get_resource_name(
            resource_name='rootbootstrap',
            resource_type='repo',
        )
        root_repo = self.create_code_commit(
            resource_id=repo_name,
            repo_name=repo_name
        )
        self.__init_pipeline(
            repo=root_repo
        )

        # =====================END OF INIT=======================================

    def create_code_commit(self, resource_id: str, repo_name: str):
        my_repo = aws_codecommit.Repository(
            self,
            id=resource_id,
            repository_name=repo_name,
            description=f"Bootstrap CodeCommit repository.",
        )
        return my_repo

    def create_code_build(
            self,
            resource_id: str,
            project_name: str,
            env_vars: Optional[Dict] = None,
    ) -> aws_codebuild.PipelineProject:
        # Avoid default mutable argument
        if not env_vars:
            env_vars = {}
        # Create CodeBuild instance
        return aws_codebuild.PipelineProject(
            self,
            id=resource_id,
            project_name=project_name,
            build_spec=aws_codebuild.BuildSpec.from_source_filename(
                filename=constants.DEFAULT_BUILDSPECT_PATH
            ),
            environment=aws_codebuild.BuildEnvironment(
                build_image=aws_codebuild.LinuxBuildImage.STANDARD_5_0,
                privileged=True,
                compute_type=aws_codebuild.ComputeType.SMALL,
            ),
            environment_variables=env_vars,
        )

    def create_code_build_action(
            self,
            action_name: str,
            project: aws_codebuild.PipelineProject,
            action_artifact_trigger: aws_codepipeline.Artifact,
            outputs: Optional[List[aws_codepipeline.Artifact]] = None,
    ) -> aws_codepipeline.Action:
        if not outputs:
            outputs = [aws_codepipeline.Artifact()]

        return aws_codepipeline_actions.CodeBuildAction(
            action_name=action_name,
            project=project,
            input=action_artifact_trigger,  # The build action must use the CodeCommitSourceAction output as input.
            outputs=outputs,
        )

    def __init_pipeline(self, repo: aws_codecommit.Repository) -> None:
        # Create pipeline
        pipeline_name = utils.get_resource_name(
            resource_name='rootbootstrap',
            resource_type='pipeline',
        )
        pipeline = aws_codepipeline.Pipeline(
            self,
            id=pipeline_name,
            pipeline_name=pipeline_name,
            cross_account_keys=False,
        )

        # Create pipeline trigger - listen for commit in my_repo on specified branch
        source_output = aws_codepipeline.Artifact("SourceArtifact")

        source_action = aws_codepipeline_actions.CodeCommitSourceAction(
            action_name=f"{ConfigLoader.DEFAULT_BRANCH_NAME}-on-commit",
            branch=ConfigLoader.DEFAULT_BRANCH_NAME,
            repository=repo,
            output=source_output,
        )
        pipeline.add_stage(stage_name="Source", actions=[source_action])

        cb_project_name = utils.get_resource_name(
            resource_name='rootbootstrap',
            resource_type='cb',
        )
        cb_project = self.create_code_build(
            resource_id=cb_project_name,
            project_name=cb_project_name,
        )
        cb_project.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=["*"],
                resources=["*"]))

        build_action = self.create_code_build_action(
            action_name="CodeBuild",
            project=cb_project,
            action_artifact_trigger=source_output
        )

        pipeline.add_stage(stage_name="Build", actions=[build_action])
