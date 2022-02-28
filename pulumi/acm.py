import pulumi_aws as aws

# Create ACM cert
cert = aws.acm.Certificate(
    "cert", domain_name="*.devopsdeployed.com", validation_method="DNS"
)
