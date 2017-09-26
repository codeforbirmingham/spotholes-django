# Create your tasks here

from __future__ import absolute_import, unicode_literals
from django.conf import settings
from potholes.models import Report
import boto3



def send_report(pothole, report):
    
    sns = boto3.resource('sns', region_name='us-west-2', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    topic  = sns.Topic('arn:aws:sns:us-west-2:781665968837:sPotholeReports')
    

    title = "New User Report"
    pothole = '/api/v1/potholes/{0}/'.format(report.pothole.id)
    message = "User {0} has reported pothole {1}\n comment : {2}".format(report.user.username, pothole, report.comment)
        
    topic.publish(TopicArn='arn:aws:sns:us-west-2:781665968837:sPotholeReports',
            Message=message,
            Subject=title)
        
    report.status = 'uv'
    report.save()
    
