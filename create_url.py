import json
import boto3
import string
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')


def generate_short_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


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
        
        short_id = generate_short_id()
        
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