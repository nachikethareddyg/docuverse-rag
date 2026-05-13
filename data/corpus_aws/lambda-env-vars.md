# Working with Lambda environment variables

You can use environment variables to adjust your function's behavior without updating code. An environment
variable is a pair of strings that is stored in a function's version-specific configuration. The Lambda runtime makes
environment variables available to your code and sets additional environment variables that contain information
about the function and invocation request.

###### Note

To increase security, we recommend that you use AWS Secrets Manager instead of environment variables to store
database credentials and other sensitive information like API keys or authorization tokens. For more information, see [Use Secrets Manager secrets in Lambda functions](./with-secrets-manager.html).

Environment variables are not evaluated before the function invocation. Any value you define is considered a
literal string and not expanded. Perform the variable evaluation in your function code.

## Creating Lambda environment variables

You can configure environment variables in Lambda using the Lambda console, the AWS Command Line Interface (AWS CLI), AWS Serverless Application Model (AWS SAM), or using an AWS SDK.

Console
:   You define environment variables on the unpublished version of your function. When you publish a version, the
    environment variables are locked for that version along with other [version-specific configuration settings](./configuration-versions.html).

    You create an environment variable for your function by defining a key and a value. Your function uses the
    name of the key to retrieve the value of the environment variable.

    ###### To set environment variables in the Lambda console

    1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.
    2. Choose a function.
    3. Choose the **Configuration** tab, then choose **Environment variables**.
    4. Under **Environment variables**, choose **Edit**.
    5. Choose **Add environment variable**.
    6. Enter a key and value.

       ###### Requirements

       * Keys start with a letter and are at least two characters.
       * Keys only contain letters, numbers, and the underscore character (`_`).
       * Keys aren't [reserved by Lambda](#configuration-envvars-runtime).
       * The total size of all environment variables doesn't exceed 4 KB.
    7. Choose **Save**.

    ###### To generate a list of environment variables in the console code editor

    You can generate a list of environment variables in the Lambda code editor. This is a quick way to reference
    your environment variables while you code.

    1. Choose the **Code** tab.
    2. Scroll down to the **ENVIRONMENT VARIABLES** section of the code editor. Existing environment variables are listed here:

       ![ENVIRONMENT VARIABLES section of the Lambda console code editor](/images/lambda/latest/dg/images/env-var.png)
    3. To create new environment variables, choose the choose the plus sign (
       ![plus sign](/images/lambda/latest/dg/images/add-plus.png)
       ):

       ![Add environment variables in the Lambda console code editor](/images/lambda/latest/dg/images/create-env-var.png)

    Environment variables remain encrypted when listed in the console code editor. If you enabled encryption helpers for encryption in transit, then those settings remain unchanged. For more information, see [Securing Lambda environment variables](./configuration-envvars-encryption.html).

    The environment variables list is read-only and is available only on the Lambda console. This file is not included when you download the function's .zip file archive, and you can't add environment variables by uploading this file.

AWS CLI
:   The following example sets two environment variables on a function named `my-function`.

    ```
    aws lambda update-function-configuration \
      --function-name my-function \
      --environment "Variables={BUCKET=amzn-s3-demo-bucket,KEY=file.txt}"
    ```

    When you apply environment variables with the `update-function-configuration` command, the entire
    contents of the `Variables` structure is replaced. To retain existing environment variables when you
    add a new one, include all existing values in your request.

    To get the current configuration, use the `get-function-configuration` command.

    ```
    aws lambda get-function-configuration \
      --function-name my-function
    ```

    You should see the following output:

    ```
    {
        "FunctionName": "my-function",
        "FunctionArn": "arn:aws:lambda:us-east-2:111122223333:function:my-function",
        "Runtime": "nodejs24.x",
        "Role": "arn:aws:iam::111122223333:role/lambda-role",
        "Environment": {
            "Variables": {
                "BUCKET": "amzn-s3-demo-bucket",
                "KEY": "file.txt"
            }
        },
        "RevisionId": "0894d3c1-2a3d-4d48-bf7f-abade99f3c15",
        ...
    }
    ```

    You can pass the revision ID from the output of `get-function-configuration` as a parameter to
    `update-function-configuration`. This ensures that the values don't change between when you read the
    configuration and when you update it.

    To configure a function's encryption key, set the `KMSKeyARN` option.

    ```
    aws lambda update-function-configuration \
      --function-name my-function \
      --kms-key-arn arn:aws:kms:us-east-2:111122223333:key/055efbb4-xmpl-4336-ba9c-538c7d31f599
    ```

