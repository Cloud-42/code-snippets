import boto3
import json
import logging
import os
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context): 
    restart_services()

def restart_services():
    client = boto3.client('ecs')
    cluster = os.environ['ecs_cluster']
    services = os.environ['ecs_services']
    my_session = boto3.session.Session()
    my_region = my_session.region_name
    
    list = []
    
    services_response = client.list_services(cluster=cluster, maxResults=100)
    
    for x in services_response['serviceArns']:
        value_stripped = x.replace('arn:aws:ecs:' + my_region + ':' + get_account_id() + ':service/' + cluster + '/', '')
        logger.info("Found ecs service {0}".format(value_stripped))
        list.append(value_stripped)
    
    try: 
      logger.info("Found ecs services {0}".format(list))  
      for svc in list:
        logger.info("Starting restart of service {0}".format(svc))
        response = client.update_service(cluster=cluster, service=svc, forceNewDeployment=True)
    except Exception as error:
        print('Caught this error: ' + repr(error))

def get_account_id():
    client = boto3.client("sts")
    return client.get_caller_identity()["Account"]
