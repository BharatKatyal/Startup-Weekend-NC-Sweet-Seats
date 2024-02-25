import json
import boto3
import os

# Assuming the environment variable 'USERS_TABLE' contains the name of the DynamoDB table
users_table = os.environ['USERS_TABLE']

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Determine the operation based on the event (e.g., HTTP method if invoked via API Gateway)
    http_method = event.get('httpMethod')

    if http_method == 'POST':
        # Extract user data from the event body
        user_data = json.loads(event.get('body'))
        user_id = user_data['id']  # Assuming the body contains an 'id' field
        # Remove 'id' from user_data to handle the rest as attributes
        del user_data['id']
        
        # Call the function to add or update the user
        response = post_user(user_id, user_data)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    elif http_method == 'GET':
        # Extract user ID from the event query string parameters
        user_id = event['queryStringParameters']['id']
        
        # Call the function to get the user by ID
        response = get_user(user_id)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Unsupported HTTP method'})
        }

def post_user(user_id, user_data):
    # Convert user_data to DynamoDB format
    dynamo_item = {'id': {'S': user_id}}
    for k, v in user_data.items():
        dynamo_item[k] = {'S': str(v)}
    
    # Add or update the user in the DynamoDB table
    response = dynamodb.put_item(
        TableName=users_table,
        Item=dynamo_item
    )
    return {'message': 'User added or updated successfully'}

def get_user(user_id):
    # Get the user by ID from the DynamoDB table
    response = dynamodb.get_item(
        TableName=users_table,
        Key={'id': {'S': user_id}}
    )
    # Check if the user exists
    if 'Item' in response:
        # Convert the DynamoDB item to a more friendly format
        user = {k: v['S'] for k, v in response['Item'].items()}
        return {'user': user}
    else:
        return {'message': 'User not found'}

