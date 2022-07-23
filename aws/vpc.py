import logging
import boto3
from botocore.exceptions import ClientError
import json

AWS_REGION = 'us-east-2'

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

vpc_resource = boto3.resource("ec2", region_name=AWS_REGION)


def create_custom_vpc(ip_cidr):
    """
    Creates a custom VPC with the specified configuration.
    """
    try:
        response = vpc_resource.create_vpc(CidrBlock=ip_cidr,
                                           InstanceTenancy='default',
                                           TagSpecifications=[{
                                               'ResourceType':
                                               'vpc',
                                               'Tags': [{
                                                   'Key':
                                                   'Name',
                                                   'Value':
                                                   'hands-on-cloud-custom-vpc'
                                               }]
                                           }])

    except ClientError:
        logger.exception('Could not create a custom vpc.')
        raise
    else:
        return response


if __name__ == '__main__':
    # Constants
    IP_CIDR = '192.168.0.0/16'
    logger.info(f'Creating a custom VPC...')
    custom_vpc = create_custom_vpc(IP_CIDR)
    logger.info(f'Custom VPC is created with VPC ID: {custom_vpc.id}')