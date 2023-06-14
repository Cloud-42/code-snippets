#!/usr/bin/env python3

import logging
import boto3
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)


class Deletes3:

    def __init__(self, filename: str = "./bucketNames.txt") -> None:
        self.filename: str = filename
        self.bucket_names: list = self.get_bucket_names(self.filename)

    def get_bucket_names(self, filename: str) -> list:
        bucket_names: list = []
        with open(filename) as f:
            for name in f.readlines():
                name = name.rstrip().strip('"')
                bucket_names.append(name.split(":")[-1])

        return bucket_names

    def remove_buckets(self, bucket_names: list) -> None:
        for bucket_name in bucket_names:

            logger.info(f"purging versions from {bucket_name}")

            try:
                s3 = boto3.resource('s3')
                bucket = s3.Bucket(bucket_name)

                logger.info(f"purging versions from {bucket_name}")
                bucket.object_versions.all().delete()

                logger.info(f"deleting bucket: s3://{bucket_name}")
                response = bucket.delete()

            except ClientError as error:
                logger.exception(f"Couldn't delete bucket {bucket}")


if __name__ == "__main__":
    c = Deletes3()
    c.remove_buckets(c.bucket_names)
