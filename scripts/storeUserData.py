import json
import time
import boto3

def lambda_handler(event, context):
    client = boto3.client('dynamodb')

    user = {
        "user": { "S": event['user'] },
        "email": { "S": event['email'] },
        "password": { "S": event['pass'] },
        "dob-day": { "N": str(event['dob-day']) },
        "dob-month": { "N": str(event['dob-month']) },
        "dob-year": { "N": str(event['dob-year']) },
        "gender": { "N": str(event['gender']) },
        "useragent": { "S": event['useragent'] },
        "country": { "S": event['country'] },
        "coordinates": { "S": event['coordinates'] },
        "status": { "N": str(event['status']) },
        "created": { "S": time.ctime(time.time()) },
        "updated": { "S": time.ctime(time.time()) }        
    }

    response = client.put_item ( 
        TableName = 'spoticry-users',
        Item = user
    )

    return 0