import json

import pulumi
import pulumi_aws as aws

from dynamodb import dynamodb_table


def generate_inline_dynamo_policy(dynamodb_table_arn):
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "dynamodb:UpdateItem",
                    "Resource": f"{dynamodb_table_arn}",
                }
            ],
        }
    )


iam_for_lambda = aws.iam.Role(
    "iamForLambda",
    assume_role_policy="""{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
""",
    inline_policies=[
        aws.iam.RoleInlinePolicyArgs(
            name="updateViewCountItem",
            policy=dynamodb_table.arn.apply(
                lambda arn: generate_inline_dynamo_policy(arn)
            ),
        )
    ],
)
lambda_function = aws.lambda_.Function(
    "api_lambda",
    name="resume_api_lambda",
    code=pulumi.FileArchive("../server/"),
    role=iam_for_lambda.arn,
    handler="lambda_function.lambda_handler",
    runtime="python3.9",
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "ENV": "dev",
        },
    ),
)
