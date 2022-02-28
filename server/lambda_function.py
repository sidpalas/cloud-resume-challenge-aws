import json
import os

import boto3


def get_env() -> str:
    return os.environ.get("ENV")


def upsert_view_count(dynamodb_table, environment) -> int:
    res = dynamodb_table.update_item(
        Key={"environment": environment},
        UpdateExpression="SET view_count = if_not_exists(view_count, :start) + :inc",
        ExpressionAttributeValues={
            ":inc": 1,
            ":start": 0,
        },
        ReturnValues="UPDATED_NEW",
    )
    return int(res.get("Attributes").get("view_count"))


def lambda_handler(event, context) -> dict:
    environment = get_env()

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("cloud-resume-views")

    view_count = upsert_view_count(table, environment)
    return {
        "statusCode": 200,
        "body": json.dumps({"environment": environment, "view_count": view_count}),
    }


if __name__ == "__main__":
    os.environ["ENV"] = "staging"
    res = lambda_handler(None, None)
    print(res)
