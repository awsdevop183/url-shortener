import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')


def lambda_handler(event, context):
    try:
        short_id = event['pathParameters']['short_id']
        
        response = table.get_item(
            Key={'short_id': short_id}
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'URL not found'})
            }
        
        long_url = response['Item']['long_url']
        
        return {
            'statusCode': 301,
            'headers': {
                'Location': long_url
            }
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
