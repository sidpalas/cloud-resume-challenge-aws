import pulumi
import pulumi_aws as aws

from resources.api_gateway import api
from resources.acm import cert
from resources.s3 import bucket


s3_origin_id = "cloudResumeS3Origin"

apigw_origin_id = "cloudResumeAPIGW"

distribution = aws.cloudfront.Distribution(
    "cloud_resume_distribution",
    origins=[
        aws.cloudfront.DistributionOriginArgs(
            domain_name=bucket.bucket_regional_domain_name,
            origin_id=s3_origin_id,
            # s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
            #     origin_access_identity=None,
            # ),
        ),
        aws.cloudfront.DistributionOriginArgs(
            domain_name=api.api_endpoint.apply(
                lambda api_endpoint: api_endpoint.split("//")[1]
            ),
            origin_id=apigw_origin_id,
            custom_origin_config=aws.cloudfront.DistributionOriginCustomOriginConfigArgs(
                http_port=80,
                https_port=443,
                origin_protocol_policy="https-only",
                origin_ssl_protocols=["TLSv1.2"],
            ),
        ),
    ],
    enabled=True,
    is_ipv6_enabled=True,
    default_root_object="index.html",
    aliases=[
        "resume.devopsdirective.com",
    ],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=[
            "GET",
            "HEAD",
        ],
        cached_methods=[
            "GET",
            "HEAD",
        ],
        target_origin_id=s3_origin_id,
        forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=False,
            cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                forward="none",
            ),
        ),
        viewer_protocol_policy="redirect-to-https",
        min_ttl=0,
        default_ttl=3600,
        max_ttl=86400,
    ),
    ordered_cache_behaviors=[
        aws.cloudfront.DistributionOrderedCacheBehaviorArgs(
            path_pattern="/api/v1/*",
            allowed_methods=[
                "GET",
                "HEAD",
            ],
            cached_methods=[
                "GET",
                "HEAD",
            ],
            target_origin_id=apigw_origin_id,
            forwarded_values=aws.cloudfront.DistributionOrderedCacheBehaviorForwardedValuesArgs(
                query_string=False,
                headers=["Origin"],
                cookies=aws.cloudfront.DistributionOrderedCacheBehaviorForwardedValuesCookiesArgs(
                    forward="none",
                ),
            ),
            min_ttl=0,
            default_ttl=0,
            max_ttl=0,
            compress=True,
            viewer_protocol_policy="redirect-to-https",
        ),
        aws.cloudfront.DistributionOrderedCacheBehaviorArgs(
            path_pattern="/content/*",
            allowed_methods=[
                "GET",
                "HEAD",
                "OPTIONS",
            ],
            cached_methods=[
                "GET",
                "HEAD",
            ],
            target_origin_id=s3_origin_id,
            forwarded_values=aws.cloudfront.DistributionOrderedCacheBehaviorForwardedValuesArgs(
                query_string=False,
                cookies=aws.cloudfront.DistributionOrderedCacheBehaviorForwardedValuesCookiesArgs(
                    forward="none",
                ),
            ),
            min_ttl=0,
            default_ttl=3600,
            max_ttl=86400,
            compress=True,
            viewer_protocol_policy="redirect-to-https",
        ),
    ],
    price_class="PriceClass_200",
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none",
        ),
    ),
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        acm_certificate_arn=cert.arn, ssl_support_method="sni-only"
    ),
)
