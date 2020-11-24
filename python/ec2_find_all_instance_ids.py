#!/usr/bin/env python
import boto3

regions=['us-east-2','us-east-1','ap-south-1','eu-west-2','eu-west-1']

instance_ids_dict = {}

def main():
  instances = instance_ids()
  for key,value in instances.items():
    ec2resource = boto3.resource('ec2', region_name=value,)
    instance = ec2resource.Instance(key)
    vols = instance.volumes.all()
    volume_id_list=[]
    for item in instance.volumes.all():
      volume_id_list.append(item.id)
      print('Found instance', key, 'in region', value, 'which has these volumes attached', volume_id_list)

def instance_ids():
    for region in regions:
      ec2client = boto3.client('ec2',region_name=region)
      response  = ec2client.describe_instances()
      for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
          instance_ids_dict[instance['InstanceId']] = region
    return dict(instance_ids_dict)

if __name__=="__main__":
  main()


