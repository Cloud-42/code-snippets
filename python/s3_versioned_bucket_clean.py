#!/usr/bin/env python
import boto3


def s3_delete_all(**kwargs):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(**kwargs)
    bucket.object_versions.all().delete()

name = input("Enter the bucket name: ")

def main():
   s3_delete_all(
     name=name
   )


if __name__=="__main__":
   main()
