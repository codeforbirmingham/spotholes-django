from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from notify.models import Action
from potholes.models import Pothole
from authentication.models import Account
from notify.serializers import VoteSerializer, ReportSerializer,  ActionSerializer
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

class NotificationListView(APIView):
    
    def get_objects(self, username):
        
        notifications = Action.objects.all()
        
        if self.request.user.is_staff:
            
            notifications = notifications.filter(Q(action = 'r') | Q(recipient__username = username))
            
            return notifications
            
        notifications = notifications.filter(recipient__username = username )
            
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
        
        data = {"up_votes": pothole.actions.filter(action = 'u').count(), "down_votes": pothole.actions.filter(action = 'd').count()}
        
        return Response(data, status = status.HTTP_200_OK)
        
   
    def post(self, request, pk, format = None):
        
        pothole = self.get_object(pk)
        
        vote_serializer = VoteSerializer(data = request.data, context = {"request":request, "content_object": pothole})
        vote_serializer.add_initial()
        
        if vote_serializer.is_valid():
            
            vote_serializer.save(user = request.user, recipient = pothole.user)
        
        
            return Response({"message":"Vote recieved"}, status = status.HTTP_201_CREATED)
            
        return Response(vote_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AccountVoteView(APIView):
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def get_object(self, username):
        
        try:
            
            return Account.objects.get(username = username)
            
        except Account.DoesNotExist:
            
            raise Http404
            

    def get(self, request, username, format =  None):
        
        account = self.get_object(username)
        
        data = {"up_votes": account.actions.filter(action = 'u').count(), "down_votes": account.actions.filter(action = 'd').count()}
        
        return Response(data, status = status.HTTP_200_OK)
        
    
    def post(self, request, username, format = None):
        
        account = self.get_object(username)
        
        vote_serializer = ActionSerializer(data = request.data, context = {"request":request, "content_object": account})
        vote_serializer.add_initial()
        
        if vote_serializer.is_valid():
            
            vote_serializer.save()
            
            data = {"up_votes": account.actions.filter(action = 'u').count(), "down_votes": account.actions.filter(action = 'd').count()}
            
            return Response(data, status = status.HTTP_201_CREATED)
            
        
        return Response(vote_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PotholeReportView(APIView):
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def get_object(self, pk):
        
        try:
            obj = Pothole.objects.get(id = pk)
            self.check_object_permissions(self.request, obj)
        
            return obj
            
        except Pothole.DoesNotExist:
            
            raise Http404
    
    def get(self, request, pk, format = None):
        
        
        pothole = self.get_object(pk)
        reports = pothole.actions.filter(action = 'r')
        report_serializer = ReportSerializer(reports, many = True, context = {"request":request})
        
        return Response(report_serializer.data, status = status.HTTP_200_OK)
   
    def post(self, request, pk, format = None):
        
        pothole = self.get_object(pk)
        report_serializer = ReportSerializer(data = request.data, context = {"request":request, "content_object": pothole})
        report_serializer.add_initial()
        if report_serializer.is_valid():
            
            report_serializer.save(user = request.user, recipient = pothole.user)
        
        
            return Response({"message":"Report is being reviewed."}, status = status.HTTP_201_CREATED)
            
        return Response(report_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

