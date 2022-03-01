import pulumi_cloudflare as cloudflare

from resources.acm import cert
from resources.cloudfront import distribution

ZONE_ID = "10fcb4b0954ea348eb17e4da5190e091"


cert_cname = cloudflare.Record(
    "cert_cname",
    zone_id=ZONE_ID,
    name=cert.domain_validation_options[0]["resource_record_name"],
    value=cert.domain_validation_options.apply(
        # remove trailing . to avoid continuous change detection
        lambda domain_validation_options: f"{domain_validation_options[0]['resource_record_value'][:-1]}"
    ),
    type="CNAME",
    ttl=3600,
)

cloudfront_cname = cloudflare.Record(
    "cloudfront_cname",
    zone_id=ZONE_ID,
    name="resume",
    value=distribution.domain_name,
    type="CNAME",
    ttl=3600,
)
