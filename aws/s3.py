from config.credentials import ACCESS_KEY, SECRET_KEY, SESSION_TOKEN, BUCKET_NAME
import boto3
from botocore.exceptions import ClientError
from os import path
import sys

# directory = path.Path(__file__).abspath()
# sys.path.append(directory.parent.parent)


class S3Instance(object):
    @staticmethod
    def _client():
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
                region_name='us-east-1'
            )
            return s3_client
        except ClientError as e:
            print(f"error{e} occur create s3 client")

    def __init__(self):
        self.s3_client = self._client()

    def create_bucket(self):
        response = self.s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(response)

    def upload_file(self, file, file_name):
        self.s3_client.put_object(
            Body=file,
            Bucket=BUCKET_NAME,
            Key=file_name
        )
        return True

    def exist(self, file_key):
        result = self.s3_client.list_objects_v2(
            Bucket=BUCKET_NAME, Prefix=file_key)

        if 'Contents' in result:
            print("Key exists in the bucket.")
            return True
        else:
            print("Key doesn't exist in the bucket.")
            return False

    def read(self, file_key):
        try:
            s3_object = self.s3_client.get_object(
                Bucket=BUCKET_NAME, Key=file_key)
            body = s3_object['Body']
            return body.read()
        except Exception as e:
            print(f"error{e} occur find this {file_key} in s3")


s3_obj = S3Instance()
s3_obj.create_bucket()
