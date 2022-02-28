import os

import boto3
from moto import mock_dynamodb2

from main import get_env
from main import upsert_view_count


def create_views_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table_name = "cloud-resume-views"

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "environment", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "environment", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    # Wait until the table exists.
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)

    return table


class TestApi:
    @classmethod
    def setup_class(cls):
        """
        Create database resource and mock table
        """
        cls.mock_dynamodb2 = mock_dynamodb2()
        cls.mock_dynamodb2.start()
        cls.dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        cls.table = create_views_table(cls.dynamodb)

    @classmethod
    def teardown_class(cls):
        """
        Delete database resource and mock table
        """
        cls.table.delete()
        cls.dynamodb = None
        cls.mock_dynamodb2.stop()

    def test_upsert_view_count(self):
        print("hello")
        view_count = upsert_view_count(TestApi.table, "test")
        assert view_count == 1
        view_count2 = upsert_view_count(TestApi.table, "test")
        assert view_count2 == 2
        view_count3 = upsert_view_count(TestApi.table, "test2")
        assert view_count3 == 1

    def test_env(self):
        test_env = "test"
        os.environ["ENV"] = test_env
        env = get_env()
        assert env == test_env
