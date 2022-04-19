# Deploy a Lambda function with Function URL using AWS CDK

This project quickly deploys a [Lambda Function URL](https://aws.amazon.com/blogs/aws/announcing-aws-lambda-function-urls-built-in-https-endpoints-for-single-function-microservices/) fronted custom Lambda function using AWS CDK.
Through the Function URL, the Lambda function can be queried by any web client to provide machine learning predictions and other tasks.

The Dev.to article [can be found here](https://dev.to/wesleycheek/aws-lambda-function-urls-with-aws-cdk-58ih)

## If starting from scratch:

1) `mkdir project && cd project`
2) `cdk init --language python`
3) Follow instructions below to activate venv, install libraries.
Note: Besides for the standard cdk libraries, you should include `aws-cdk.aws-lambda-python-alpha`.
This experimental library allows CDK to build the Lambda function including additional libraries at deployment time.
You will need `Docker` to use this deployment method.
4) Make sure you have activated your AWS credentials and `cdk deploy`



## Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
