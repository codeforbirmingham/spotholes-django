from rest_framework import serializers
from potholes.serializers import PotholeSerializer
from authentication.serializers import AccountSerializer
from authentication.models import Account
from potholes.models import Pothole
from notify.models import Action
from generic_relations.relations import GenericRelatedField
from django.contrib.contenttypes.models import ContentType

class ActionSerializer(serializers.ModelSerializer):
    
    def add_initial(self):
        
        validated_data = {}
        if hasattr(self.context['content_object'], 'user'):
            
            validated_data['recipient'] = self.context['content_object'].user.id
            
        else:
            
            validated_data['recipient'] = self.context['object_object'].id
                
        validated_data['content_object'] = self.context['content_object'].get_absolute_url()
        validated_data['object_id'] = self.context['content_object'].id
        validated_data['user'] = self.context['request'].user.id
        validated_data['content_type'] = ContentType.objects.get_for_model(type(self.context['content_object'])).id
                
        if self.initial_data:
            
            self.initial_data.update(validated_data)
            
        
        
    
    content_object = GenericRelatedField({
        Account: serializers.HyperlinkedRelatedField(
            view_name = 'account-detail',
            queryset = Account.objects.all(),
            lookup_field = 'username'
            
        ),
        Pothole: serializers.HyperlinkedRelatedField(
            view_name = 'pothole-detail',
            queryset = Pothole.objects.all(),
            lookup_field = 'pk'
        )}, 
        read_only = False
    )
    
    
    class Meta:
        
        model = Action
        fields = '__all__'
        
        
    
        
class VoteSerializer(ActionSerializer):
    
    
    def validate_action(self, value):
        
        if value not in ['u', 'd']:
            
            raise serializers.ValidationError("Please submit an up or down vote.")
            
        return value
        
        
        

class ReportSerializer(ActionSerializer):
    
    def validate_action(self, value):
        
        if value != 'r':
            
            raise serializers.ValidationError("Please submit a report.")
            
        return value

        
    