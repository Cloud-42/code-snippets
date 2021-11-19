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
  result = []
  for i in mylist:
    if i not in result:
        result.append(i)
  print ("The list after removing duplicates : " + str(result))

if __name__=="__main__":
  main()
