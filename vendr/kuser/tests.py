from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from kuser.models import *
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
        self.create_user(expected_status=status.HTTP_400_BAD_REQUEST)


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


'''   Tests on the ChatList() view. '''
class TestChatList(APITestCase):

    def setUp(self):
        
        self.view = ChatList.as_view()
        self.factory = APIRequestFactory()

        # Create users.
        self.user_a = User.objects.create(email='sender@vendr.xyz',
                password='sender')
        self.user_b = User.objects.create(email='recipient@vendr.xyz',
                password='recipient')
        self.chat_data = { 'participants': [self.user_b.pk] }
 
        self.path_a = '/v1/users/{}/chat/'.format(self.user_a.pk)
        self.path_b = '/v1/users/{}/chat/'.format(self.user_b.pk)

    ''' (Helper) Creates a Chat object. '''
    def create_chat(self, user, path):

        request = self.factory.post(path, self.chat_data, format='json')
        force_authenticate(request, user=user)
        response = self.view(request, user.pk)

        return response
    
    ''' Create a chat. '''
    def test_create_chat(self):
        
        response = self.create_chat(user=self.user_a, path=self.path_a)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    ''' Ensure we can read chats on our endpoint. '''
    def test_read_chat(self):
        
        chat_response = self.create_chat(user=self.user_a, path=self.path_a)
        chat_data = chat_response.data
        
        request = self.factory.get(self.path_a, format='json')
        force_authenticate(request, user=self.user_a)
        response = self.view(request, self.user_a.pk)

        self.assertEquals(response.data[0]['pk'], chat_data['pk'])
        self.assertEquals(response.data[0]['participants'],
                chat_data['participants'])

    ''' Ensure sender is included in participants implicitly. '''
    def test_sender_included_in_participants(self):

        request = self.factory.post(self.path_a, self.chat_data, format='json')
        force_authenticate(request, user=self.user_a)
        response = self.view(request, self.user_a.pk)

        self.assertItemsEqual(response.data['participants'],
                [self.user_a.pk, self.user_b.pk])

    ''' Ensure all desired participants are included. '''
    def test_participants(self):

        request = self.factory.post(self.path_a, self.chat_data, format='json')
        force_authenticate(request, user=self.user_a)
        response = self.view(request, self.user_a.pk)
        
        # Ensure our recipient is included.
        self.assertItemsEqual(response.data['participants'],
                [self.user_a.pk, self.user_b.pk])
        
        # Ensure only our sender and recipient are included.
        self.assertEqual(len(response.data['participants']), 2)

    ''' Create a chat with another user on their endpoint. This should fail
        as all chat related activities must be performed on a user's own
        endpoint. '''
    def test_create_chat_on_wrong_endpoint(self):
        
        request = self.factory.post(self.path_b, self.chat_data, format='json')
        force_authenticate(request, user=self.user_a)
        response = self.view(request, self.user_b.pk)

        self.assertEqual(response.status_code, 403)
    
    ''' Read a chat with another user on THEIR endpoint. This should fail, as
        all chat related activites must be performed on a user's own endpoint.
    '''
    def test_read_chat_on_wrong_endpoint(self):

        # Create the chat.
        self.create_chat(user=self.user_a, path=self.path_a)

        # Now, user A attempts to read on user B's endpoint.
        request = self.factory.get(self.path_b, format='json')
        force_authenticate(request, user=self.user_a)
        response = self.view(request, self.user_b.pk)
        
        self.assertEqual(response.status_code, 403)


'''   Tests on the ChatDetail view. '''
class TestChatDetail(APITestCase):

    def setUp(self):
        
        self.view = ChatDetail.as_view()
        self.factory = APIRequestFactory()

        # Create users.
        self.user_a = User.objects.create(email='sender@vendr.xyz',
                password='sender')
        self.user_b = User.objects.create(email='recipient@vendr.xyz',
                password='recipient')
 
        # Create our Chat.
        self.chat = Chat.objects.create(participants=[self.user_a.pk,
                        self.user_b.pk])
        
        self.path_a = '/v1/users/{}/chat/{}/'.format(self.user_a.pk, self.chat.pk)
        self.path_b = '/v1/users/{}/chat/{}/'.format(self.user_b.pk, self.chat.pk)

    ''' Read a chat on your own endpoint. '''
    def test_read_chat(self):
        '''
        request = self.factory.get(self.path_a, format='json')
        force_authenticate(request, user=self.user_a)
        response = self.view(request, self.user_a.pk, self.chat.pk)

        #TODO: kwargs not passed through to the view!
        assertEquals(response.status_code, 200)
        assertEquals(response.data[0]['pk'], self.chat.pk)
        assertEquals(response.data[0]['participants'], self.chat.participants)
        '''
    def test_read_chat_on_wrong_endpoint(self):
        '''
        #TODO: kwargs not passed through to the view!
        request = self.factory.get(self.path_b, format='json')
        force_authenticate(request, user=self.user_a)
        response = self.view(request, self.user_b.pk, self.chat.pk)
 
        assertEquals(response.status_code, 403)
        '''

class TestMessageList(APITestCase):

    def setUp(self):

        self.view = MessageList.as_view()
        self.factory = APIRequestFactory()

        # Create users.
        self.user_a = User.objects.create(email='sender@vendr.xyz',
                password='sender')
        self.user_b = User.objects.create(email='recipient@vendr.xyz',
                password='recipient')
 
        # Create our Chat.
        self.chat = Chat.objects.create(participants=[self.user_a.pk,
                        self.user_b.pk])
        
        self.path_a = '/v1/users/{}/chat/{}/messages/'.\
                      format(self.user_a.pk, self.chat.pk)
        self.path_b = '/v1/users/{}/chat/{}/messages/'.\
                      format(self.user_b.pk, self.chat.pk)

    def test_create_message(self):
        pass

    def test_create_message_no_auth(self):
        pass

    def test_create_message_on_wrong_endpoint(self):
        pass

    def test_delete_message(self):
        pass

    def test_delete_message_on_wrong_endpoint(self):
        pass

