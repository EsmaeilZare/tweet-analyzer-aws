from config.credentials import ACCESS_KEY, SECRET_KEY, SESSION_TOKEN, BUCKET_NAME
import boto3
from botocore.exceptions import ClientError

queue_url = 'https://queue.amazonaws.com/649303115657/clcprojectsqs'
queue_name = 'clcprojectsqs'

class SQS():
    @staticmethod
    def _client():
        try:
            sqs_client = boto3.client(
                'sqs',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
                region_name='us-east-1'
            )
            return sqs_client
        except ClientError as e:
            print(f"error{e} occur create sqs_client client")

    def __init__(self):
        self.s3_client = self._client()

    def create_queue(self):
        response = self.s3_client.create_queue(
            QueueName=queue_name,
            # Attributes={'FifoQueue': 'true'},
            tags={
                'Name': 'clcprojectsqs'
            }
        )
        print(f"response of create queue {response}")

    def send_message(self, message):
        response = self.s3_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
            DelaySeconds= 2,
        )
        print(f"response of send message {response}")
    
    def receive_message(self, ):
        response = self.s3_client.receive_message(
            QueueUrl=queue_url
        )
        message = response['Messages'][0]
        print(f"response of send message {message}")
        return message

sqs_obj = SQS()
sqs_obj.create_queue()   
