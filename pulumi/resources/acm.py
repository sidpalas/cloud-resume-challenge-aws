import pulumi_aws as aws

# Create ACM cert
cert = aws.acm.Certificate(
    "cert-devops-directive",
    domain_name="*.devopsdirective.com",
    validation_method="DNS",
)
