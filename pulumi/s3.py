import pulumi
import pulumi_aws as aws


BUCKET_NAME = "resume.devopsdeployed.com"
# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket(
    "bucket",
    bucket=BUCKET_NAME,
    policy=(lambda path: open(path).read().replace("BUCKET_NAME", BUCKET_NAME))(
        "policy.json"
    ),
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html",
        error_document="error.html",
    ),
)
