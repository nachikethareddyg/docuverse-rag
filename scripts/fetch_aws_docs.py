from __future__ import annotations

import re
import warnings
from dataclasses import dataclass
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown


OUTPUT_DIR = Path("data/corpus_aws")


@dataclass(frozen=True)
class AwsDocPage:
    service: str
    slug: str
    url: str


PAGES = [
    AwsDocPage("s3", "s3-what-is", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"),
    AwsDocPage("s3", "s3-getting-started", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html"),
    AwsDocPage("s3", "s3-buckets-overview", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html"),
    AwsDocPage("s3", "s3-objects-overview", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingObjects.html"),
    AwsDocPage("s3", "s3-upload-objects", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html"),
    AwsDocPage("s3", "s3-versioning", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html"),
    AwsDocPage("s3", "s3-security-best-practices", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html"),
    AwsDocPage("iam", "iam-what-is", "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"),
    AwsDocPage("iam", "iam-identities", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id.html"),
    AwsDocPage("iam", "iam-users-overview", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html"),
    AwsDocPage("iam", "iam-roles-overview", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html"),
    AwsDocPage("iam", "iam-policies-overview", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html"),
    AwsDocPage("iam", "iam-security-credentials", "https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html"),
    AwsDocPage("iam", "iam-best-practices", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"),
    AwsDocPage("lambda", "lambda-what-is", "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"),
    AwsDocPage("lambda", "lambda-getting-started", "https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html"),
    AwsDocPage("lambda", "lambda-functions", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-functions.html"),
    AwsDocPage("lambda", "lambda-runtimes", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html"),
    AwsDocPage("lambda", "lambda-invocation", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html"),
    AwsDocPage("lambda", "lambda-permissions", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-permissions.html"),
    AwsDocPage("lambda", "lambda-env-vars", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html"),
    AwsDocPage("ec2", "ec2-what-is", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html"),
    AwsDocPage("ec2", "ec2-getting-started", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html"),
    AwsDocPage("ec2", "ec2-instances", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Instances.html"),
    AwsDocPage("ec2", "ec2-amis", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html"),
    AwsDocPage("ec2", "ec2-key-pairs", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html"),
    AwsDocPage("ec2", "ec2-security-groups", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html"),
    AwsDocPage("ec2", "ec2-ebs-volumes", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html"),
]


def find_main_content(soup: BeautifulSoup) -> BeautifulSoup:
    for selector in ["main", "article", "#main-content", "div.awsdocs-content"]:
        content = soup.select_one(selector)
        if content is not None:
            return content

    body = soup.body
    if body is None:
        raise ValueError("Could not find HTML body")

    return body


def clean_content(content: BeautifulSoup) -> BeautifulSoup:
    for element in content.select(
        "script, style, nav, footer, header, noscript, .breadcrumbs, .feedback, .awsdocs-page-footer"
    ):
        element.decompose()

    return content


def normalize_markdown(markdown: str) -> str:
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    return markdown.strip() + "\n"


def fetch_page(page: AwsDocPage, session: requests.Session) -> str:
    try:
        response = session.get(page.url, timeout=30)
    except requests.exceptions.SSLError:
        warnings.warn(
            f"TLS verification failed for {page.url}; retrying without verification.",
            stacklevel=2,
        )
        response = session.get(page.url, timeout=30, verify=False)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content = clean_content(find_main_content(soup))
    markdown = html_to_markdown(str(content), heading_style="ATX")

    return normalize_markdown(markdown)


def write_page(page: AwsDocPage, markdown: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{page.slug}.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def main() -> None:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "docuverse-rag documentation fetcher",
        }
    )

    written_paths = []
    for page in PAGES:
        markdown = fetch_page(page, session)
        path = write_page(page, markdown)
        written_paths.append(path)
        print(f"Wrote {path}")

    print(f"Fetched {len(written_paths)} AWS documentation pages")


if __name__ == "__main__":
    main()
