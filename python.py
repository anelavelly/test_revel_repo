import boto3
import logging
import time
from classes import imagebuilderchecker
from classes import ec2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = 'us-east-1'
status = 'FAILED'

ibchecker = imagebuilderchecker.imagebuilderchecker(region)
ec2_obj = ec2.ec2(region)

image_arn = ibchecker.get_image_arn()

while status != 'AVAILABLE':
    status = ibchecker.check_if_ready(image_arn)
    print(status)
    if status not in ['FAILED', 'CREATING', 'BUILDING', 'AVAILABLE', 'TESTING', 'DISTRIBUTING', 'INTEGRATING', 'CANCELLED', 'FAILED', 'DEPRECATED', 'DELETED']:
        break
    if status in ['FAILED', 'CANCELLED', 'DELETED']:
        print('im here too')
        break
    if status != 'AVAILABLE':
        time.sleep(5)

if status == 'AVAILABLE':
    template_name='helloworldtest'
    ami_id = ibchecker.get_ami_id(image_arn)
    # ec2_obj.update_launch_template(template_name, ami_id)
    print(ami_id)
    template_id = ec2_obj.template_id(template_name)
    print(template_id)
    instance_ids = ec2_obj.get_instance_ids(template_id)
    print(instance_ids)
    # ec2_obj.terminate_instances(instance_ids)
    print('done')
