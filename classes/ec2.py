import boto3
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ec2:
    def __init__(self,region):
        try:
            self.region=region
            self.client = boto3.client('ec2',region_name=region)
        except Exception as e:
            logger.error('Error in initialization: ' + str(e))

    def update_launch_template(self, templateName, ami):
        response = self.client.create_launch_template_version(
            LaunchTemplateName=templateName,
            LaunchTemplateData={
                'IamInstanceProfile': {
                    'Arn': 'arn:aws:iam::324767943142:instance-profile/revelmediagroup-dev-iam-role-InstanceProfile-EQ1RY9BYEV24'
                },
                'ImageId': ami,
                'InstanceType': 't3.micro',
                'KeyName': 'onica-workloads-us-east-1',
                'TagSpecifications': [
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'Helloworld'
                        },
                        {
                            'Key': 'Env',
                            'Value': 'Test'
                        }
                    ]
                }],
                'SecurityGroupIds': [
                    'sg-05e6d9dd348896149',
                ],
            })

    def template_id(self, templateName):
        response = self.client.describe_launch_templates(
            LaunchTemplateNames=[
                templateName,
            ]
        )
        return response['LaunchTemplates'][0]['LaunchTemplateId']

    def get_instance_ids(self, key_value):
        try:
            ec2_ids = []
            response = self.client.describe_instances(Filters=[
                {
                    'Name': 'tag:aws:ec2launchtemplate:id',
                    'Values': [
                        key_value,
                    ]
                },
            ])
            for r in response['Reservations']:
                for i in r['Instances']:
                    ec2_ids.append(i['InstanceId'])
            return ec2_ids
        except Exception as e:
            logger.error('Failed in get_instance_ids' + str(e))

    def terminate_instances(self, ids):
        try:
            for id in ids:
                response = self.client.terminate_instances(
                    InstanceIds=[
                        id,
                    ]
                )
                print('waiting for 300sec for new instance to be ready')
                # time.sleep(300)
        except Exception as e:
            logger.error('Failed in terminate_instances' + str(e))
