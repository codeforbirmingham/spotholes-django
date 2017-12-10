from rest_framework import serializers
from potholes.models import Pothole



class PotholeSerializer(serializers.ModelSerializer):

    
    class Meta:
        
        model = Pothole
        fields = '__all__'
        
