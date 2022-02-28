import pulumi_aws as aws

dynamodb_table = aws.dynamodb.Table(
    "dynamodb_table",
    name="cloud-resume-views",
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="environment",
            type="S",
        )
    ],
    billing_mode="PAY_PER_REQUEST",
    hash_key="environment",
)
