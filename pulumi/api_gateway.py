import time

import pulumi
import pulumi_aws as aws

from lambda_fn import lambda_function
from acm import cert

# Define an endpoint that invokes a lambda to handle requests
api = aws.apigatewayv2.Api(
    "api",
    name="cloud_resume_api",
    protocol_type="HTTP",
    route_key="GET /api/v1/visits",
    target=lambda_function.invoke_arn,
)

# Give API Gateway permissions to invoke the Lambda
lambda_permission = aws.lambda_.Permission(
    "lambdaPermission",
    action="lambda:InvokeFunction",
    principal="apigateway.amazonaws.com",
    function=lambda_function,
)


# FIXME: Fails first apply because certificate hasn't been issued
# Workaround is to run pulumi up again after cert is validated
aws.apigatewayv2.DomainName(
    "api_custom_domain",
    domain_name="resume.devopsdeployed.com",
    domain_name_configuration=aws.apigatewayv2.DomainNameDomainNameConfigurationArgs(
        certificate_arn=cert.arn,
        endpoint_type="REGIONAL",
        security_policy="TLS_1_2",
    ),
)
