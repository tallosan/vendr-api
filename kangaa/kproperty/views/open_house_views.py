#
#
#
# ======================================================================

from rest_framework import generics

from kproperty.models import OpenHouse, RSVP
from kproperty.serializers import OpenHouseSerializer, RSVPSerializer
import kproperty.permissions as kproperty_permissions


class OpenHouseList(generics.ListCreateAPIView):
    
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer
    permission_classes = ( kproperty_permissions.OpenHouseListPermissions, )

    #TODO: Override get_queryset()


class OpenHouseDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer
    permission_classes = ( kproperty_permissions.OpenHouseDetailPermissions, )

    #TODO: Override get_object()

class RSVPList(generics.CreateAPIView):

    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = ( kproperty_permissions.RSVPListPermissions, )
    
    #TODO: Override get_queryset()


class RSVPDetail(generics.RetrieveDestroyAPIView):

    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = ( kproperty_permissions.RSVPDetailPermissions, )

    #TODO: Override get_object()

