import aws_cdk as cdk

from cdk_lambda_stack.lambda_url_stack import LambdaStack

app = cdk.App()
LambdaStack(app, "ExampleLambdaURLStack")

app.synth()
