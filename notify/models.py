from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Action(models.Model):
    
    UP_VOTE = 'u'
    DOWN_VOTE = 'd'
    REPORT = 'r'
    
    ACTIONS = (
        (UP_VOTE, 'Up Vote'), 
        (DOWN_VOTE, 'Down Vote'),
        (REPORT, 'Report')
        )
    
    user = models.ForeignKey('authentication.Account', related_name = 'sent')
    recipient = models.ForeignKey('authentication.Account', related_name = 'recieved')
    action = models.CharField(max_length = 1, choices = ACTIONS)
    date_added = models.DateTimeField(auto_now_add = True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
    def __unicode__(self):
        
        
        return self.action


class Notification(models.Model):
    
    user = models.ForeignKey('authentication.Account')
    message = models.CharField(max_length = 225)
    created_at = models.DateTimeField(auto_now_add = True)
    
    
    def __unicode__(self):
        
        return self.message
