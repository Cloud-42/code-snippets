#!/bin/bash -
for i in $(aws ec2 describe-instances --output text --query 'Reservations[*].Instances[*].[InstanceId]');

do

 aws ec2 describe-tags --filters "Name=resource-id,Values=${i}" --output table

done
