import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class imagebuilderchecker:
    def __init__(self,region):
        try:
            self.region=region
            self.client = boto3.client('imagebuilder',region_name=region)
        except Exception as e:
            logger.error('Error in initialization: ' + str(e))

    def get_image_arn(self):
        try:
            response = self.client.list_images(filters=[
                    {
                        'name': 'name',
                        'values': [
                            'revelmediagroup-dev-revel-image-recipe',
                        ]
                    },
                    {
                        'name': 'version',
                        'values': [
                            '1.0.0',
                        ]
                    },
                ])
            # print(response)

            arn = response['imageVersionList'][0]['arn']
            return arn
        except Exception as e:
            logger.error('Failed in get_image_arn' + str(e))

    def check_if_ready(self, arn): 
        try:
            response = self.client.list_image_build_versions(
                imageVersionArn=arn
            )

            state = response['imageSummaryList'][0]['state']
            status = state['status']

            return status
        except Exception as e:
            logger.error('Failed in check_if_ready' + str(e))

    def get_ami_id(self, arn):
        try:
            response = self.client.list_image_build_versions(
                imageVersionArn=arn
            )

            image_id = response['imageSummaryList'][0]['outputResources']['amis'][0]['image']
            
            return(image_id)
        except Exception as e:
            logger.error('Failed in get_ami_id' + str(e))
