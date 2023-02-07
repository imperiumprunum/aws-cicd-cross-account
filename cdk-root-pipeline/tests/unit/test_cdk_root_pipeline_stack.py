import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_root_pipeline.cdk_root_pipeline_stack import CdkRootPipelineStack


# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_root_pipeline/cdk_root_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkRootPipelineStack(app, "cdk-root-pipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
