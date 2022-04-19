# AWS Lambda Function URLs with AWS CDK

AWS recently released a great new feature for Lambda: [AWS Lambda Function URLs](https://aws.amazon.com/blogs/aws/announcing-aws-lambda-function-urls-built-in-https-endpoints-for-single-function-microservices/)

Function URLs promise to replace the API Gateway Lambda Proxy pattern as they allow a simpler way to do `HTTP GET` operations on your Lambda functions.

The [Github repository can be found here.](https://github.com/wcheek/CDK_Lambda_function_URL)

## CDK init & deploy

I won’t cover setting up CDK and bootstrapping the environment. You can find that information [here.](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

Once you have set up CDK, we need to set up the project:

1. `mkdir CDK_Lambda_URL && cd CDK_Lambda_URL`

2. `cdk init --language python`

3. `source .venv/bin/activate`

4. Optional: If you need additional libraries in your Lambda function, add `aws-cdk.aws-lambda-python-alpha` to requirements.txt to allow custom builds during stack deployment using Docker.

5. `pip install -r requirements.txt && pip install -r requirements-dev.txt`

    Now deploy empty stack to AWS:

6. `cdk deploy`

## Stack design

This stack will deploy a lambda function using `aws-lambda-python-alpha` to build the function with all its additional libraries using a docker container. Make sure to have Docker installed and the daemon running before running `cdk deploy`.

```python
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

```

## Minimum Working Lambda Function

You can see [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html) an example of the response format the API gateway is expecting.

```python
from logging import getLogger

logger = getLogger()
logger.setLevel(level="DEBUG")


def handler(event, context):
    logger.debug(msg=f"Initial event: {event}")
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": f"Nice! You said {event['queryStringParameters']['q']}",
    }
    return response

```

Now you can do `cdk deploy`. The lambda function will be built using docker and uploaded to the bootstrapped ECR repository. Once the project is built, it will synth a `CloudFormation` template and begin deploying the infrastructure. You can watch your stack deploy on `AWS CloudFormation` - it should be quick since the infrastructure is relatively simple.

So far I have unfortunately not found a way to output the Function URL using `AWS CDK` (please let me know in comments if you know how), so unfortunately once the process is completed it will be necessary to navigate to your Lambda function on the `AWS Console` to find your `Lambda Function URL`

![aws_console](D:\Projects\Notes\My Articles\2_CDK_Lambda_function_URL\Assets\aws_console.png)

## Query the API Gateway

To query the `Function URL` and get a response back from your lambda function, just send a `GET` request using `requests` or `Postman`

![image-20220419164801774](D:\Projects\Notes\My Articles\2_CDK_Lambda_function_URL\Assets\image-20220419164801774.png)

