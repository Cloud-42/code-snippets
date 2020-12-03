import json
import datetime

def lambda_handler(event, context):
    current_time = datetime.date.today()
    body = {
        "message": "Hello, the date today is " + str(current_time)
    }
    
    response = {
        "StatusCode": 200,
        "body": json.dumps(body)
    }

    return response
