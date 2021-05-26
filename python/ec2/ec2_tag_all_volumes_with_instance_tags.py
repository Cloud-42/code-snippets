#!/usr/bin/env python3
import boto3

regions=['us-east-2','us-east-1','ap-south-1','eu-west-2','eu-west-1']

def tag_all_volumes():
  full_instance_dict = instance_ids_with_volumes()
  for key,value in full_instance_dict.items():
    session = boto3.Session(region_name=value[0])
    ec2 = session.resource('ec2', region_name=value[0] )
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-id', 'Values': [key]}])
    for instance in instances:
      for tag in instance.tags:
        volumes = value[1]
        for volumeid in volumes:
          print('Found instance ' + key + ' in region ' + value[0] + ' updating all volume ' + volumeid + ' to include instance tag of ' + str(tag)) 
          ec2.create_tags(Resources=[volumeid],Tags=[tag]);

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

def main():
  tag_all_volumes()

if __name__=="__main__":
  main()
