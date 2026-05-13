# Uploading objects

When you upload a file to Amazon S3, it is stored as an S3 *object*. Objects consist of the file data and metadata that describes the object.
You can have an unlimited number of objects in a bucket. Before you can upload files to an Amazon S3
bucket, you need write permissions for the bucket. For more information about access
permissions, see [Identity and Access Management for Amazon S3](./security-iam.html).

You can upload any file typeâimages, backups, data, movies, and so onâinto an
S3 bucket. The maximum size of a file that you can upload by using the Amazon S3 console is 160 GB.
To upload a file larger than 160 GB, use the AWS Command Line Interface (AWS CLI), AWS SDKs, or Amazon S3 REST
API.

If you upload an object with a key name that already exists in a versioning-enabled bucket,
Amazon S3 creates another version of the object instead of replacing the existing object. For more
information about enabling versioning, see [Enabling versioning on buckets](./manage-versioning-examples.html).

Depending on the size of the data that you're uploading, Amazon S3 offers the following options:

* Upload an object in a single operation by using the AWS SDKs,
  REST API, or AWS CLI â With a single `PUT` operation, you can
  upload a single object up to 5 GB in size.
* Upload a single object by using the Amazon S3 console â With the Amazon S3 console, you can upload a single object up
  to 160 GB in size.
* Upload an object in parts by using the AWS SDKs, REST API, or
  AWS CLI â Using the multipart upload API
  operation, you can upload a single large object, up to 50 TB in size.

  The multipart upload API operation is designed to improve the upload experience for
  larger objects. You can upload an object in parts. These object parts can be uploaded
  independently, in any order, and in parallel. You can use a multipart upload for objects
  from 5 MB to 50 TB in size. For more information, see [Uploading and copying objects using multipart upload in Amazon S3](./mpuoverview.html).

To upload files greater than 5 TB, use the S3 Transfer Manager in the Java v1/v2, Python, or
AWS CLI SDKs. For the best performance, use the latest AWS Common Runtime (CRT) with these SDKs,
which has been optimized for better resource utilization.

When uploading large objects from memory stream, CRT buffers each part up to 5 GB in memory,
limiting overall throughput by allocated memory. You can adjust the CRT memory limit using
configuration options such as `maxNativeMemoryLimitInBytes` for Java SDK. For uploads
from disk, CRT automatically switches to direct disk streaming instead of intermediate part
buffering, improving memory usage. This behavior is automatically enabled for large objects, but
can also be enabled for smaller files via request parameters such as `should_stream`
for AWS CLI and `CRT_MEMORY_BUFFER_DISABLED` for Java SDK.

When you upload an object, the object is automatically encrypted using server-side
encryption with Amazon S3 managed keys (SSE-S3) by default. When you download it, the object is
decrypted. For more information, see [Setting default server-side encryption behavior for Amazon S3 buckets](./bucket-encryption.html) and [Protecting data with encryption](./UsingEncryption.html).

