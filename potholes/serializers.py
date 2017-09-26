from rest_framework import serializers
from potholes.models import Pothole, Report, Vote



class PotholeSerializer(serializers.ModelSerializer):
    
    votes = serializers.SerializerMethodField()
    
    def get_votes(self, obj):
        
        return obj.vote_set.count()
    
    class Meta:
        
        model = Pothole
        fields = '__all__'
        
        

class ReportSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model = Report
        fields = '__all__'
        
        
class VoteSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model = Vote
        fields = '__all__'
