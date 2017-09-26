from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from authentication.models import Account
# Create your tests here.

class AuthenticationTestCase(APITestCase):
    
    def setUp(self):
        
        self.user = Account.objects.create_user(email = "casuru@uab.edu", username = "casuru", password = "password")
        
    def test_can_register(self):
        
        response = self.client.post('/api/v1/accounts/', {"email":"test@example.com",
            "username":"test",
            "password":"test"
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_can_update(self):
        
        self.client.force_authenticate(user = self.user)
        
        response = self.client.put('/api/v1/accounts/casuru/', {"email":"chineyeasuru@gmail.com"})
        
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
    
    def test_can_change_pass(self):
        
        self.client.force_authenticate(user = self.user)
        
        response = self.client.put('/api/v1/accounts/casuru/', {"password":"satan"})
        
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
    def test_permissions(self):
        
        unallowed = Account.objects.create_user(email='no@example.com', username = 'no', password = 'no')
        
        self.client.force_authenticate(user = unallowed)
        
        response = self.client.put('/api/v1/accounts/casuru/', {"username":"satan"})
        
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        unallowed.is_staff = True
        unallowed.save()
        
        response = self.client.put('/api/v1/accounts/casuru/', {"username":"satan"})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    
        
        response = self.client.put('/api/v1/accounts/satan/', {"username":"casuru","password":"test"})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        


        