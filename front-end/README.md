# 🚀 awshero.shop - URL Shortener Frontend

Beautiful, serverless URL shortener frontend with HTTPS, powered by AWS CloudFront + S3.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CloudFront                               │
│                    (CDN + SSL/HTTPS)                             │
├─────────────────────────────────────────────────────────────────┤
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│   ┌──────────┐        ┌──────────┐        ┌──────────┐         │
│   │   S3     │        │   API    │        │  Lambda  │         │
│   │ (HTML)   │        │ Gateway  │───────▶│ + Dynamo │         │
│   └──────────┘        └──────────┘        └──────────┘         │
│   /index.html          /shorten            /{shortCode}         │
│   /error.html          /api/*              (redirects)          │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **Existing Lambda + API Gateway + DynamoDB** setup (from your YouTube video)
2. **awshero.shop** domain in Route 53
3. **AWS CLI** configured with appropriate permissions
4. **Terraform** installed (v1.0+)

## Quick Start

### Step 1: Get Required Information

You'll need these values from your AWS console:

| Value | Where to Find |
|-------|---------------|
| API Gateway Endpoint | API Gateway → Your API → Stages → prod → Invoke URL |
| Route 53 Zone ID | Route 53 → Hosted zones → awshero.shop → Hosted zone ID |

### Step 2: Update Configuration

1. **Update the frontend HTML with your API endpoint:**
   
   Edit `index.html`, find this line near the bottom:
   ```javascript
   const API_BASE_URL = 'https://YOUR_API_GATEWAY_ID.execute-api.YOUR_REGION.amazonaws.com/prod';
   ```
   
   Replace with your actual API Gateway URL:
   ```javascript
   const API_BASE_URL = 'https://abc123xyz.execute-api.ap-south-1.amazonaws.com/prod';
   ```


### Step 2: Deploy Infrastructure


⏱️ **Note:** SSL certificate validation and CloudFront distribution can sometimes take 10-30 minutes.

### Step 4: Upload Frontend Files

### Step 5: Test

1. Open https://awshero.shop
2. Enter a long URL and click "Shorten"
3. Copy the short URL and test the redirect

## API Endpoints

Your Lambda should handle these endpoints:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/shorten` | Create short URL |
| GET | `/{shortCode}` | Redirect to original URL |
| GET | `/api/stats` | Get statistics (optional) |

### Expected Request/Response

**Create Short URL:**
```bash
curl -X POST https://awshero.shop/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/url"}'
```

**Response:**
```json
{
  "short_url": "https://awshero.shop/abc123",
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url"
}
```


**Total: ~$0.50-2/month** for moderate traffic

## Troubleshooting

### SSL Certificate Pending
- DNS validation records are created automatically
- Can take up to 30 minutes to validate
- Check Route 53 for CNAME records

### CloudFront 403 Error
- S3 bucket policy may not be applied yet
- Wait 5-10 minutes after Terraform apply
- Check CloudFront OAC configuration

### API Returns CORS Error
- Ensure Lambda returns proper CORS headers
- Check CloudFront forwards necessary headers

### Short URL Not Redirecting
- Verify Lambda handles the path correctly
- Check DynamoDB for the short code
- Test API Gateway directly first

## Files Structure

```
url-shortener-UI/
├── index.html          # Main landing page
├── error.html          # 404 error page
├── deploy.sh           # Deployment script
├── README.md           # This file

```

## YouTube Video Content Ideas

This setup makes great content for:
1. "Add HTTPS to Your Serverless App with CloudFront"
2. "Build a Complete URL Shortener on AWS"
3. "S3 + CloudFront + ACM: The Complete Guide"
4. "Terraform for AWS Beginners"

---

Built with ❤️ for the DevOps community
