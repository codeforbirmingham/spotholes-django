from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from potholes.models import Pothole
from authentication.models import Account
from rest_framework import status
# Create your tests here.

class PermissionCase(APITestCase):
    
    def setUp(self):
        self.users = [Account.objects.create_user(email = 'test@example', username = 'test', password = 'password'),
        Account.objects.create_user(email = 'test1@example', username = 'test1', password = 'password'),
        Account.objects.create_user(email = 'test2@example', username = 'test2', password = 'password')]
        Pothole.objects.create(user = self.users[0] , longitude = '-43.43234',
        latitude = '34.34344', status = 'uv', rating = 4, name = 'a pothole')
        #self.factory = APIRequestFactory()


    def test_accept_safe(self):
        
        response = self.client.get('/api/v1/potholes/')
        self.assertEqual(response.status_code, 200)
        
    def test_reject_unauthenticated_unsafe(self):
        
        response = self.client.post('/api/v1/potholes/', {
            'user': self.users[0].id , 'longitude':'-43.43234',
            'latitude':'34.34344', 'status':'uv', 'rating' : 4, 'name':'a pothole'
        })
        
        self.assertEqual(response.status_code, 403)
        
    def test_allow_authenticated_create(self):
        
        self.client.force_authenticate(user=self.users[0])
        response = self.client.post('/api/v1/potholes/', {
            'user': self.users[0].id , 'longitude':'-43.43234',
            'latitude':'34.34344', 'status':'uv', 'rating' : 4, 'name':'a pothole'
        })
        
        self.assertEqual(response.status_code, 201)
   
    def test_allow_owner_or_moderator_to_modify(self):
        
        self.client.force_authenticate(user = self.users[0])
        response = self.client.patch('/api/v1/potholes/1/', {'status':'vd'})
        
        self.assertEqual(response.status_code, 202)
        
        self.client.force_authenticate(user = self.users[1])
        
        response = self.client.put('/api/v1/potholes/1/', {
            'longitude':'-43.43234',
            'latitude':'34.34344', 'status':'uv', 'rating' : 4, 'name':'a pothole'
        })
        
        self.assertEqual(response.status_code, 403)
        
    def test_create_report(self):
        
        self.client.force_authenticate(user = self.users[1])
        response = self.client.post('/api/v1/potholes/1/reports/', {"comment":"no comment."})
        self.assertEqual(response.status_code, 201)
        
        
        
        
  
        