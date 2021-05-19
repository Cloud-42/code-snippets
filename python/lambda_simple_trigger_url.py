import requests
import os

def lambda_handler(event, context):
  print('Loading function..........')

  payload = os.environ['payload']
  url = os.environ['url']

  try:
    response = requests.post(url, data = payload)
    print(response.status_code)
    return response.status_code
  except Exception as e:
    print(str(e))
