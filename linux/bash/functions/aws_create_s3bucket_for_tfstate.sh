#!/bin/bash

bucket_name=$1
aws_region=$2

create_tfstate_s3 () {

which aws

if [ $? -ne 0 ]; then
   printf "\n\nThe AWS CLI is not installed...exiting\n\n\n"
   exit
else
   aws s3api create-bucket --bucket $bucket_name --region $aws_region --create-bucket-configuration LocationConstraint=$aws_region
   aws s3api put-bucket-versioning --bucket $bucket_name --versioning-configuration Status=Enabled
   aws s3api put-public-access-block --bucket $bucket_name --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
fi
}

create_tfstate_s3

# ---------------------------------
#
# execution example: ./s3create.sh bucketname us-east-2
#
# ---------------------------------
