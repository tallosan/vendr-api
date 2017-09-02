#
# User schedule.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import permissions

from vendr_core.generics import NestedListUpdateAPIView
from vendr_core.permissions import IsOwner

from kuser.serializers import ProfileSerializer
from kuser.models import Profile

User = get_user_model()


class ProfileDetail(NestedListUpdateAPIView):

    parent = User
    parent_field_name = 'kuser'
    field_name = 'profile'
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

