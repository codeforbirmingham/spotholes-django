from rest_framework import serializers
from potholes.models import Pothole, Report
from potholes.serializers import PotholeSerializer, ReportSerializer
from authentication.serializers import AccountSerializer
from authentication.models import Account
from notify.models import Action, Notification

class RelatedFieldSerializer(serializers.RelatedField):
    
    def to_representation(self, value):

        if isinstance(value, Pothole):
            serializer = PotholeSerializer(value)
        elif isinstance(value, Account):
            serializer = AccountSerializer(value)
        else:
            raise Exception('Unexpected object')

        return serializer.data
        
class ActionSerializer(serializers.ModelSerializer):
    
    content_object = RelatedFieldSerializer(read_only = True)
    
    class Meta:
        
        model = Action
        fields = '__all__'
        read_only_fields = ['content_object']
        
    