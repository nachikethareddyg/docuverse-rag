# Amazon Machine Images in Amazon EC2

An Amazon Machine Image (AMI) is an image that provides the software that is required to set up
and boot an Amazon EC2 instance. Each AMI also contains a block device mapping that specifies
the block devices to attach to the instances that you launch. You must specify an AMI
when you launch an instance. The AMI must be compatible with the instance type that you
chose for your instance. You can use an AMI provided by AWS, a public AMI, an AMI
that someone else shared with you, or an AMI that you purchased from the AWS Marketplace.

An AMI is specific to the following:

* Region
* Operating system
* Processor architecture
* Root volume type
* Virtualization type

You can launch multiple instances from a single AMI when you require multiple instances with the
same configuration. You can use different AMIs to launch instances when you require
instances with different configurations, as shown in the following diagram.

![Launch multiple instances from an AMI.](/images/AWSEC2/latest/UserGuide/images/launch-from-ami.png)

You can create an AMI from your Amazon EC2 instances and then use it to launch instances
with the same configuration. You can copy an AMI to another AWS Region, and then use it
to launch instances in that Region. You can also share an AMI that you created with other
accounts so that they can launch instances with the same configuration. You can sell your
AMI using the AWS Marketplace.

###### Contents

* [AMI characteristics](./ComponentsAMIs.html)
* [Find an AMI](./finding-an-ami.html)
* [Paid AMIs in the AWS Marketplace](./paid-amis.html)
* [AMI lifecycle](./ami-lifecycle.html)
* [Boot modes](./ami-boot.html)
* [AMI encryption](./AMIEncryption.html)
* [Shared AMIs](./sharing-amis.html)
* [Monitor AMI events](./monitor-ami-events.html)
* [Understand AMI billing](./ami-billing-info.html)
* [AMI quotas](./ami-quotas.html)

[Document Conventions](/general/latest/gr/docconventions.html)

Best practices

AMI characteristics
