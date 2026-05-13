# Amazon EC2 instances

An Amazon EC2 instance is a virtual server in the AWS cloud environment. You have full
control over your instance, from the time that you first start it (referred to as
launching an instance) until you delete it (referred to as terminating an instance).
You can choose from a variety of operating systems when you launch your instance.
You can connect to your instance and customize it to meet your needs. For example,
you can configure the operating system, install operating system updates, and install
applications on your instance.

Amazon EC2 provides a wide range of instance types. You can choose an instance type that
provides the compute resources, memory, storage, and network performance that you
need to run your applications.

With Amazon EC2, you pay only for what you use. Billing for your instance
starts when you launch your instance and it transitions to the running state.
Billing stops when you stop your instance and resumes when you start your instance.
When you terminate your instance, billing stops when it transitions to the shutting
down state.

Amazon EC2 provides features that you can use to optimize the performance and the cost
of your instances. For example, you can use Amazon EC2 Fleet or Amazon EC2 Auto Scaling to scale your
capacity up or down as your instance utilization changes. You can reduce the costs
for your instances using Spot Instances or Savings Plans.

A *managed instance* is managed by a service provider, such
as Amazon EKS Auto Mode. You canât directly modify the settings of a managed instance. Managed
instances are identified by a **true** value in the
**Managed** field. For more information, see [Amazon EC2 managed instances](./amazon-ec2-managed-instances.html).

###### Features and tasks

* [Amazon EC2 instance types](./instance-types.html)
* [Amazon EC2 managed instances](./amazon-ec2-managed-instances.html)
* [Use nested virtualization to run hypervisors in Amazon EC2 instances](./amazon-ec2-nested-virtualization.html)
* [Amazon EC2 billing and purchasing options](./instance-purchasing-options.html)
* [Store instance launch parameters in Amazon EC2 launch templates](./ec2-launch-templates.html)
* [Launch an Amazon EC2 instance](./LaunchingAndUsingInstances.html)
* [Connect to your EC2 instance](./connect.html)
* [Amazon EC2 instance state changes](./ec2-instance-lifecycle.html)
* [Automatic instance recovery](./ec2-instance-recover.html)
* [Use instance metadata to manage your EC2 instance](./ec2-instance-metadata.html)
* [Detect whether a host is an EC2 instance](./identify_ec2_instances.html)
* [Instance identity documents for Amazon EC2 instances](./instance-identity-documents.html)
* [STIG compliance for your EC2 instance](./ec2-configure-stig.html)
* [Precision clock and time synchronization on your EC2 instance](./set-time.html)
* [EC2 Capacity Manager](./capacity-manager.html)
* [Manage device drivers for your EC2 instance](./manage-device-drivers.html)
* [Configure your Amazon EC2 Windows instance](./ec2-windows-instances.html)
* [Upgrade an EC2 Windows instance to a newer version of Windows Server](./serverupgrade.html)
* [Tutorial: Connect an Amazon EC2 instance to an Amazon RDS database](./tutorial-connect-ec2-instance-to-rds-database.html)

[Document Conventions](/general/latest/gr/docconventions.html)

AMI quotas

Instance types
