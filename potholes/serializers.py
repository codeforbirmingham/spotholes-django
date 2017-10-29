from rest_framework import serializers
from potholes.models import Pothole, Report



class PotholeSerializer(serializers.ModelSerializer):

    
    class Meta:
        
        model = Pothole
        fields = '__all__'
        
        

class ReportSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model = Report
        fields = '__all__'
