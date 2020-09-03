#!/usr/bin/env bash
#
# Requires https://github.com/venth/aws-adfs
# Useful for AWS SAML Logins with multiple roles available
#
getcreds () {
printf "\nPurging all credentials\n\n"
rm -f ~/.aws/credentials
rm -f ~/.aws/config
echo "Enter region to use:"
read region
aws-adfs login --profile=default --ssl-verification --adfs-host=SamlLoginAddress.co.uk/adfs/ls/idpinitiatedsignon.aspx  --session-duration 3600
aws configure set region $region --profile default
}

getcreds
