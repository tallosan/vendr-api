#
#
#
# ======================================================================

from django.db import IntegrityError
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status, permissions

from kproperty.models import Property, OpenHouse, RSVP
from kproperty.serializers import OpenHouseSerializer, RSVPSerializer
from kproperty.signals.dispatch import openhouse_create_signal, \
        openhouse_change_signal, openhouse_cancel_signal, \
        openhouse_start_signal
import kproperty.permissions as kproperty_permissions


class OpenHouseList(APIView):
    
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer
    permission_classes = ( kproperty_permissions.OpenHouseListPermissions, )

    ''' Gets all Open Houses that a given user has created.
        Args:
            pk -- The primary key of the user we're querying over.
    '''
    def get_queryset(self, pk):

        queryset = Property.objects.get(pk=pk).open_houses.all()
        return queryset

    ''' Handles LIST / GET requests.
        Args:
            request: The GET request.
            pk: The primary key of the user we're querying over.
            *format: Specified data format.
    '''
    def get(self, request, pk, format=None):

        queryset = self.get_queryset(pk)
        response = []
        for open_house in queryset:
            response.append(self.serializer_class(open_house).data)

        return Response(response)

    ''' Handles POST requests.
        Args:
            request: The POST request.
            pk: The primary key of the user we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, pk, format=None):
        
        kproperty = Property.objects.get(pk=pk)
        self.check_object_permissions(request, kproperty)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            open_house = serializer.save(
                    owner=self.request.user,
                    kproperty=kproperty
            )

            # Get the open house's URL resource, and send a change signal.
            resource = '{}listings/{}/open-houses/{}/'.format(
                    settings.BASE_WEB_URL,
                    open_house.kproperty.pk,
                    open_house.pk
            )
            openhouse_create_signal.send(sender=open_house, resource=resource)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpenHouseDetail(APIView):
    
    queryset = OpenHouse.objects.all()
    serializer_class = OpenHouseSerializer
    permission_classes = ( kproperty_permissions.OpenHouseDetailPermissions, )

    ''' Return the Open House object with the given pk. Raises an exception if
        none exists.
        Args:
            oh_pk -- The open house object's primary key.
    '''
    def get_object(self, oh_pk):

        try:
            open_house = OpenHouse.objects.get(pk=oh_pk)
            self.check_object_permissions(self.request, open_house)
            return open_house

        except OpenHouse.DoesNotExist:
            error_msg = {'error': 'open house with id=' + str(oh_pk) + ' does not exist.'}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = status.HTTP_400_BAD_REQUEST
            raise dne_exc
    
    ''' Handles GET requests on Open House models.
        Args:
            request: The GET request.
            pk: The user that the open house belongs to.
            oh_pk: The primary key of the open house to get.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, pk, oh_pk, format=None):

        open_house = self.get_object(oh_pk)
        serializer = self.serializer_class(open_house)
        
        return Response(serializer.data)
 
    ''' Handles PUT requests on Open House models.
        Args:
            request: The GET request.
            pk: The user that the open house belongs to.
            oh_pk: The primary key of the open house to update.
            *format: Specified data format (e.g. JSON).
    '''
    def put(self, request, pk, oh_pk, format=None):

        open_house = self.get_object(oh_pk)
 
        serializer = self.serializer_class(open_house, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Get the open house's URL resource, and send a change signal.
            resource = '{}listings/{}/open-houses/{}/'.format(
                    settings.BASE_WEB_URL,
                    open_house.kproperty.pk,
                    open_house.pk
            )
            openhouse_change_signal.send(sender=open_house, resource=resource)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ''' Handles DELETE requests on Open House models.
        Args:
            request: The GET request.
            pk: The user that the open house belongs to.
            oh_pk: The primary key of the open house to delete.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, pk, oh_pk, format=None):

        open_house = self.get_object(oh_pk)
    
        # Get the open house's URL resource, and send a change signal.
        resource = '{}listings/{}/open-houses/'.format(
                settings.BASE_WEB_URL,
                open_house.kproperty.pk,
        )
        openhouse_cancel_signal.send(sender=open_house, resource=resource)
        open_house.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RSVPList(APIView):

    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = ( permissions.IsAuthenticated, 
                           kproperty_permissions.RSVPListPermissions
    )

    ''' Gets all RSVPs to a given Open House.
        Args:
            oh_pk -- The primary key of the open house we're querying over.
    '''
    def get_queryset(self, oh_pk):

        queryset = OpenHouse.objects.get(pk=oh_pk).rsvp_list.all()
        return queryset
    
    ''' Handles LIST / GET requests.
        Args:
            request: The GET request.
            pk: The primary key of the user we're querying over.
            oh_pk: The primary key of the open house we're querying over.
            *format: Specified data format.
    '''
    def get(self, request, pk, oh_pk, format=None):

        self.check_object_permissions(self.request,
                OpenHouse.objects.get(pk=oh_pk))
        queryset = self.get_queryset(oh_pk)
        
        response = []
        for rsvp in queryset:
            response.append(self.serializer_class(rsvp).data)

        return Response(response)

    ''' Handles POST requests.
        Args:
            request: The POST request.
            pk: The primary key of the user we're querying over.
            oh_pk: The primary key of the open house we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, pk, oh_pk, format=None):

        open_house = OpenHouse.objects.get(pk=oh_pk)
        self.check_object_permissions(self.request, open_house)

        # Create the RSVP if it is now a duplicate.
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(owner=request.user, open_house=open_house)
            except IntegrityError:
                return Response({'error': 'cannot have duplicate'}, status=400)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RSVPDetail(APIView):

    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = ( permissions.IsAuthenticated,
                           kproperty_permissions.RSVPDetailPermissions
    )

    ''' Return the RSVP object with the given pk. Raises an exception if
        none exists.
        Args:
            rsvp_pk -- The RSVP object's primary key.
    '''
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

    ''' Handles GET requests on RSVP models.
        Args:
            request: The GET request.
            pk: The user that the open house belongs to.
            oh_pk: The primary key of the open house we're querying over.
            rsvp_pk: The primary key of the RSVP we're getting.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, pk, oh_pk, rsvp_pk, format=None):

        rsvp = self.get_object(rsvp_pk)
        serializer = self.serializer_class(rsvp)

        return Response(serializer.data)
   
    ''' Handles DELETE requests on RSVP models.
        Args:
            request: The GET request.
            pk: The user that the open house belongs to.
            oh_pk: The primary key of the open house we're querying over.
            rsvp_pk: The primary key of the RSVP we're deleting
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, pk, oh_pk, rsvp_pk, format=None):

        rsvp = self.get_object(rsvp_pk)
        rsvp.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

