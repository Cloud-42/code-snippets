#!/bin/bash - 
set -o nounset                              # Treat unset variables as an error
 
deployment_monitor() {
  aws ecs wait services-stable --services=SERVICE_NAME --cluster=CLUSTER_NAME
  status=$?

  if [ $status == 0 ]; then 
    echo "SUCCESS exit code is ${status}"
    exit 0
  else
    echo "FAILURE exit code is ${status}"
    exit "${status}"
  fi
}

deployment_monitor 
