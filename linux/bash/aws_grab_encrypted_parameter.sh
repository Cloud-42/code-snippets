aws ssm get-parameters --names "SUPERSECRET" --with-decryption --region=eu-west-1 --output text --query "Parameters[0]"."Value"
