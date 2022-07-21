import boto3
from botocore.exceptions import ClientError
import path
import sys

directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from config.credentials import ACCESS_KEY, SECRET_KEY, SESSION_TOKEN, BUCKET_NAME


class S3Instance(object):
    def __init__(self, s3_client):
        self.s3_client = s3_client

    def create_bucket(self):
        response = self.s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(response)

    def upload_file(self, file_path):
        self.s3_client.upload_file(
            Filename=file_path,
            Bucket=BUCKET_NAME,
            Key=file_path.split("/")[-1]
        )
        return file_path.split("/")[-1]


def initialize():
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            region_name='us-east-1'
        )
        s3_obj = S3Instance(s3_client)
        s3_obj.create_bucket()

    except ClientError as e:
        print(e)


initialize()
