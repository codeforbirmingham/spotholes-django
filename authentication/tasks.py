import boto3
from authentication.models import Account
from django.conf import settings


def subscribe(username):
    
    obj = Account.objects.get(username = username)
    sns = boto3.resource('sns', region_name='us-west-2', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    topic = sns.Topic('arn:aws:sns:us-west-2:781665968837:sPotholeReports')
    
    if obj.is_staff:
        
        topic.subscribe(Protocol = 'email', Endpoint = obj.email)
    
    