import boto3
from botocore.exceptions import ClientError
from config.credentials import ACCESS_KEY, SECRET_KEY, SESSION_TOKEN


class EC2Instance(object):
    def __init__(self, ec2_client):
        self.ec2_client = ec2_client

    def grep_vpc_subnet_id(self):
        response = self.ec2_client.describe_vpcs()
        vpc_id = ""
        for vpc in response["Vpcs"]:
            if vpc["IsDefault"]:
                vpc_id = vpc["VpcId"]
                break
        response = self.ec2_client.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])
        subnet_ids = [subnet["SubnetId"] for subnet in response["Subnets"]]
        return vpc_id, subnet_ids

    def create_security_group(self):
        sg_name = "clc_project_security_group"
        vpc_id, subnet_ids = self.grep_vpc_subnet_id()
        try:
            # creating our security group
            response = self.ec2_client.create_security_group(
                GroupName=sg_name,
                Description="Default security group of our project",
                VpcId=vpc_id,
            )
            sg_id = response["GroupId"]
            sg_config = self.ec2_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 22,
                        "ToPort": 22,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                    }
                ]
            )
            return sg_id
        except Exception as e:
            if str(e).__contains__("already exists"):
                response = self.ec2_client.describe_security_groups(GroupNames=[sg_name])
                return response["SecurityGroups"][0]["GroupId"]

    def create_ec2_instance(self):
        try:
            vpc_id, subnet_ids = self.grep_vpc_subnet_id()
            sg_id = self.create_security_group()
            print("Creating an EC2 instance")
            self.ec2_client.run_instances(
                ImageId="ami-0cff7528ff583bf9a",
                MinCount=1,
                MaxCount=1,
                InstanceType="t2.micro",
                KeyName="clc_project",
                SecurityGroupIds=[sg_id],
                SubnetId=subnet_ids[0]
            )
        except Exception as e:
            print(e)


def initialize():
    try:
        ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            region_name='us-east-1'
        )
        ec2_obj = EC2Instance(ec2_client)
        ec2_obj.grep_vpc_subnet_id()
        ec2_obj.create_security_group()
        ec2_obj.create_ec2_instance()
    except ClientError as e:
        print(e)


initialize()
