import os
import boto3
import logging

from botocore.client import BaseClient
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = "AKIA2O3WJVIG42BHMUPF"#os.getenv('POSTGRES_HOST')
AWS_SECRET_KEY ="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"# os.getenv('AWS_SECRET_KEY')
AWS_S3_BUCKET_NAME ="cinedarbaar"# os.getenv('AWS_S3_BUCKET_NAME')


def s3() -> BaseClient:
    client = boto3.client(service_name='s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          endpoint_url='https://cinedarbaar.s3.ap-south-1.amazonaws.com/')  # Use LocalStack Endpoint

    return client
from random import randint
gid = randint(100000,1000000)

def upload_file_to_bucket(s3_client, file_obj, bucket, folder, object_name=None):
    """Upload a file to an S3 bucket

    :param s3_client: S3 Client
    :param file_obj: File to upload
    :param bucket: Bucket to upload to
    :param folder: Folder to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        
        rec = ("course_video"+str(gid))
        object_name = rec

    # Upload the file
    try:
        # with open("files", "rb") as f:
        upload = s3_client.upload_fileobj(file_obj, bucket, f"{folder}/{object_name}")
        print(upload)
        #return upload
    except ClientError as e:
        logging.error(e)
        return False
    return True

import logging
from uuid import uuid4

logger = logging.getLogger(__name__)


def generate_png_string():
    logger.info("Generating random string .png")
    return uuid4().hex[:6].upper().replace('0', 'X').replace('O', 'Y') + ".png"