AWS SAM
:   You can use the [AWS Serverless Application Model](https://docs.aws.amazon.com//serverless-application-model/latest/developerguide/serverless-getting-started.html ) to configure environment variables for your function. Update the [Environment](https://docs.aws.amazon.com//serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-environment) and [Variables](https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-environment.html#cfn-lambda-function-environment-variables) properties in your `template.yaml` file and then run [sam deploy](https://docs.aws.amazon.com//serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html).

    ###### Example template.yaml

    ```
    AWSTemplateFormatVersion: '2010-09-09'
    Transform: AWS::Serverless-2016-10-31
    Description: An AWS Serverless Application Model template describing your function.
    Resources:
      my-function:
        Type: AWS::Serverless::Function
        Properties:
          CodeUri: .
          Description: ''
          MemorySize: 128
          Timeout: 120
          Handler: index.handler
          Runtime: nodejs24.x
          Architectures:
            - x86_64
          EphemeralStorage:
            Size: 10240
          Environment:
            Variables:
              BUCKET: amzn-s3-demo-bucket
              KEY: file.txt
          # Other function properties...
    ```

AWS SDKs
:   To manage environment variables using an AWS SDK, use the following API operations.

    * [UpdateFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html)
    * [GetFunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_GetFunctionConfiguration.html)
    * [CreateFunction](https://docs.aws.amazon.com/lambda/latest/api/API_CreateFunction.html)

    To learn more, refer to the [AWS SDK documentation](https://aws.amazon.com/developer/tools/) for your preferred programming language.

## Example scenario for environment variables

You can use environment variables to customize function behavior in your test environment and production
environment. For example, you can create two functions with the same code but different configurations. One
function connects to a test database, and the other connects to a production database. In this situation, you use
environment variables to pass the hostname and other connection details for the database to the function.

The following example shows how to define the database host and database name as environment variables.

![Environment variables in the Lambda console.](/images/lambda/latest/dg/images/console-env.png)

If you want your test environment to generate more debug information than the production environment, you
could set an environment variable to configure your test environment to use more verbose logging or more detailed
tracing.

For example, in your test environment, you could set an environment variable with the key `LOG_LEVEL` and a value indicating a log level of
debug or trace. In your Lambda function's code, you can then use this environment variable to set the log level.

The following code examples in Python and Node.js illustrate how you can achieve this. These examples assume your environment variable has a
value of `DEBUG` in Python or `debug` in Node.js.

Python
:   ###### Example Python code to set log level

    ```
    import os
    import logging

    # Initialize the logger
    logger = logging.getLogger()

    # Get the log level from the environment variable and default to INFO if not set
    log_level = os.environ.get('LOG_LEVEL', 'INFO')

    # Set the log level
    logger.setLevel(log_level)

    def lambda_handler(event, context):
        # Produce some example log outputs
        logger.debug('This is a log with detailed debug information - shown only in test environment')
        logger.info('This is a log with standard information - shown in production and test environments')
    ```

Node.js (ES module format)
:   ###### Example Node.js code to set log level

    This example uses the `winston` logging library. Use npm to add this library to your function's deployment package. For more information, see
    [Creating a .zip deployment package with dependencies](./nodejs-package.html#nodejs-package-create-dependencies).

    ```
    import winston from 'winston';

    // Initialize the logger using the log level from environment variables, defaulting to INFO if not set
    const logger = winston.createLogger({
       level: process.env.LOG_LEVEL || 'info',
       format: winston.format.json(),
       transports: [new winston.transports.Console()]
    });

    export const handler = async (event) => {
       // Produce some example log outputs
       logger.debug('This is a log with detailed debug information - shown only in test environment');
       logger.info('This is a log with standard information - shown in production and test environment');

    };
    ```

## Retrieving Lambda environment variables

To retrieve environment variables in your function code, use the standard method for your programming
language.

Node.js
:   ```
    let region = process.env.AWS_REGION
    ```

Python
:   ```
    import os
      region = os.environ['AWS_REGION']
    ```

    ###### Note

    In some cases, you may need to use the following format:

    ```
    region = os.environ.get('AWS_REGION')
    ```

Ruby
:   ```
    region = ENV["AWS_REGION"]
    ```

Java
:   ```
    String region = System.getenv("AWS_REGION");
    ```

Go
:   ```
    var region = os.Getenv("AWS_REGION")
    ```

C#
:   ```
    string region = Environment.GetEnvironmentVariable("AWS_REGION");
    ```

PowerShell
:   ```
    $region = $env:AWS_REGION
    ```

Lambda stores environment variables securely by encrypting them at rest. You can [configure Lambda to use a different encryption key](./configuration-envvars-encryption.html), encrypt
environment variable values on the client side, or set environment variables in an CloudFormation template with
AWS Secrets Manager.

## Defined runtime environment variables

Lambda [runtimes](./lambda-runtimes.html) set several environment variables during initialization.
Most of the environment variables provide information about the function or runtime. The keys for these
environment variables are *reserved* and cannot be set in your function configuration.

###### Reserved environment variables

* `_HANDLER` â The handler location configured on the function.
* `_X_AMZN_TRACE_ID` â The [X-Ray tracing
  header](./services-xray.html). This environment variable changes with each invocation.

  + This environment variable is not defined for OS-only runtimes (the `provided` runtime family).
    You can set `_X_AMZN_TRACE_ID` for custom runtimes using the
    `Lambda-Runtime-Trace-Id` response header from the
    [Next invocation](./runtimes-api.html#runtimes-api-next).
  + For Java runtime versions 17 and later, this environment variable is not used.
    Instead, Lambda stores tracing information in the `com.amazonaws.xray.traceHeader`
    system property.
* `AWS_DEFAULT_REGION` â The default AWS Region where the Lambda function is executed.
* `AWS_REGION` â The AWS Region where the Lambda function is executed. If defined, this value overrides the `AWS_DEFAULT_REGION`.

  + For more information about using the AWS Region environment variables with AWS SDKs, see [AWS Region](https://docs.aws.amazon.com/sdkref/latest/guide/feature-region.html#feature-region-sdk-compat)
    in the *AWS SDKs and Tools Reference Guide*.
* `AWS_EXECUTION_ENV` â The [runtime identifier](./lambda-runtimes.html),
  prefixed by `AWS_Lambda_` (for example, `AWS_Lambda_java8`). This environment variable is not defined for OS-only runtimes (the `provided` runtime family).
* `AWS_LAMBDA_FUNCTION_NAME` â The name of the function.
* `AWS_LAMBDA_FUNCTION_MEMORY_SIZE` â The amount of memory available to the function in
  MB.
* `AWS_LAMBDA_FUNCTION_VERSION` â The version of the function being
  executed.
* `AWS_LAMBDA_INITIALIZATION_TYPE` â The initialization type of the function, which is `on-demand`, `provisioned-concurrency`, `snap-start`, or `lambda-managed-instances`. For information, see [Configuring provisioned concurrency](./provisioned-concurrency.html), [Improving startup performance with Lambda SnapStart](./snapstart.html), or [Lambda Managed Instances](./lambda-managed-instances.html).
* `AWS_LAMBDA_LOG_GROUP_NAME`, `AWS_LAMBDA_LOG_STREAM_NAME` â The name of the
  Amazon CloudWatch Logs group and stream for the function. The `AWS_LAMBDA_LOG_GROUP_NAME` and `AWS_LAMBDA_LOG_STREAM_NAME` environment variables are not available in Lambda SnapStart functions.
* `AWS_ACCESS_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`
  â The access keys obtained from the function's [execution
  role](./lambda-intro-execution-role.html).
* `AWS_LAMBDA_RUNTIME_API` â ([Custom runtime](./runtimes-custom.html)) The
  host and port of the [runtime API](./runtimes-api.html).
* `LAMBDA_TASK_ROOT` â The path to your Lambda function code.
* `LAMBDA_RUNTIME_DIR` â The path to runtime libraries.
* `AWS_LAMBDA_MAX_CONCURRENCY` â (Lambda Managed Instances only) The maximum number of concurrent invocations Lambda will send to one execution environment.
* `AWS_LAMBDA_METADATA_API` â The [metadata endpoint](./configuration-metadata-endpoint.html) server address in the format
  `{ipv4_address}:{port}` (for example, `169.254.100.1:9001`).
* `AWS_LAMBDA_METADATA_TOKEN` â A unique authentication token for the current
  execution environment used to authenticate requests to the [metadata endpoint](./configuration-metadata-endpoint.html). Lambda generates this token automatically at initialization.

The following additional environment variables aren't reserved and can be extended in your function
configuration.

###### Unreserved environment variables

* `LANG` â The locale of the runtime (`en_US.UTF-8`).
* `PATH` â The execution path
  (`/usr/local/bin:/usr/bin/:/bin:/opt/bin`).
* `LD_LIBRARY_PATH` â The system library path
  (`/var/lang/lib:/lib64:/usr/lib64:$LAMBDA_RUNTIME_DIR:$LAMBDA_RUNTIME_DIR/lib:$LAMBDA_TASK_ROOT:$LAMBDA_TASK_ROOT/lib:/opt/lib`).
* `NODE_PATH` â ([Node.js](./lambda-nodejs.html)) The Node.js library path
  (`/opt/nodejs/node12/node_modules/:/opt/nodejs/node_modules:$LAMBDA_RUNTIME_DIR/node_modules`).
* `NODE_OPTIONS` â ([Node.js](./lambda-nodejs.html)) For
  Node.js runtimes, you can use `NODE_OPTIONS` to re-enable experimental features
  that Lambda disables by default.
* `PYTHONPATH` â ([Python](./lambda-python.html)) The Python
  library path (`$LAMBDA_RUNTIME_DIR`).
* `GEM_PATH` â ([Ruby](./lambda-ruby.html)) The Ruby library path
  (`$LAMBDA_TASK_ROOT/vendor/bundle/ruby/3.3.0:/opt/ruby/gems/3.3.0`).
* `AWS_XRAY_CONTEXT_MISSING` â For X-Ray tracing, Lambda sets this to
  `LOG_ERROR` to avoid throwing runtime errors from the X-Ray SDK.
* `AWS_XRAY_DAEMON_ADDRESS` â For X-Ray tracing, the IP address and port of the X-Ray
  daemon.
* `AWS_LAMBDA_DOTNET_PREJIT` â ([.NET](./lambda-csharp.html)) Set this variable to enable or
  disable .NET specific runtime optimizations. Values include `always`, `never`, and
  `provisioned-concurrency`. For more information, see [Configuring provisioned concurrency for a function](./provisioned-concurrency.html).
* `TZ` â The environment's time zone (`:UTC`). The execution environment uses
  NTP to synchronize the system clock.

The sample values shown reflect the latest runtimes. The presence of specific variables or their values can
vary on earlier runtimes.

[Document Conventions](/general/latest/gr/docconventions.html)

Timeout

Securing environment variables
