#!/bin/bash
# define array

PARAMETERS=(\
 "MAIL_USERNAME"\
 "MAILP_PASSWORD"\
 "CURL_TIMEOUT"\
 "DATABASE_URL"\
)

# Constants
aws_region=eu-west-1

# get length of an array
tLen=${#PARAMETERS[@]}

# use for loop read all nameservers
for (( i=0; i<${tLen}; i++ ));
do

  export ${PARAMETERS[$i]}=$(aws ssm get-parameters --names ${PARAMETERS[$i]} --with-decryption --region=${aws_region} --output text --query "Parameters[0]"."Value");

done

# --------------------------------------------------
# Useful for Debugging, remove comments and echo env
# --------------------------------------------------
#env
