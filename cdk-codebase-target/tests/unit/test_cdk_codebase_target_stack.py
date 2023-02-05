import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_codebase_target.cdk_codebase_target_stack import CdkCodebaseTargetStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_codebase_target/cdk_codebase_target_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkCodebaseTargetStack(app, "cdk-codebase-target")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
