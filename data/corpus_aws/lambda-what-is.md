# What is AWS Lambda?

###### Tip

Join Serverless experts for free hands-on workshops to learn how to build Serverless
applications with best practices. [Click here](https://aws-experience.com/amer/smb/events/series/Get-Hands-On-With-Serverless?trk=188abe3e-9f94-4e84-aefb-398d944ad567%26sc_channel%3Del) to sign up.

AWS Lambda is a compute service that runs code without the need to manage servers. Your code runs, scaling up and down automatically, with pay-per-use pricing.
To get started, see [Create your first function](./getting-started.html).

You can use Lambda for:

* **File processing**: Process files automatically when uploaded to Amazon Simple Storage Service. See [file processing examples](./example-apps.html#examples-apps-file) for details.
* **Long-running workflows:** Use [durable Lambda functions](./durable-functions.html) to build stateful, multi-step workflows that can run for up to one year. Perfect for order processing, approval workflows, human-in-the-loop processes, and complex data pipelines that need to remember their progress.
* **Database operations and integration examples**: Respond to database changes and automate data workflows. See [database examples](./example-apps.html#examples-apps-database) for details.
* **Scheduled and periodic tasks**: Run automated operations on a regular schedule using EventBridge. See [scheduled task examples](./example-apps.html#examples-apps-scheduled) for details.
* **Stream processing**: Process real-time data streams for analytics and monitoring. See [Kinesis Data Streams](./with-kinesis.html) for details.
* **Web applications**: Build scalable web apps that automatically adjust to demand.
* **Mobile backends**: Create secure API backends for mobile and web applications.
* **IoT backends**: Handle web, mobile, IoT, and third-party API requests. See [IoT](./services-iot.html) for details.

For pricing information, see [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/).

## How Lambda works

When using Lambda, you are responsible only for your code. Lambda runs your code on a high-availability compute infrastructure and manages all the computing resources,
including server and operating system maintenance, capacity provisioning, automatic scaling, and logging.

Because Lambda is a serverless,
event-driven compute service, it uses a different programming paradigm than traditional web applications. The following model illustrates how Lambda works:

1. You write and organize your code in [Lambda functions](./concepts-basics.html#gettingstarted-concepts-function), which are the basic building blocks you use to create a Lambda application.
2. You control security and access through [Lambda permissions](./lambda-permissions.html), using [execution roles](./lambda-intro-execution-role.html) to manage what AWS services your functions can interact with and what resource policies can interact with your code.
3. Event sources and AWS services [trigger](./concepts-event-driven-architectures.html) your Lambda functions, passing event data in JSON format, which your functions process (this includes event source mappings).
4. [Lambda runs your code](./concepts-how-lambda-runs-code.html) with language-specific runtimes (like Node.js and Python) in execution environments that package your runtime, layers, and extensions.

###### Tip

To learn how to build **serverless solutions**, check out the [Serverless Developer Guide](https://docs.aws.amazon.com/serverless/latest/devguide/).

## Key features

**Configure, control, and deploy secure applications:**

* [Environment variables](./configuration-envvars.html) modify application behavior without new code deployments.
* [Versions](./configuration-versions.html) safely test new features while maintaining stable production environments.
* [Lambda layers](./chapter-layers.html) optimize code reuse and maintenance by sharing common components across multiple functions.
* [Code signing](./configuration-codesigning.html) enforce security compliance by ensuring only approved code reaches production systems.

**Scale and perform reliably:**

* [Concurrency and scaling controls](./lambda-concurrency.html) precisely manage application responsiveness and resource utilization during traffic spikes.
* [Lambda SnapStart](./snapstart.html) significantly reduce cold start times. Lambda SnapStart can provide as low as sub-second startup performance, typically with no changes to your function code.
* [Response streaming](./configuration-response-streaming.html) optimize function performance by delivering large payloads incrementally for real-time processing.
* [Container images](./images-create.html) package functions with complex dependencies using container workflows.

**Connect and integrate seamlessly:**

* [VPC networks](./configuration-vpc.html) secure sensitive resources and internal services.
* [File systems](./configuration-filesystem.html) integration that shares persistent data and manage stateful operations across function invocations.
* [Function URLs](./urls-configuration.html) create public-facing APIs and endpoints without additional services.
* [Lambda extensions](./lambda-extensions.html) augment functions with monitoring, security, and operational tools.

## Related information

* For information on how Lambda works, see [How Lambda works](./concepts-basics.html).
* To start using Lambda, see [Create your first Lambda function](./getting-started.html).
* For a list of example applications, see [Getting started with example applications and patterns](./example-apps.html).

[Document Conventions](/general/latest/gr/docconventions.html)

How it works
