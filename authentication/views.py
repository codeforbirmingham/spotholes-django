from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator
from authentication.models import Account
from authentication.serializers import AccountSerializer, EmailSerializer, PasswordResetSerializer
from authentication.permissions import IsUserOrModeratorOrReadOnly, IsModerator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from spotholes.mixins import PaginationMixin
from rest_framework.settings import api_settings



# Create your views here.

class AccountListView(PaginationMixin, APIView):
    
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    
    def get(self, request):
        
        objs = Account.objects.all()
        
        page = self.paginate_queryset(objs)
        
        if page is not None:
            
            serializer = AccountSerializer(page, many = True)
            
            return self.get_paginated_response(serializer.data)
            
        serializer = AccountSerializer(objs, many = True)        
        return Response(serializer.data, status = status.HTTP_200_OK)
        
    
    def post(self, request):
        
        serializer = AccountSerializer(data = request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

class AccountDetailView(APIView):
    
    permission_classes = (IsUserOrModeratorOrReadOnly, )
    
    def get_object(self, username):
        
        try:
            obj = Account.objects.get(username = username)
            self.check_object_permissions(self.request, obj)
            return obj
        
        except Account.DoesNotExist:
            
            raise Http404
            
    def get(self, request, username):

        obj = self.get_object(username)
        serializer = AccountSerializer(obj)
        
        return Response(serializer.data, status = status.HTTP_200_OK)
        
    
    def patch(self, request, username):
        
        obj = self.get_object(username)
        serializer = AccountSerializer(obj, data = request.data, partial = True)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

class AccountStatusView(APIView):
    
    permission_classes = (IsModerator, )
    
    def get_object(self, username):
        
        try:
            obj = Account.objects.get(username = username)
            self.check_object_permissions(self.request, obj)
            return obj
        
        except Account.DoesNotExist:
            
            raise Http404
    
    def patch(self, request, username):
        
        obj = self.get_object(username)
        print(request.data)
        serializer = AccountSerializer(obj, data = request.data, partial = True)
    
        if serializer.is_valid():
        
            serializer.save()
            
            
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        

class SignInView(APIView):
    
    
    def post(self, request):
    
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        user = authenticate(username = email, password = password)
        
        if user is not None:
            
            login(request, user)
            serializer = AccountSerializer(request.user)
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
            
        
        return Response({"detail": "No user with those credentials exists"}, status = status.HTTP_403_FORBIDDEN)
        
class SignOutView(APIView):
    
    def get(self, request):
        
        logout(request)
        
        return Response({"message":"See you next time"}, status = status.HTTP_302_FOUND)
        

class PasswordResetRequestView(APIView):
    
    def get_object(self, email):
        
        try:
            obj = Account.objects.get(email = email)

            return obj
        
        except Account.DoesNotExist:
            
            return None
    
    def post(self, request, format = None):
        
        serializer = EmailSerializer(data = request.data)
        
        if serializer.is_valid():
            
            email = request.data.get('email', None)
            user = self.get_object(email)
            
            if user is not None:
                
                token = default_token_generator.make_token(user)
                print token
            
            return Response({"message":"An email has been sent with the appropriate instructions"})
            
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        

class PasswordResetConfirmView(APIView):
    
    def get_object(self, uib64):
        
        try:
            obj = Account.objects.get(pk = uib64)
            
        
        except Account.DoesNotExist:
            
            obj = None
        
        return obj
        
    
    def patch(self, request, uidb64, token, format = None):
        
        
        uidb64 = urlsafe_base64_decode(uidb64)
        user = self.get_object(uidb64)
        
        if user is not None:
            
            if default_token_generator.check_token(user, token):
                
                
                serializer = PasswordResetSerializer(user, data = request.data)
                
                if serializer.is_valid():
                    
                    serializer.save()
                    
                    return Response({"message":"You may now login with your updated credentials."}, status = status.HTTP_202_ACCEPTED)
                    
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":"Their was a problem with your request"}, status = status.HTTP_400_BAD_REQUEST)
        
        


    
            
            
        
        
        
        
        
        