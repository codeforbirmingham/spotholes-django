from rest_framework import serializers
from authentication.models import Account
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash


class AccountSerializer(serializers.ModelSerializer):
    
    def get_membership_length(self, obj):
        
        delta = timezone.now() - obj.created_at
        
        if delta.days < 365:
            
            return "{0} days".format(delta.days)
            
        return "{0} years".format(delta.days//365)
        
    membership_length = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'score', 'membership_length', 'is_staff')
        write_only_fields = ('password', 'is_active')
        read_only_fields = ('score', 'membership_length')
        
    
    
    def create(self, validated_data):
        
        
        return Account.objects.create_user(**validated_data)
        
    def update(self, instance, validated_data):
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        
        password = validated_data.get('password', None)
        
        if password:
            
            instance.set_password(password)
            update_session_auth_hash(self.context.get('request', None), instance)
            
            instance.save()
            
            
        return instance
        
        
    
        
        
        
    
    