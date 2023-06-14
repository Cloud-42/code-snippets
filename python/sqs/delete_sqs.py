#!/usr/bin/env python3

import logging
import boto3
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)

class ManageSqsQueue: 

  def __init__(self, filename: str="./arns.txt") -> None:
    self.filename: str = filename
    self.client = boto3.client('sqs')
    self.queue_names: list = self.get_queue_names(self.filename)

  def get_queue_names(self, filename: str) -> list:
    queue_names: list = []
    with open(filename) as f:     
      for arn in f.readlines():
         arn = arn.rstrip().strip('"')
         queue_names.append(arn.split(":")[-1])

    return queue_names     
     
  def remove_queues(self, queue_names: list) -> None:
    for queue in queue_names:
      
      logger.info(f"deleting https://sqs.eu-west-1.amazonaws.com/279340141865/{queue}")

      try:
          response = self.client.delete_queue(
            QueueUrl=f"https://sqs.eu-west-1.amazonaws.com/279340141865/{queue}"
            )

      except ClientError as error:
        logger.exception(f"Couldn't delete queue {queue}")


if __name__ == "__main__": 
  c = ManageSqsQueue() 
  c.remove_queues(c.queue_names)
