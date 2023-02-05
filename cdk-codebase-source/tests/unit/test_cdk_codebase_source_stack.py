import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_codebase_source.cdk_codebase_source_stack import CdkCodebaseSourceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_codebase_source/cdk_codebase_source_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkCodebaseSourceStack(app, "cdk-codebase-source")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
