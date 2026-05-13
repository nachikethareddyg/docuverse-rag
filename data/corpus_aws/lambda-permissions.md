# Managing permissions in AWS Lambda

You can use AWS Identity and Access Management (IAM) to manage permissions in AWS Lambda. There are two main
categories of permissions that you need to consider when working with Lambda functions:

* Permissions that your Lambda functions need to perform API actions and access
  other AWS resources
* Permissions that other AWS users and entities need to access your Lambda
  functions

Lambda functions often need to access other AWS resources, and perform various API
operations on those resources. For example, you might have a Lambda function that responds
to an event by updating entries in an Amazon DynamoDB database. In this case, your function
needs permissions to access the database, as well as permissions to put or update items
in that database.

You define the permissions that your Lambda function needs in a special IAM role
called an [execution role](./lambda-intro-execution-role.html). In this
role, you can attach a policy that defines every permission your function needs to
access other AWS resources, and read from event sources. Every Lambda function must
have an execution role. At a minimum, your execution role must have access to
Amazon CloudWatch because Lambda functions log to CloudWatch Logs by default. You can attach the
[`AWSLambdaBasicExecutionRole` managed policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLambdaBasicExecutionRole.html) to your execution
role to satisfy this requirement.

To give other AWS accounts, organizations, and services permissions to access
your Lambda resources, you have a few options:

* You can use [identity-based policies](./access-control-identity-based.html)
  to grant other users access to your Lambda resources. Identity-based policies can
  apply to users directly, or to groups and roles that are associated with a user.
* You can use [resource-based policies](./access-control-resource-based.html)
  to give other accounts and AWS services permissions to access your Lambda resources.
  When a user tries to access a Lambda resource, Lambda considers both the user's
  identity-based policies and the resource's resource-based policy. When an AWS service
  such as Amazon Simple Storage Service (Amazon S3) calls your Lambda function, Lambda considers only the
  resource-based policy.
* You can use an [attribute-based
  access control (ABAC)](./attribute-based-access-control.html) model to control access to your Lambda functions. With
  ABAC, you can attach tags to a Lambda function, pass them in certain API requests,
  or attach them to the IAM principal making the request. Specify the same tags
  in the condition element of an IAM policy to control function access.

In AWS, it's a best practice to grant only the permissions required to perform a
task ([least-privilege
permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege)). To implement this in Lambda, we recommend starting with an
[AWS managed policy](./permissions-managed-policies.html). You can use
these managed policies as-is, or as a starting point for writing your own more
restrictive policies.

To help you fine-tune your permissions for least-privilege
access, Lambda provides some additional conditions you can include in your policies.
For more information, see [Fine-tuning the Resources and Conditions sections of policies](./lambda-api-permissions-ref.html).

For more information about IAM, see the *[IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)*.

[Document Conventions](/general/latest/gr/docconventions.html)

Tutorial

Execution role (permissions for functions to access other resources)
