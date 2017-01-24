from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import generics

from kuser.serializers import *


'''   User list view. '''
class UserList(generics.ListAPIView):

    queryset         = User.objects.all()
    serializer_class = UserSerializer


'''   User detail view. '''
class UserDetail(generics.RetrieveAPIView):

    queryset         = User.objects.all()
    serializer_class = UserSerializer

