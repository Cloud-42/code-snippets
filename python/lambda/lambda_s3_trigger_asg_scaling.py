import json
import boto3
import os

print('Loading function..........')

def lambda_handler(event, context):
    for record in event['Records']:
      bucket = record['s3']['bucket']['name']
      file = record['s3']['object']['key']
      sourceIP = record['requestParameters']['sourceIPAddress']
	  
    print( "received " + file + " from " + sourceIP + " in s3://" + bucket)

    asg_name = os.environ['asg_name']	
    region = os.environ['region']
    try:
      client = boto3.client('autoscaling', region_name=region)
      response = client.set_desired_capacity(AutoScalingGroupName=asg_name,DesiredCapacity=1,HonorCooldown=True)
      if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("SUCCESS: - asg " + asg_name + " desired capacity set to 1")
      else:
       print("ERROR: Unable to set desired capacity set to 1" )
    except Exception as e:
      print(str(e))
