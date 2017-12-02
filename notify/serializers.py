from rest_framework import serializers
from potholes.serializers import PotholeSerializer
from authentication.serializers import AccountSerializer
from authentication.models import Account
from potholes.models import Pothole
from notify.models import Action
from generic_relations.relations import GenericRelatedField


        
class ActionSerializer(serializers.ModelSerializer):
    

        
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
        
        
    