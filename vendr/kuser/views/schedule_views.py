#
# User schedule.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework import permissions

from vendr_core.generics import NestedListAPIView
from vendr_core.permissions import IsOwner

from kuser.serializers import ScheduleSerializer
from kproperty.models import RSVP
from kproperty.permissions import RSVPDetailPermissions

User = get_user_model()


class ScheduleList(NestedListAPIView):
    
    parent = User
    parent_field_name = 'user'
    field_name = 'rsvp_schedule'
    
    queryset = RSVP.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

    def get(self, request, *args, **kwargs):

        self.check_object_permissions(request, request.user)
        return super(ScheduleList, self).get(request, *args, **kwargs)

