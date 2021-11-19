#!/usr/bin/env python3
import boto3

regions=['us-east-2','us-east-1','ap-south-1','eu-west-2','eu-west-1']

mylist =[]

def main():
  for region in regions:
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
      for instance in reservation["Instances"]:
        mylist.append(instance["ImageId"])
  print ("The list is: " + str(mylist))

if __name__=="__main__":
  main()
