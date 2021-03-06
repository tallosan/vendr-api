from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import Http404
from django.conf import settings

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from kuser.serializers import UserReadSerializer, UserCreateUpdateSerializer
from kuser.permissions import IsOwnerOrReadOnly

User = get_user_model()


'''   User list view. '''
class UserList(APIView):

    queryset           = User.objects.all()
    read_serializer    = UserReadSerializer
    create_serializer  = UserCreateUpdateSerializer
    permission_classes = (
                            permissions.AllowAny,
    )

    ''' Get a list of users. '''
    def get(self, request, format=None):
        
        serializer_class = self.read_serializer

        # Paginate the queryset if necessary.
        response = []
        for user in self.get_queryset():
            response.append(serializer_class(user, context={'request': request}).data)

        return Response(response)
    
    ''' Create a new User if their username and email are valid. '''
    def post(self, request, format=None):
        
        # Determine if the email is available.
        email = request.data.get('email')
        if not self.is_available(email):
            error_msg = {'error': 'user with email ' + str(email) + ' already exists.'}
            user_exists_exc = APIException(detail=error_msg)
            user_exists_exc.status_code = status.HTTP_400_BAD_REQUEST
            raise user_exists_exc

        serializer_class = self.create_serializer
        serializer = serializer_class(data=request.data, context=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ''' Determines if the username and email of the new registration is
        available.
        Args:
            username: The desired username for the new user.
            email: The desired email for the new user.
    '''
    def is_available(self, email):
        return User.objects.filter(email=email).count() == 0


'''   User detail view. '''
class UserDetail(APIView):

    queryset           = User.objects.all()
    serializer_class   = UserReadSerializer
    update_serializer  = UserCreateUpdateSerializer
    permission_classes = (
                            permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,
    )

    ''' Retrieve the user if s/he exists.
        Args:
            pk: The primary key (id) of the target user.
    '''
    def get_object(self, pk):

        try:
            kuser = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, kuser)
            return kuser
        except User.DoesNotExist:
            user_dne_exc = APIException(detail={'error': 'user with id ' + str(pk) +\
                                ' does not exist.'})
            user_dne_exc.status_code = status.HTTP_400_BAD_REQUEST
            raise user_dne_exc

    ''' Returns the user details. Note, only the user can see their personal info. 
        Args:
            request: Handler for request field.
            pk: The primary key of the target user.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, pk, format=None):

        kuser = self.get_object(pk=pk)
        serializer = self.serializer_class(kuser)

        return Response(serializer.data)
    
    ''' Updates the user.
        Args:
            request: The updated data.
            pk: The primary key of the user to be updated.
            *format: Specified data format (e.g. JSON).
    '''
    def put(self, request, pk, format=None):
        
        kuser = self.get_object(pk=pk)
        serializer = self.update_serializer(kuser, data=request.data,
                        context=request.FILES, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ''' Deletes a user from the database.
        Args:
            request: Handler for the request field.
            pk: The primary key of the user to be deleted.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, pk, format=None):

        kuser = self.get_object(pk)
        kuser.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

