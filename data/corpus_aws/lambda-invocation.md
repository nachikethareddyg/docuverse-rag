# Understanding Lambda function invocation methods

After you deploy your Lambda function, you can invoke it in several ways:

* The [Lambda console](./testing-functions.html) â Use the
  Lambda console to quickly create a test event to invoke your function.
* The [AWS SDK](https://aws.amazon.com/developer/tools/)
  â Use the AWS SDK to programmatically invoke your function.
* The [Invoke](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html) API â Use the Lambda Invoke API to directly invoke
  your function.
* The [AWS Command Line Interface (AWS CLI)](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/invoke.html) â Use the `aws lambda invoke`
  AWS CLI command to directly invoke your function from the command line.
* A [function URL HTTP(S) endpoint](./urls-configuration.html) â
  Use function URLs to create a dedicated HTTP(S) endpoint that you can use to
  invoke your function.

All of these methods are *direct* ways to invoke your function.
In Lambda, a common use case is to invoke your function based on an event that occurs
elsewhere in your application. Some services can invoke a Lambda function with each new event. This is called a [trigger](./lambda-services.html). For stream and queue-based services, Lambda invokes the function with batches of records. This is called an [event source mapping](./invocation-eventsourcemapping.html).

When you invoke a function, you can choose to invoke it synchronously or
asynchronously. With [synchronous invocation](./invocation-sync.html),
you wait for the function to process the event and return a response. With
[asynchronous invocation](./invocation-async.html), Lambda queues the
event for processing and returns a response immediately. The [`InvocationType` request parameter in the Invoke API](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html#API_Invoke_RequestParameters) determines
how Lambda invokes your function. A value of `RequestResponse` indicates
synchronous invocation, and a value of `Event` indicates asynchronous
invocation.

To invoke your function over IPv6, use Lambda's public [dual-stack endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#dual-stack-endpoints). Dual-stack endpoints support both IPv4 and IPv6. Lambda dual-stack endpoints use the following syntax:

```
protocol://lambda.us-east-1.api.aws
```

You can also use [Lambda function URLs](./urls-configuration.html) to invoke functions over IPv6. Function URL endpoints have the following format:

```
https://url-id.lambda-url.us-east-1.on.aws
```

If the function invocation results in an error, for synchronous invocations,
view the error message in the response and retry the invocation manually. For
asynchronous invocations, Lambda handles retries automatically and can send invocation
records to a [destination](./invocation-async-retain-records.html#invocation-async-destinations).

[Document Conventions](/general/latest/gr/docconventions.html)

Metadata endpoint

Invoke a function synchronously
