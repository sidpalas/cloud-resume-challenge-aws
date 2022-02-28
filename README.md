1. Skip 😅
2. Create index.html
```html
<!DOCTYPE html>
<html>
<head>
</head>
<body>
  <h1>Sid Palas</h1>
  <p>This is my cloud resume</p>
  <p>View count: <span id="viewCount">0</span></p>
</body>
</html>
```
3. Create main.css
```html
<link rel="stylesheet" href="main.css">
```
4. Create S3 bucket
5. Create Cloud front distribution
6. Create Route53 record
   1. A record (aliased to cloudfront)
   2. AAAA record (aliased to cloudfront)
   3. Add NS to google domains
   4. Add alternate domains to cloudfront 
      1. Create certificate in ACM
      2. Create CNAME record to validate certificate
      3. Add certificate to cloudfront
7. Create main.js
```html
<script src="main.js" defer></script>
```
```js
function updateViewCount() {
  viewCount = document.getElementById('viewCount');
  viewCount.innerHTML = Math.random();
}

window.onload = updateViewCount();
```
8. Create DynamoDB table
   - Partition key: environment (dev/staging/production)
   - Additional info: view_count
10. Create python lambda
    1. Write the code
```python
import json

def lambda_handler(event, context):
    # Within a single dynamo db transaction:
    #   1. get todays date in dynamo db table 
    #   2. if exists, increment view_count and update
    #   3. if doesn't exists, create record with view_count 1
    #
    # Get total view count and return in api response
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```
    3. Update the IAM role to enable DynamoDB access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:UpdateItem",
            "Resource": "arn:aws:dynamodb:us-east-1:917774925227:table/cloud-resume-views"
        }
    ]
}
```
9.  Create api gateway
   1.  Add custom domain (with API mapping using api/v1)
   2.  Update cloudfront distribution to route /api/v1 traffic to api gateway (path based routing)
11.  Write tests
    1.  mock dynamodb
12. Infrastructure as code
    1.  Create IAM user
    2.  Install pulumi in venv
    3.  `pulumi new aws-python`
    4.  Resources:
        1.  ✅ Set up AWS and Cloudflare authentication
        2.  ✅ S3 bucket
        3.  ✅ S3 files
        4.  ✅ DynamoDB
        5.  ✅ Lambda
        6.  ✅ API Gateway
        7.  ✅ Cloudfront
        8.  ✅ Cloudflare

13. Push to github
14. CI/CD back-end
15. CI/CD front-end
16. Blog post / video

BONUS: 
- modularize pulumi code
- add dev/staging stacks