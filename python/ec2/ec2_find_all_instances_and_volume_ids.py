#!/usr/bin/env python3
import boto3

regions=['us-east-2','us-east-1','ap-south-1','eu-west-2','eu-west-1']

def main():
  full_instance_dict = instance_ids_with_volumes()
  for key,value in full_instance_dict.items():
    print('Found instance ' + key + ' in region ' + value[0] + ' with attached volumes ' + str(value[1]))

def instance_ids_with_volumes():
  instance_ids_with_volumes_dict = {}
  instances = instance_ids()
  for key,value in instances.items():
    ec2resource = boto3.resource('ec2', region_name=value,)
    instance = ec2resource.Instance(key)
    vols = instance.volumes.all()
    volume_id_list=[]
    for item in instance.volumes.all():
      volume_id_list.append(item.id)
    instance_ids_with_volumes_dict.setdefault(key, []).append(value)
    instance_ids_with_volumes_dict.setdefault(key, []).append(volume_id_list)
  return dict(instance_ids_with_volumes_dict)

def instance_ids():
    instance_ids_dict = {}
    for region in regions:
      ec2client = boto3.client('ec2',region_name=region)
      response  = ec2client.describe_instances()
      for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
          instance_ids_dict[instance['InstanceId']] = region
    return dict(instance_ids_dict)

if __name__=="__main__":
  main()
