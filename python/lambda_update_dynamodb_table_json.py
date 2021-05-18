import requests
import os
import boto3

def lambda_handler(event, context):
  print('Loading function..........')

  region = os.environ['region']
  table_name = os.environ['table_name']

  try:
    datadict = (event)
    print(datadict)
    database = boto3.resource('dynamodb', region_name=region)
    table = database.Table(table_name)
    response = table.put_item(Item = datadict)
    return response['ResponseMetadata']['HTTPStatusCode'] 
  except Exception as e:
    print(str(e))
