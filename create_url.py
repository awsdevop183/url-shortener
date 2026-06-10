import json
import boto3
import string
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortner')
import hashlib

def generate_short_id(long_url: str, length: int = 8) -> str:
    hash_object = hashlib.sha256(long_url.encode('utf-8'))
    hash_bytes = hash_object.digest()
    short_id = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
    return short_id[:length].rstrip('=')


def lambda_handler(event, context):
    try:
        # Handle body (could be string or dict)
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        long_url = body.get('url')
        
        if not long_url:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing url parameter'})
            }
        
        short_id = generate_short_id(long_url)
        
        table.put_item(
            Item={
                'short_id': short_id,
                'long_url': long_url
            }
        )
        
        # Build short URL
        host = event.get('headers', {}).get('Host', '')
        stage = event.get('requestContext', {}).get('stage', 'prod')
        short_url = f"https://{host}/{stage}/{short_id}"
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'short_url': short_url,
                'short_id': short_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
