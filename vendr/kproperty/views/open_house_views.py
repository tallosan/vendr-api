#
#
#
# ======================================================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from kproperty.models import Property, OpenHouse, RSVP
from kproperty.serializers import OpenHouseSerializer, RSVPSerializer
import kproperty.permissions as kproperty_permissions


class OpenHouseList(APIView):
    
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer
    permission_classes = ( kproperty_permissions.OpenHouseListPermissions, )

    def get_queryset(self, pk):

        queryset = Property.objects.get(pk=pk).open_houses.all()
        return queryset

    def get(self, request, pk, format=None):

        queryset = self.get_queryset(pk)
        response = []
        for open_house in queryset:
            response.append(self.serializer_class(open_house).data)

        return Response(response)

    def post(self, request, pk, format=None):
        
        kproperty = Property.objects.get(pk=pk)
        self.check_object_permissions(request, kproperty)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, kproperty=kproperty)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpenHouseDetail(APIView):
    
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer
    permission_classes = ( kproperty_permissions.OpenHouseDetailPermissions, )

    def get_object(self, oh_pk):

        try:
            open_house = OpenHouse.objects.get(pk=oh_pk)
            self.check_object_permissions(self.request, open_house)
            return open_house

        except OpenHouse.DoesNotExist:
            error_msg = {'error': 'open house with id=' + str(pk) + ' does not exist.'}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = status.HTTP_400_BAD_REQUEST
            raise dne_exc

    def get(self, request, pk, oh_pk, format=None):

        open_house = self.get_object(oh_pk)
        serializer = self.serializer_class(open_house)
        
        return Response(serializer.data)

    def put(self, request, pk, oh_pk, format=None):

        open_house = self.get_object(pk, oh_pk)
 
        serializer = self.serializer_class(open_house, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, oh_pk, format=None):

        open_house = self.get_object(pk, oh_pk)
        open_house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RSVPList(APIView):

    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = ( kproperty_permissions.RSVPListPermissions, )
 
    def get_queryset(self, oh_pk):

        open_house = OpenHouse.objects.get(pk=oh_pk)
        queryset = open_house.rsvp_list.all()
        return queryset, open_house

    def get(self, request, pk, oh_pk, format=None):

        queryset, open_house = self.get_queryset(oh_pk)
        
        self.check_object_permissions(self.request, open_house)
        response = []
        for rsvp in queryset:
            response.append(self.serializer_class(rsvp).data)

        return Response(response)

    def post(self, request, pk, oh_pk, format=None):

        open_house = OpenHouse.objects.get(pk=oh_pk)
        self.check_object_permissions(self.request, open_house)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, open_house=open_house)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RSVPDetail(APIView):

    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = ( kproperty_permissions.RSVPDetailPermissions, )

    def get_object(self, rsvp_pk):

        try:
            rsvp = RSVP.objects.get(pk=rsvp_pk)
            self.check_object_permissions(self.request, rsvp)
            return rsvp
        except RSVP.DoesNotExist:
            error_msg = {'error': 'RSVP with id=' + str(pk) + ' does not exist.'}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = status.HTTP_400_BAD_REQUEST
            raise dne_exc

    def get(self, request, pk, oh_pk, rsvp_pk, format=None):

        rsvp = self.get_object(rsvp_pk)
        serializer = self.serializer_class(rsvp)

        return Response(serializer.data)

    def put(self, request, pk, oh_pk, rsvp_pk, format=None):

        rsvp = self.get_object(rsvp_pk)
        serializer = self.serializer_class(rsvp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, oh_pk, rsvp_pk, format=None):

        rsvp = self.get_object(rsvp_pk)
        rsvp.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

