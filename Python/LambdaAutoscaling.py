# boto3 - library providing the low-level functionality shared between the Python SDK and the AWS CLI
import boto3
import os
# Boto Connection

def lambda_handler(event, context):
  print(event)
  asg = boto3.client('autoscaling',event['aws_region'])
  response = asg.update_auto_scaling_group(AutoScalingGroupName=event['asg_name'],MinSize=int(event['min']),DesiredCapacity=int(event['desired']),MaxSize=int(event['max']))
  print(response)