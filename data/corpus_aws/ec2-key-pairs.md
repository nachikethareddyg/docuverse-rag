# Amazon EC2 key pairs and Amazon EC2 instances

A key pair, consisting of a public key and a private key, is a set of security credentials
that you use to prove your identity when connecting to an Amazon EC2 instance. For Linux instances,
the private key allows you to securely SSH into your instance. For Windows instances, the
private key is required to decrypt the administrator password, which you then use to connect to
your instance.

Amazon EC2 stores the public key on your instance, and you store the private key, as shown in the
following diagram. It's important that you store your private key in a secure place because
anyone who possesses your private key can connect to your instances that use the key
pair.

![A key pair consists of a private key for your computer and a public key for your instance.](/images/AWSEC2/latest/UserGuide/images/ec2-key-pair.png)

When you launch an instance, you can [specify a key pair](./ec2-instance-launch-parameters.html#liw-key-pair),
so that you can connect to your instance using a method that requires a key pair. Depending on
how you manage your security, you can specify the same key pair for all your instances or you
can specify different key pairs.

For Linux instances, when your instance boots for the first time, the public key that you
specified at launch is placed on your Linux instance in an entry within
`~/.ssh/authorized_keys`. When you connect to your Linux instance using
SSH, to log in you must specify the private key that corresponds to the public key.

For more information about connecting to your EC2 instance, see [Connect to your EC2 instance](./connect.html).

###### Important

Because Amazon EC2 doesn't keep a copy of your private key, there is no way to recover a
private key if you lose it. However, there can still be a way to connect to instances for
which you've lost the private key. For more information, see [I've lost my private key. How can I connect to my instance?](./TroubleshootingInstancesConnecting.html#replacing-lost-key-pair)

As an alternative to key pairs, you can use [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) to connect to
your instance with an interactive one-click browser-based shell or the AWS Command Line Interface (AWS CLI).

###### Contents

* [Create a key pair for your Amazon EC2 instance](./create-key-pairs.html)
* [Describe your key pairs](./describe-keys.html)
* [Delete your key pair](./delete-key-pair.html)
* [Add or replace a public key on your Linux instance](./replacing-key-pair.html)
* [Verify the fingerprint of your key pair](./verify-keys.html)

[Document Conventions](/general/latest/gr/docconventions.html)

Best practices for Windows instances

Create a key pair
