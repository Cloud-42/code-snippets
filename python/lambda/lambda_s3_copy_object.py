import boto3
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
  print('Loading function..........')

  bucket = os.environ['bucket']
  prefix = os.environ['prefix']
  copy_location = os.environ['copy_location']
  
  s3 = boto3.resource('s3')

  try:
    latest_file = get_latest_file_name(bucket_name=bucket,prefix=prefix)
    source = "s3://" + bucket + "/" + latest_file
    
    logger.info("Found latest file to be " "s3://" + bucket + "/" + latest_file)
        
    copy_source = {
      'Bucket': bucket,
      'Key': latest_file
    }
    
    response = s3.meta.client.copy(copy_source, bucket, copy_location)
    
    logger.info("Copied " + "s3://" + bucket + "/" + latest_file + "  to " + "s3://" + bucket + "/" + copy_location)
    
    return response
  except Exception as e:
    print(str(e))


def get_latest_file_name(bucket_name,prefix):
  """
  Return the latest file name in an S3 bucket folder.
  :param bucket: Name of the S3 bucket.
  :param prefix: Only fetch keys that start with this prefix (folder  name).
  """
  s3_client = boto3.client('s3')
  objs = s3_client.list_objects_v2(Bucket=bucket_name)['Contents']
  shortlisted_files = dict()
  for obj in objs:
      key = obj['Key']
      timestamp = obj['LastModified']
      # if key starts with folder name retrieve that key
      if key.startswith(prefix):
      # Adding a new key value pair
        shortlisted_files.update( {key : timestamp} )
  latest_filename = max(shortlisted_files, key=shortlisted_files.get)
  return latest_filename
