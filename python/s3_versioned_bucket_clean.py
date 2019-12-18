#!/usr/bin/env python
import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('S3BUCKETNAME')
bucket.object_versions.all().delete()
