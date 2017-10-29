from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from notify.models import Action
from potholes.models import Pothole
from authentication.models import Account
from notify.serializers import ActionSerializer
from django.http import Http404
from django.contrib.contenttypes.models import ContentType

class NotificationListView(APIView):
    
    def get_objects(self, username):
        
        notifications = Action.objects.filter(recipient__username = username)
        return notifications
    
    def get(self, request, username):
        
        notifications = self.get_objects(username)
        serializer = ActionSerializer(notifications, many = True, context = {'request':request})
        
        return Response(serializer.data, status = status.HTTP_200_OK)
        

class PotholeVoteView(APIView):
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def get_object(self, pk):
        
        try:
            obj = Pothole.objects.get(id = pk)
            self.check_object_permissions(self.request, obj)
        
            return obj
            
        except Pothole.DoesNotExist:
            
            raise Http404
            
    
    def get(self, request, pk, format =  None):
        
        pothole = self.get_object(pk)
        
        data = {"up_votes": pothole.up_votes.count(), "down_votes": pothole.down_votes.count()}
        
        return Response(data, status = status.HTTP_200_OK)
        
   
    def post(self, request, pk, format = None):
        
        pothole = self.get_object(pk)
        
        request.data['content_object'] = pothole.get_absolute_url()
        request.data['object_id'] = pothole.id
        request.data['recipient'] = pothole.user.id
        request.data['user'] = request.user.id
        request.data['content_type'] = ContentType.objects.get(model = 'pothole').id
        
        action_serializer = ActionSerializer(data = request.data)
        
       
        
        if action_serializer.is_valid():
            
            action_serializer.save(user = request.user, recipient = pothole.user)
        
        
            return Response({"message":"Vote recieved"}, status = status.HTTP_201_CREATED)
            
        return Response(action_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AccountVoteView(APIView):
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def get_object(self, username):
        
        try:
            
            return Account.objects.get(username = username)
            
        except Account.DoesNotExist:
            
            raise Http404
            

    def get(self, request, username, format =  None):
        
        account = self.get_object(username)
        
        data = {"up_votes": account.up_votes.count(), "down_votes": account.down_votes.count()}
        
        return Response(data, status = status.HTTP_200_OK)
        
    
    def post(self, request, username, format = None):
        
        account = self.get_object(username)
        
        request.data['content_object'] =account.get_absolute_url()
        request.data['object_id'] = account.id
        request.data['recipient'] = account.id
        request.data['user'] = request.user.id
        request.data['content_type'] = ContentType.objects.get(model = 'account').id
            