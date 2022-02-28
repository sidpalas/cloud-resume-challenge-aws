from glob import glob
import mimetypes
import os

import pulumi
import pulumi_aws as aws
import pulumi_command as command

from resources.s3 import bucket
from resources.cloudfront import distribution

# For each file in the directory, create an S3 object stored in `bucket`
files = {}
for file_path in glob(f"../client/*"):
    file_name = os.path.basename(file_path)
    files[file_name] = aws.s3.BucketObject(
        file_name,
        bucket=bucket.id,
        source=pulumi.asset.FileAsset(file_path),
        content_type=mimetypes.guess_type(file_path)[0] or None,
    )


def generate_invalidate_command(distribution_id, path):
    return f"aws cloudfront create-invalidation --distribution-id {distribution_id} --paths /{path}"


# Invalidate cache upon update of s3 files
# https://github.com/pulumi/pulumi-aws/issues/916
cache_invalidation_file = "index.html"
indexFile = files[cache_invalidation_file]
invalidationCommand = command.local.Command(
    "invalidate_index",
    create=distribution.id.apply(
        lambda id: generate_invalidate_command(id, cache_invalidation_file)
    ),
    environment={"ETAG": indexFile.etag},
    opts=pulumi.ResourceOptions(replace_on_changes=["environment"]),
)
