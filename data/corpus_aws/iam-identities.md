# IAM Identities

An IAM identity can be associated with one or more policies, which determine what actions
an identity is authorized to perform, on which AWS resources, and under what conditions. IAM
identities include IAM users, IAM groups, and IAM roles. An IAM entity is a type
of identity that represents a human user or programmatic workload that can be authenticated and
then authorized to perform actions in AWS accounts. IAM entities include IAM users and
IAM roles. For definitions for commonly used terms, see [Terms](./introduction_identity-management.html#intro-structure-terms).

You can federate existing identities from an external identity provider. These identities
will assume IAM roles to access AWS resources. For more information, see [Identity providers and federation into AWS](./id_roles_providers.html).

You can also use AWS IAM Identity Center to create and manage identities and access to AWS resources.
IAM Identity Center permission sets automatically create the IAM roles needed to provide access to
resources. For more information, see [What is IAM Identity Center?](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)

The AWS account root user is an AWS account principal that is created when your AWS account is
established. The root user has access to all AWS services and resources in the account. For more
information, see [IAM root user](#id_root).

###### Note

* Follow the [Security best practices in
  IAM](https://docs.aws.amazon.com//IAM/latest/UserGuide/best-practices-use-cases.html) when working with IAM identities.
* Follow the [root user best practices for your
  AWS account](./root-user-best-practices.html) when working with the root user.
* If you're having trouble signing in, see [Sign in to the
  AWS Management Console](https://docs.aws.amazon.com/signin/latest/userguide/console-sign-in-tutorials.html).

## IAM root user

When you first create an AWS account, you begin with one sign-in identity that has
complete access to all AWS services and resources in the account. This identity is called
the AWS account *root user*. For more information, see [AWS account root
user.](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html)

## IAM users

An *IAM user* is an identity within your AWS account that has
specific permissions for a single person or application. For more information, see [IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html).

## IAM user groups

An *IAM user group* is an identity that specifies a collection of
IAM users. For more information, see [User groups](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html).

## IAM roles

An *IAM role* is an identity within your AWS account that has
specific permissions. It's similar to an IAM user, but isn't associated with a specific
person. For more information, see [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

[Document Conventions](/general/latest/gr/docconventions.html)

Create SAML IdP and federated role with CloudFormation

AWS account root user
