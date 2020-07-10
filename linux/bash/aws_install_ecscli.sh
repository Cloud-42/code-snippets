#!/usr/bin/env bash

# Download binary
/usr/bin/curl -o /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
# Checksum
/bin/echo "$(curl -s https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest.md5) /usr/local/bin/ecs-cli" | md5sum -c -

# Use exit code
if [ $? -eq 0 ]; then
        /usr/bin/printf  "\n\n **ECS-CLI checksum PASSED, ECS-CLI will be installed** \n\n"
        sudo chmod +x /usr/local/bin/ecs-cli
else
        /usr/bin/printf  "\n\n  **ECS-CLI checksum FAILED, ECS-CLI will be removed**  \n\n"
        sudo rm -f /usr/local/bin/ecs-cli
fi
