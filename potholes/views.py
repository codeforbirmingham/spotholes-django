from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from potholes.serializers import PotholeSerializer
from potholes.models import Pothole
from authentication.models import Account
from rest_framework import status, permissions
from potholes.permissions import IsModeratorOwnerOrReadOnly
from django.http import Http404
from rest_framework.settings import api_settings
from spotholes.mixins import PaginationMixin



# Create your views here.
        
class ListPotholeView(PaginationMixin, APIView):
    
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def get_objects(self):
        
        objs = Pothole.objects.all()
        return objs
    
    def get(self, request, format = None):
        
        objs = self.get_objects()
        page = self.paginate_queryset(objs)
        
        if page is not None:
            
            serializer = PotholeSerializer(page, many = True)
            
            return self.get_paginated_response(serializer.data)
            
        serializer = PotholeSerializer(objs, many = True)
        
        return Response(serializer.data, status = status.HTTP_200_OK)
        
    
    def post(self, request):
        
        serializer = PotholeSerializer(data = request.data)
        
        if serializer.is_valid():
            
            serializer.save(user = request.user)
            
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        


class PotholeDetailView(APIView):
    
    permission_classes = (IsModeratorOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    
    def get_object(self, pk):
        try:
            obj = Pothole.objects.get(id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Pothole.DoesNotExist:
            raise Http404
            
    
    def get(self, request, pk, format = None):
        
        obj = self.get_object(pk)
        serializer = PotholeSerializer(obj)
        
        return Response(serializer.data)
        

    def put(self, request, pk, format = None):
        
        obj = self.get_object(pk)
        serializer = PotholeSerializer(obj, data = request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk, format = None):
        
        obj = self.get_object(pk)
        serializer = PotholeSerializer(obj, data = request.data, partial = True)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, pk):
        
        obj = self.get_object(pk)
        
        obj.delete()
        
        return Response(status = status.HTTP_204_NO_CONTENT)
        
class PotholeByUserListView(APIView):
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsModeratorOwnerOrReadOnly)
    
    def get_objects(self, username):
        
        try:
            account = Account.objects.get(username = username)
            return Pothole.objects.filter(user = account)
            
        except Account.DoesNotExist:
            
            raise Http404
    
    def get(self, request, username, format = None):
        
        objs = self.get_objects(username)
        serializer = PotholeSerializer(objs, many = True)
        
        return Response(serializer.data, status = status.HTTP_200_OK)
        
