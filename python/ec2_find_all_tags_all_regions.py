#!/usr/bin/env python
import boto3

regions=['us-east-2','us-east-1','ap-south-1','eu-west-1','eu-west-2']

def main():
  for region in regions:
    ec2client = boto3.client('ec2',region_name=region)
    response  = ec2client.describe_instances()
    for reservation in response["Reservations"]:
      for instance in reservation["Instances"]:
        print(instance["Tags"])


if __name__=="__main__":
  main()
