# Serverless URL Shortener

🔗 AWS Lambda + API Gateway + DynamoDB

## Architecture

```
POST /shorten → Lambda → DynamoDB → Returns short URL
GET /{shortId} → Lambda → DynamoDB → Redirects to original URL
```

## AWS Services Used

| Service | Purpose |
|---------|---------|
| DynamoDB | Store URLs |
| Lambda | Python functions |
| API Gateway | REST API |

---

## Setup Guide

### Step 1: Create DynamoDB Table

1. Go to **DynamoDB** → Create table
2. Settings:
   - Table name: `url-shortener`
   - Partition key: `short_id` (String)
3. Click **Create table**

---

### Step 2: Create Lambda Functions

#### Function 1: create_url

1. Go to **Lambda** → Create function
2. Settings:
   - Name: `create_url`
   - Runtime: Python 3.11
3. Paste code from `lambda/create_url.py`
4. Add DynamoDB permission to role

#### Function 2: redirect_url

1. Create another function
2. Settings:
   - Name: `redirect_url`
   - Runtime: Python 3.11
3. Paste code from `lambda/redirect_url.py`
4. Add DynamoDB permission to role

---

### Step 3: Create API Gateway

1. Go to **API Gateway** → Create API → REST API
2. Create resources and methods:

```
/shorten
  └── POST → create_url Lambda

/{short_id}
  └── GET → redirect_url Lambda
```

3. Deploy API → Create stage: `prod`

---

## Test

### Create Short URL

```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/prod/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

### Use Short URL

Open in browser:
```
https://your-api-id.execute-api.region.amazonaws.com/prod/{short_id}
```

---

## Lambda IAM Policy

Add this policy to Lambda role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/url-shortener"
    }
  ]
}
```
