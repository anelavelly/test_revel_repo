#!/bin/bash
arn=`aws cloudformation describe-stacks --stack-name revelmediagroup-dev-image-pipeline --query "Stacks[0].Outputs[0].OutputValue" --output text --region us-east-1`
aws imagebuilder start-image-pipeline-execution --image-pipeline-arn $arn --region us-east-1
aws imagebuilder get-image-pipeline --image-pipeline-arn $arn --region us-east-1
python3 ../python.py
