#!/usr/bin/env python
import boto3
import sys
import logging
import pprint

def s3_delete_all(**kwargs):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(**kwargs)
    try: 
      response = bucket.object_versions.all().delete()
      pprint.pprint(response[0]['Deleted'])
    except Exception as e:
     print(str(e))

 
name = input("Enter the bucket name: ")

def main():
   s3_delete_all(
     name=name
   )


if __name__=="__main__":
   main()

# Enter the name using format "BUCKET_NAME"
# Has to be a string in ""
