from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from notify.models import Action
from notify.serializers import ActionSerializer

class NotificationListView(APIView):
    
    def get_objects(self, username):
        
        notifications = Action.objects.filter(recipient__username = username)
        return notifications
    
    def get(self, request, username):
        
        notifications = self.get_objects(username)
        serializer = ActionSerializer(notifications, many = True)
        
        return Response(serializer.data, status = status.HTTP_200_OK)
        
