from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from kuser.models import KUser
from kuser.views import *

User = get_user_model()


'''   Tests for UserList() view. '''
class TestUserList(APITestCase):

    def setUp(self):
        
        self.view = UserList.as_view()
        self.factory = APIRequestFactory()

        self.user_data = {
                            'email': 't0@kangaa.xyz',
                            'password': 'test_pwd'
        }
        self.path = '/v1/users/'

    ''' (Helper Function) Create a user. '''
    def create_user(self, expected_status):
       
        request = self.factory.post(self.path, self.user_data, format='json')
        force_authenticate(self.view)
        response = self.view(request)
        
        self.assertEqual(response.status_code, expected_status)
        
    ''' Create a user. '''
    def test_create_user(self):
        
        self.create_user(expected_status=status.HTTP_201_CREATED)

    ''' Attempt to create a user that already exists in the DB. '''
    def test_create_duplicate_user(self):

        User.objects.create_user(email='t0@kangaa.xyz', password='test_pwd')
        self.create_user(expected_status=status.HTTP_404_NOT_FOUND)


'''   Tests for UserList() view. '''
class TestUserDetail(APITestCase):

    def setUp(self):

        self.view = UserDetail.as_view()
        self.factory = APIRequestFactory()
        
        self.user_a = User.objects.create_user(email='user_a@kangaa.xyz',
                        password='pwd_a')
        self.user_b = User.objects.create_user(email='user_b@kangaa.xyz',
                        password='pwd_b')

        self.user_a_id = self.user_a.id
        self.user_b_id = self.user_b.id

        self.user_a_path = '/v1/users/' + str(self.user_a_id)
        self.user_b_path = '/v1/users/' + str(self.user_b_id)

    ''' Ensure that Profiles are created when Users are intialized. '''
    def test_user_profile_created_on_init(self):

        self.assertEqual(Profile.objects.filter(id=self.user_a.profile.id).count(), 1)
        
    ''' (Helper Function) Update a User. '''
    def update_user(self, user, update, path, uid, expected_status, auth=False):
 
        request = self.factory.put(path, update, format='json')
        force_authenticate(request, user=user)
        response = self.view(request, uid)

        self.assertEqual(response.status_code, expected_status)
        if auth: self.assertEqual(response.data['email'], update['email'])
        
    ''' Update a User with the correct authentication. '''
    def test_update_user_with_auth(self):
       
        self.update_user(user=self.user_a, update={'email': 'new_email@kangaa.xyz'},
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_200_OK, auth=True)

    ''' Attempt to update a User with the wrong authentication. '''
    def test_update_user_with_wrong_auth(self):
         
        self.update_user(user=self.user_b, update={'email': 'new_email@kangaa.xyz'},

                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_403_FORBIDDEN)

    ''' Attempt to update a User with no authentication. '''
    def test_update_user_with_no_auth(self):
        
        self.update_user(user=None, update={'email': 'new_email@kangaa.xyz'},
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_401_UNAUTHORIZED)
     
    ''' Perform a nested update a User with the correct authentication. '''
    def test_nested_update_user_with_auth(self):
       
        update = { 'profile': { 'first_name': 'Test' } }
        self.update_user(user=self.user_a, update=update,
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_200_OK)

    ''' Attempt a nested update for a User, with the wrong authentication. '''
    def test_nested_update_user_with_wrong_auth(self):
         
        update = { 'profile': { 'first_name': 'Test' } }
        self.update_user(user=self.user_b, update=update,
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_403_FORBIDDEN)

    ''' Attempt a nested update for a User, with no authentication. '''
    def test_nested_update_user_with_no_auth(self):
        
        update = { 'profile': { 'first_name': 'Test' } }
        self.update_user(user=None, update=update,
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_401_UNAUTHORIZED)
 
    ''' (Helper Function) Delete a User. '''
    def delete_user(self, user, path, uid, expected_status):
        
        request = self.factory.delete(path)
        force_authenticate(request, user=user)
        response = self.view(request, uid)

        self.assertEqual(response.status_code, expected_status)

    ''' Delete a User with the correct authentication. '''
    def test_delete_user_with_auth(self):

        self.delete_user(user=self.user_a,
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_204_NO_CONTENT)

    ''' Attempt to delete a User with the wrong authentication. '''
    def test_delete_user_with_wrong_auth(self):

        self.delete_user(user=self.user_b,
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_403_FORBIDDEN)

    ''' Attempt to delete a User with no authentication. '''
    def test_delete_user_with_no_auth(self):

        self.delete_user(user=None,
                path=self.user_a_path, uid=self.user_a_id,
                expected_status=status.HTTP_401_UNAUTHORIZED)

