from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from kproperty.models import *
from kproperty.serializers import *
from kproperty.permissions import IsOwnerOrReadOnly


'''   Lists all properties. '''
class PropertyList(APIView):

    permission_classes = (
                            permissions.IsAuthenticatedOrReadOnly,
    )

    ''' Returns all properties in the database.
        Args:
            request: Handler for request field.
            *format: Specified data format.
    '''
    def get(self, request, format=None):
        
        response = []
        for kproperty in Property.objects.select_subclasses():
            serializer = kproperty.get_serializer()
            response.append(serializer(kproperty).data)

        return Response(response)

    ''' Places objects in the database.
        Args:
            request: Properties to create.
            *format: Specified data format.
    '''
    def post(self, request, format=None):

        # Determine the serializer type, as specified by the '?ptype' param.
        try:
            serializer_type = self.resolve_serializer(request.GET.get('ptype'))
            serializer = serializer_type(data=request.data)
        except KeyError as key_error:
            raise Http404('error: invalid property type.')

        # Save the valid serializer along with data about the user who created it.
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ''' Takes in the 'ptype' parameter, and returns the appropriate serializer.
        Args:
            type: The property type paramter (e.g. condo).
    '''
    def resolve_serializer(self, ptype):

        types = {
                    'condo': CondoSerializer,
                    'house': HouseSerializer,
                    'multiplex': MultiplexSerializer
                }

        return types[ptype]


'''   Lists an individual property's (identified by primary key) details. '''
class PropertyDetail(APIView):

    def __init__(self):
        
        self.serializer         = None
        self.permission_classes = (
                                    permissions.IsAuthenticatedOrReadOnly,
                                    IsOwnerOrReadOnly,
        )

    ''' Retrieve the property if it exists. Returns a 404 otherwise.
        Args:
            request: Property data. Necessary for the permissions check.
    '''
    def get_object(self, pk):

        # Get the object in question, and its serializer.
        try:
            kproperty = Property.objects.get_subclass(pk=pk)
            self.check_object_permissions(self.request, kproperty)
            self.serializer = kproperty.get_serializer()
            return kproperty
        except Property.DoesNotExist:
            raise Http404
    
    ''' Returns the property details.
        Args:
            request: Handler for request field.
            pk: The primary key of the property.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, pk, format=None):
        
        kproperty       = self.get_object(pk)
        self.serializer = self.serializer(kproperty)
        
        return Response(self.serializer.data)
    
    ''' Puts an property in the database.
        Args:
            request: Property data.
            pk: The primary key of the property.
            *format: Specified data format (e.g. JSON).
    '''
    def put(self, request, pk, format=None):

        kproperty = self.get_object(pk)
        self.serializer = self.serializer(kproperty, data=request.data, partial=True)
        if self.serializer.is_valid():
            self.serializer.save()
            return Response(self.serializer.data)
        
        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    ''' Deletes a property from the database.
        Args:
            request: Handler for request field.
            pk: The primary key of the property.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, pk, format=None):

        kproperty = self.get_object(pk)
        kproperty.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

