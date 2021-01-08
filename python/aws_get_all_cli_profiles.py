#!/usr/bin/env python3
import botocore
import boto3
from boto3 import Session

session = botocore.session.get_session()
for profile in boto3.session.Session().available_profiles:
    print(profile)

