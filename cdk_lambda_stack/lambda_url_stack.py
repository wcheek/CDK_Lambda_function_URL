from aws_cdk import CfnResource, Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as _lambda_python
from constructs import Construct


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # in __init__ I like to initialize the infrastructure I will be creating
        self.example_lambda = None

        self.build_infrastructure()

    def build_infrastructure(self):
        # For convenience, consolidate infrastructure construction
        self.build_lambda()

    def build_lambda(self):
        self.example_lambda = _lambda_python.PythonFunction(
            scope=self,
            id="ExampleLambda",
            # entry points to the directory
            entry="lambda_funcs/LambdaURL",
            # index is the file name
            index="URL_lambda.py",
            # handler is the function entry point name in the lambda.py file
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            # name of function on AWS
            function_name="ExampleLambdaFunctionURL",
        )

        # Set up the Lambda Function URL
        CfnResource(
            scope=self,
            id="lambdaFuncUrl",
            type="AWS::Lambda::Url",
            properties={
                "TargetFunctionArn": self.example_lambda.function_arn,
                "AuthType": "NONE",
                "Cors": {"AllowOrigins": ["*"]},
            },
        )

        # Give everyone permission to invoke the Function URL
        CfnResource(
            scope=self,
            id="funcURLPermission",
            type="AWS::Lambda::Permission",
            properties={
                "FunctionName": self.example_lambda.function_name,
                "Principal": "*",
                "Action": "lambda:InvokeFunctionUrl",
                "FunctionUrlAuthType": "NONE",
            },
        )
