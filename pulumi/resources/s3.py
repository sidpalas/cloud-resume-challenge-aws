import pulumi
import pulumi_aws as aws


BUCKET_NAME = "resume.devopsdeployed.com"

POLICY = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::BUCKET_NAME/*"]
    }
  ]
}
"""

# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket(
    "bucket",
    bucket=BUCKET_NAME,
    policy=POLICY.replace("BUCKET_NAME", BUCKET_NAME),
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html",
        error_document="error.html",
    ),
)
