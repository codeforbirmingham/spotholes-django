from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse

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
    comment = models.TextField(max_length = 2000, null = True, blank= True)
    status = models.CharField(max_length = 2, null = True, blank = True, default = 'ur')
    date_added = models.DateTimeField(auto_now_add = True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
    def __unicode__(self):
        
        
        return self.action
        
    def save(self, *args, **kwargs):
        
        if self.action == 'u':
            
            q = Action.objects.filter(user = self.user, action = 'd', object_id = self.object_id, content_type = self.content_type)
            
            if q.exists():
                
                Action.objects.get(user = self.user, action = 'd', object_id = self.object_id, content_type = self.content_type).delete()
            
        
        elif self.action == 'd':
            
            q = Action.objects.filter(user = self.user, action = 'u', object_id = self.object_id, content_type = self.content_type)
        
            if q.exists():
                
                Action.objects.get(user = self.user, action = 'u', object_id = self.object_id, content_type = self.content_type).delete()
            
        
        super(Action, self).save(*args, **kwargs)
    
    
    class Meta:
        
        unique_together = (('action', 'object_id', 'user', 'content_type',))