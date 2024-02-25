import json
import boto3
import os
import logging
import uuid

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERINFO_TABLE_NAME'])
ses = boto3.client('ses', region_name=os.environ['SES_REGION'])
source_email = os.environ['SES_SOURCE_EMAIL']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    id = str(uuid.uuid4())
    first_name = body.get('first_name', '')
    email = body.get('email', '')
    phone = body.get('phone', '')

    # Check for first name and at least one contact method
    if not first_name or (not email and not phone):
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps('First name and at least one contact method (email or phone) are required!')
        }

    try:
        # Store data in DynamoDB
        item = {'id': id, 'first_name': first_name}
        if email:
            item['email'] = email
        if phone:
            item['phone'] = phone
        table.put_item(Item=item)

        # Send an email if the email address is provided
        if email:
            response = ses.send_email(
                Source=source_email,
                Destination={
                    'ToAddresses': [email]  # Use the user's provided email as the destination
                },
                Message={
                    'Subject': {
                        'Data': 'Welcome to our service'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Hello {first_name},\nWelcome to our service. We have received your contact information.'
                        }
                    }
                }
            )

        success_message = 'Data submitted successfully.'
        if email:
            success_message += ' An email has been sent to your provided email address.'
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(success_message)
        }
    except Exception as e:
        # Log the error to CloudWatch Logs
        logger.error(f'Error: {str(e)}')
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(f'Error: {str(e)}')
        }