When you're uploading an object, if you want to use a different type of default encryption,
you can also specify server-side encryption with AWS Key Management Service (AWS KMS) keys (SSE-KMS) in your S3
`PUT` requests or set the default encryption configuration in the destination
bucket to use SSE-KMS to encrypt your data. For more information about SSE-KMS, see [Specifying server-side encryption with AWS KMS (SSE-KMS)](./specifying-kms-encryption.html). If you want
to use a KMS key that is owned by a different account, you must have permission to use the
key. For more information about cross-account permissions for KMS keys, see [Creating KMS keys that other accounts can use](https://docs.aws.amazon.com//kms/latest/developerguide/key-policy-modifying-external-accounts.html#cross-account-console) in the
*AWS Key Management Service Developer Guide*.

If you encounter an Access Denied (403 Forbidden) error in Amazon S3, see [Troubleshoot access denied (403 Forbidden) errors in Amazon S3](./troubleshoot-403-errors.html) to learn more
about its common causes.

## Upload an object

This procedure explains how to upload objects and folders to an Amazon S3 bucket by using the
console.

When you upload an object, the object key name is the file name and any optional
prefixes. In the Amazon S3 console, you can create folders to organize your objects. In Amazon S3,
folders are represented as prefixes that appear in the object key name. If you upload an
individual object to a folder in the Amazon S3 console, the folder name is included in the object
key name.

For example, if you upload an object named `sample1.jpg` to a folder named
`backup`, the key name is `backup/sample1.jpg`. However, the object
is displayed in the console as `sample1.jpg` in the `backup` folder.
For more information about key names, see [Working with object metadata](./UsingMetadata.html).

###### Note

If you rename an object or change any of the properties in the Amazon S3 console, for example
**Storage Class**, **Encryption**, or **Metadata**, a new object is created
to replace the old one. If S3 Versioning is enabled, a new version of the object is created,
and the existing object becomes an older version. The role that changes the property also
becomes the owner of the new object (or object version).

When you upload a folder, Amazon S3 uploads all of the files and subfolders from the specified
folder to your bucket. It then assigns an object key name that is a combination of the uploaded
file name and the folder name. For example, if you upload a folder named
`/images` that contains two files, `sample1.jpg` and
`sample2.jpg`, Amazon S3 uploads the files and then assigns the corresponding
key names, `images/sample1.jpg` and `images/sample2.jpg`.
The key names include the folder name as a prefix. The Amazon S3 console displays only the part of
the key name that follows the last `/`. For example, within an
`images` folder, the `images/sample1.jpg` and
`images/sample2.jpg` objects are displayed as `sample1.jpg` and a
`sample2.jpg`.

###### To upload folders and files to an S3 bucket

1. Sign in to the AWS Management Console and open the Amazon S3 console at
   <https://console.aws.amazon.com/s3/>.
2. In the left navigation pane, choose **Buckets**.
3. In the **Buckets** list, choose the name of the bucket that you want to
   upload your folders or files to.
4. Choose **Upload**.
5. In the **Upload** window, do one of the following:

   * Drag and drop files and folders to the **Upload** window.
   * Choose **Add file** or **Add folder**, choose the
     files or folders to upload, and choose **Open**.
6. To enable versioning, under **Destination**, choose **Enable
   Bucket Versioning**.
7. To upload the listed files and folders without configuring additional upload options, at
   the bottom of the page, choose **Upload**.

   Amazon S3 uploads your objects and folders. When the upload is finished, you see a success
   message on the **Upload: status** page.

###### To configure additional object properties

1. To change access control list permissions, choose **Permissions**.
2. Under **Access control list (ACL)**, edit the permissions.

   For information about object access permissions, see [Using the S3 console to set ACL permissions for an object](./managing-acls.html#set-object-permissions). You can grant
   read access to your objects to the public (everyone in the world) for all of the files that
   you're uploading. However, we recommend not changing the default setting for public read
   access. Granting public read access is applicable to a small subset of use cases, such as
   when buckets are used for websites. You can always change the object permissions after you
   upload the object.
3. To configure other additional properties, choose **Properties**.
4. Under **Storage class**, choose the storage class for the files that
   you're uploading.

   For more information about storage classes, see [Understanding and managing Amazon S3 storage classes](./storage-class-intro.html).
5. To update the encryption settings for your objects, under **Server-side encryption
   settings**, do the following.

   1. Choose **Specify an encryption key**.
   2. Under
      **Encryption settings**, choose **Use
      bucket settings for default encryption** or **Override
      bucket settings for default encryption**.
   3. If you chose **Override bucket settings for default encryption**,
      you must configure the following encryption settings.

      * To encrypt the uploaded files by using keys that are managed by Amazon S3, choose **Amazon S3
        managed key (SSE-S3)**.

        For more information, see [Using server-side encryption with Amazon S3 managed keys (SSE-S3)](./UsingServerSideEncryption.html).
      * To encrypt the uploaded files by using keys stored in AWS Key Management Service (AWS KMS), choose
        **AWS Key Management Service key (SSE-KMS)**. Then choose one of the following
        options for **AWS KMS key**:

        + To choose from a list of available KMS keys, choose **Choose from your
          AWS KMS keys**, and then choose your **KMS key** from
          the list of available keys.

          Both the AWS managed key (`aws/s3`) and your customer managed keys appear in this
          list. For more information about customer managed keys, see [Customer keys and AWS
          keys](https://docs.aws.amazon.com//kms/latest/developerguide/concepts.html#key-mgmt) in the *AWS Key Management Service Developer Guide*.
        + To enter the KMS key ARN, choose **Enter AWS KMS key ARN**,
          and then enter your KMS key ARN in the field that appears.
        + To create a new customer managed key in the AWS KMS console, choose **Create a
          KMS key**.

          For more information about creating an AWS KMS key, see [Creating
          keys](https://docs.aws.amazon.com//kms/latest/developerguide/create-keys.html) in the *AWS Key Management Service Developer Guide*.

        ###### Important

        You can use only KMS keys that are available in the same AWS Region as
        the bucket. The Amazon S3 console lists only the first 100 KMS keys in the same
        Region as the bucket. To use a KMS key that is not listed, you must enter
        your KMS key ARN. If you want to use a KMS key that is owned by a different
        account, you must first have permission to use the key and then you must enter the
        KMS key ARN.

        Amazon S3 supports only symmetric encryption KMS keys, and not asymmetric KMS keys. For
        more information, see [Identifying symmetric and
        asymmetric KMS keys](https://docs.aws.amazon.com//kms/latest/developerguide/find-symm-asymm.html) in the *AWS Key Management Service Developer Guide*.
6. To use additional checksums, choose **On**. Then for
   **Checksum function**, choose the function that you would like to use.
   Amazon S3 calculates and stores the checksum value after it receives the entire object. You can
   use the **Precalculated value** box to supply a precalculated value. If you
   do, Amazon S3 compares the value that you provided to the value that it calculates. If the two
   values do not match, Amazon S3 generates an error.

   Additional checksums enable you to specify the checksum algorithm that you would
   like to use to verify your data. For more information about additional checksums, see [Checking object integrity in Amazon S3](./checking-object-integrity.html).
7. To add tags to all of the objects that you are uploading, choose **Add
   tag**. Enter a tag name in the **Key** field. Enter a value for
   the tag.

   Object tagging gives you a way to categorize storage. Each tag is a key-value pair. Key
   and tag values are case sensitive. You can have up to 10 tags per object. A tag key can be
   up to 128 Unicode characters in length, and tag values can be up to 255 Unicode characters
   in length. For more information about object tags, see [Categorizing your objects using tags](./object-tagging.html).
8. To add metadata, choose **Add metadata**.

   1. Under **Type**, choose **System defined** or **User defined**.

      For system-defined metadata, you can select common HTTP headers, such as
      **Content-Type** and **Content-Disposition**. For a
      list of system-defined metadata and information about whether you can add the value, see
      [System-defined object metadata](./UsingMetadata.html#SysMetadata). Any metadata starting with
      the prefix `x-amz-meta-` is treated as user-defined metadata. User-defined
      metadata is stored with the object and is returned when you download the object. Both
      the keys and their values must conform to US-ASCII standards. User-defined metadata can
      be as large as 2 KB. For more information about system-defined and user-defined
      metadata, see [Working with object metadata](./UsingMetadata.html).
   2. For **Key**, choose a key.
   3. Type a value for the key.
9. To upload your objects, choose **Upload**.

   Amazon S3 uploads your object. When the upload completes, you can see a success message on the **Upload: status** page.
10. Choose **Exit**.

You can send a `PUT` request to upload an object of up to 5 GB in a single
operation. For more information, see the [`PutObject`](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-object.html#examples) example
in the *AWS CLI Command Reference*.

You can send REST requests to upload an object. You can send a `PUT`
request to upload data in a single operation. For more information, see [PUT Object](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html).

For examples of how to upload an object with the AWS SDKs, see [Code
Examples](https://docs.aws.amazon.com/AmazonS3/latest/API/s3_example_s3_PutObject_section.html) in the *Amazon Simple Storage Service API Reference*.

For general information about using different AWS SDKs, see [Developing with Amazon S3 using the AWS SDKs](https://docs.aws.amazon.com/AmazonS3/latest/API/sdk-general-information-section.html) in the *Amazon Simple Storage Service API Reference*.

## Prevent uploading objects with identical key names

You can check for the existence of an object in your bucket before creating it using a
conditional write on upload operations. This can prevent overwrites of existing data. Conditional writes
will validate there is no existing object with the same key name already in your
bucket while uploading.

You can use conditional writes for [PutObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html) or [CompleteMultipartUpload](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CompleteMultipartUpload.html) requests.

For more information about conditional requests see, [Add preconditions to S3 operations with conditional requests](./conditional-requests.html).

[Document Conventions](/general/latest/gr/docconventions.html)

Troubleshooting

Using multipart upload
