import aiobotocore
import botocore
import logging

logger = logging.getLogger(__name__)

'''
For Asynchronous Events
'''
class S3_SERVICE(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    async def upload_fileobj(self, fileobject, bucket, key):
        session = aiobotocore.get_session()
        async with session.create_client('s3', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            file_upload_response = await client.put_object(ACL="public-read",ContentType = 'image/jpeg' ,Bucket=bucket, Key=key, Body=fileobject)

            if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logger.info(f"File uploaded path : https://{bucket}.s3.{self.region}.amazonaws.com/{key}")
                return True
        return False

class S3_SERVICE_VIDEO(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    async def upload_fileobj(self, fileobject, bucket, key):
        session = aiobotocore.get_session()
        async with session.create_client('s3', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            file_upload_response = await client.put_object(ACL="public-read",ContentType='video/mp4',Bucket=bucket, Key=key)

            if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logger.info(f"File uploaded path : https://{bucket}.s3.{self.region}.amazonaws.com/{key}")
                return True
        return False

class S3_SERVICE_DOC(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    async def upload_fileobj(self, fileobject, bucket, key):
        session = aiobotocore.get_session()
        async with session.create_client('s3', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            file_upload_response = await client.put_object(ACL="public-read",ContentType = 'application/pdf' ,Bucket=bucket, Key=key)

            if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logger.info(f"File uploaded path : https://{bucket}.s3.{self.region}.amazonaws.com/{key}")
                return True
        return False