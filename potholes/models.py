from __future__ import unicode_literals

from django.db import models
from rest_framework.reverse import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from authentication.models import Account
from notify.models import Action



# Create your models here.


class Pothole(models.Model):
    
    STATUS_CHOICES = (
        ('uv', 'unverified'),
        ('vd', 'verified'),
        ('tg', 'tagged'),
        ('fx', 'fixed'),
    )
    
    user = models.ForeignKey(Account, blank = True)
    name = models.CharField(max_length = 225)
    longitude = models.CharField(max_length = 50)
    latitude = models.CharField(max_length = 50)
    photo = models.ImageField(default = 'chain_rule.PNG', upload_to = 'potholes/')
    thumbnail = ImageSpecField(source = 'photo', processors = [ResizeToFill(300, 250)], format = 'JPEG', options={'quality': 60})
    status = models.CharField(default = 'uv', max_length = 10, choices = STATUS_CHOICES)
    actions = GenericRelation(Action)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        
        return self.name
        
    def get_absolute_url(self):
        
        
        return reverse('pothole-detail', args = [self.id])
        
  
        
        