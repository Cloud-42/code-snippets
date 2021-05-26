# If you are using this in AWS you'll need a layer with requests installed:
# https://github.com/keithrozario/Klayers/blob/master/deployments/python3.8/arns/eu-west-2.csv
# or to add requests to your Python package zip:
# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

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
