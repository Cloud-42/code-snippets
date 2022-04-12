#!/bin/bash

set -ex

for i in `aws ssm describe-parameters --region eu-west-2  | grep Name | grep %PREFIX-% | awk '{print $2}' | cut -d\" -f2` ; do
  export `echo ${i} | cut -d\- -f4`="`aws ssm get-parameter --name ${i} --region eu-west-2 --with-decryption | jq -r '.Parameter.Value'`";
done

#env
