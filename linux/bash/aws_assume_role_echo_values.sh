#!/bin/bash -
set -o nounset                              # Treat unset variables as an error

role=$(aws sts assume-role --role-arn="arn:aws:iam::866644848801:role/IAM-IAC-eks-admin-role" --role-session-name IAM-IAC-eks-admin-role --duration-seconds 3600)

accessKey=$(jq '.Credentials.AccessKeyId' <<< $role)
secretKey=$(jq '.Credentials.SecretAccessKey' <<< $role)
sessionToken=$(jq '.Credentials.SessionToken' <<< $role)

echo export AWS_ACCESS_KEY_ID=$accessKey | tr -d '"'
echo export AWS_SECRET_ACCESS_KEY=$secretKey | tr -d '"'
echo export AWS_SESSION_TOKEN=$sessionToken | tr -d '"'
