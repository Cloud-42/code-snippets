#!/usr/bin/env python3
import boto3

regions=['us-east-2','us-east-1','ap-south-1','eu-west-2','eu-west-1']

instance_ids_list = []

def main():
  instances = instance_ids()
  for instance in instances:
    print(instance)

def instance_ids():
    for region in regions:
      ec2client = boto3.client('ec2',region_name=region)
      response  = ec2client.describe_instances()
      for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
          instance_ids_list.append(instance['InstanceId'])
    return instance_ids_list

if __name__=="__main__":
  main()



