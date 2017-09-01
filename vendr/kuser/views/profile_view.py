#
# User schedule.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import permissions

from vendr_core.generics import NestedListAPIView, NestedUpdateAPIView
from vendr_core.permissions import IsOwner

from kuser.serializers import ProfileSerializer
from kuser.models import Profile

User = get_user_model()


class ProfileDetail(NestedListAPIView, NestedUpdateAPIView):

    parent = User
    parent_field_name = 'kuser'
    field_name = 'profile'
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

    """ We're going to make a slight modification here, as we only have one
        Profile object / User. Thus, it makes sense to pop the one Profile out
        of the queryset list so that it's easier to work with. """
    def get(self, request, *args, **kwargs):

        response = super(ProfileDetail, self).get(request, *args, **kwargs)
        return Response(response.data[0])

