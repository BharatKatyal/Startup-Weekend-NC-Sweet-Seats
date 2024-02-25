import json
import boto3
import os

# import requests

users_table = os.environ['USERS_TABLE']

def lambda_handler(event, context):
  

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
