import boto3
from botocore.exceptions import ClientError
import path
import sys
import base64

directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from config.credentials import ACCESS_KEY, SECRET_KEY, SESSION_TOKEN, SECURITY_GROUP_NAME, TEMPLATE_NAME, AUTO_SCALING_GROUP_NAME


with open("userdata.sh", "r") as fp:
    userdata_str = fp.read()
USERDATA_B64 = base64.b64encode(userdata_str)


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
        az = response["Subnets"][0]["AvailabilityZone"]
        return vpc_id, subnet_ids, az

    def create_security_group(self):
        vpc_id, subnet_ids, az = self.grep_vpc_subnet_id()
        try:
            # creating our security group
            response = self.ec2_client.create_security_group(
                GroupName=SECURITY_GROUP_NAME,
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
                    },
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 80,
                        "ToPort": 80,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                    }
                ]
            )
            return sg_id
        except Exception as e:
            if str(e).__contains__("already exists"):
                response = self.ec2_client.describe_security_groups(GroupNames=[SECURITY_GROUP_NAME])
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

    def creat_ec2_launch_template(self):
        print("Creating the Launch Template: Started")
        try:
            sg_id = self.create_security_group()
            response = self.ec2_client.create_launch_template(
                LaunchTemplateName=TEMPLATE_NAME,
                LaunchTemplateData={
                    "ImageId": "ami-0cff7528ff583bf9a",
                    "InstanceType": "t2.micro",
                    "KeyName": "clc_project",
                    "UserData": USERDATA_B64,
                    "SecurityGroupIds": [sg_id]
                }
            )
            template_id = response["LaunchTemplate"]["LaunchTemplateId"]
            print("Creating the Launch Template: Completed")
            print("Template ID: {}, Template Name: {}".format(template_id, TEMPLATE_NAME))
            return template_id

        except Exception as e:
            response = self.ec2_client.describe_launch_templates(
                LaunchTemaplateNames=[TEMPLATE_NAME]
            )
            template_id = response["LaunchTemplates"][0]["LaunchTemplateId"]
            return template_id

    def create_ec2_auto_scaling_group(self):
        print("Creating Auto Scaling Group using Launch Template")
        launch_template_id = self.creat_ec2_launch_template()
        vpc_id, subnet_ids, az = self.grep_vpc_subnet_id()
        auto_scaling_client = boto3.client(
            "autoscaling",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            region_name='us-east-1'
        )
        response = auto_scaling_client.create_auto_scaling_group(
            AutoScalingGroupName=AUTO_SCALING_GROUP_NAME,
            LaunchTemplate={
                "LaunchTemplateId": launch_template_id
            },
            MinSize=1,
            MaxSize=4,
            DesiredCapacity=2,
            AvailabilityZones=[az]
        )



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





response = client.create_vpc(
    CidrBlock='string',
    AmazonProvidedIpv6CidrBlock=True|False,
    Ipv6Pool='string',
    Ipv6CidrBlock='string',
    Ipv4IpamPoolId='string',
    Ipv4NetmaskLength=123,
    Ipv6IpamPoolId='string',
    Ipv6NetmaskLength=123,
    DryRun=True|False,
    InstanceTenancy='default'|'dedicated'|'host',
    Ipv6CidrBlockNetworkBorderGroup='string',
    TagSpecifications=[
        {
            'ResourceType': 'capacity-reservation'|'client-vpn-endpoint'|'customer-gateway'|'carrier-gateway'|'dedicated-host'|'dhcp-options'|'egress-only-internet-gateway'|'elastic-ip'|'elastic-gpu'|'export-image-task'|'export-instance-task'|'fleet'|'fpga-image'|'host-reservation'|'image'|'import-image-task'|'import-snapshot-task'|'instance'|'instance-event-window'|'internet-gateway'|'ipam'|'ipam-pool'|'ipam-scope'|'ipv4pool-ec2'|'ipv6pool-ec2'|'key-pair'|'launch-template'|'local-gateway'|'local-gateway-route-table'|'local-gateway-virtual-interface'|'local-gateway-virtual-interface-group'|'local-gateway-route-table-vpc-association'|'local-gateway-route-table-virtual-interface-group-association'|'natgateway'|'network-acl'|'network-interface'|'network-insights-analysis'|'network-insights-path'|'network-insights-access-scope'|'network-insights-access-scope-analysis'|'placement-group'|'prefix-list'|'replace-root-volume-task'|'reserved-instances'|'route-table'|'security-group'|'security-group-rule'|'snapshot'|'spot-fleet-request'|'spot-instances-request'|'subnet'|'subnet-cidr-reservation'|'traffic-mirror-filter'|'traffic-mirror-session'|'traffic-mirror-target'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-connect-peer'|'transit-gateway-multicast-domain'|'transit-gateway-policy-table'|'transit-gateway-route-table'|'transit-gateway-route-table-announcement'|'volume'|'vpc'|'vpc-endpoint'|'vpc-endpoint-service'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway'|'vpc-flow-log',
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },
    ]
)



subnet = ec2.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'capacity-reservation'|'client-vpn-endpoint'|'customer-gateway'|'carrier-gateway'|'dedicated-host'|'dhcp-options'|'egress-only-internet-gateway'|'elastic-ip'|'elastic-gpu'|'export-image-task'|'export-instance-task'|'fleet'|'fpga-image'|'host-reservation'|'image'|'import-image-task'|'import-snapshot-task'|'instance'|'instance-event-window'|'internet-gateway'|'ipam'|'ipam-pool'|'ipam-scope'|'ipv4pool-ec2'|'ipv6pool-ec2'|'key-pair'|'launch-template'|'local-gateway'|'local-gateway-route-table'|'local-gateway-virtual-interface'|'local-gateway-virtual-interface-group'|'local-gateway-route-table-vpc-association'|'local-gateway-route-table-virtual-interface-group-association'|'natgateway'|'network-acl'|'network-interface'|'network-insights-analysis'|'network-insights-path'|'network-insights-access-scope'|'network-insights-access-scope-analysis'|'placement-group'|'prefix-list'|'replace-root-volume-task'|'reserved-instances'|'route-table'|'security-group'|'security-group-rule'|'snapshot'|'spot-fleet-request'|'spot-instances-request'|'subnet'|'subnet-cidr-reservation'|'traffic-mirror-filter'|'traffic-mirror-session'|'traffic-mirror-target'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-connect-peer'|'transit-gateway-multicast-domain'|'transit-gateway-policy-table'|'transit-gateway-route-table'|'transit-gateway-route-table-announcement'|'volume'|'vpc'|'vpc-endpoint'|'vpc-endpoint-service'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway'|'vpc-flow-log',
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },
    ],
    AvailabilityZone='string',
    AvailabilityZoneId='string',
    CidrBlock='string',
    Ipv6CidrBlock='string',
    OutpostArn='string',
    VpcId='string',
    DryRun=True|False,
    Ipv6Native=True|False
)
