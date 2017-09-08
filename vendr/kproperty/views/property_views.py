from django.http import Http404
from django.apps import apps
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import APIException
from rest_framework.parsers import FormParser, MultiPartParser

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from kproperty.models import *
from kproperty.serializers import *
from kproperty.permissions import IsOwnerOrReadOnly


'''   Lists all properties. '''
class PropertyList(APIView):

    permission_classes = ( permissions.IsAuthenticatedOrReadOnly, )

    ''' Places objects in the database.
        Args:
            request: Properties to create.
            *format: Specified data format.
    '''
    def post(self, request, format=None):

        # Determine the serializer type, as specified by the '?ptype' param.
        try:
            ptype = request.GET.get('ptype')
            serializer_type = self.resolve_serializer(ptype.lower())
            serializer = serializer_type(data=request.data)
        except (KeyError, AttributeError) as key_error:
            key_error_exc = APIException(detail={'error': 'no property type given.'})
            key_error_exc.status_code = status.HTTP_400_BAD_REQUEST

            raise key_error_exc

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
                    'townhouse': TownhouseSerializer,
                    'manufactured': ManufacturedSerializer,
                    'vacant_land': VacantLandSerializer
                }

        return types[ptype]


'''   Lists an individual property's (identified by primary key) details. '''
class PropertyDetail(APIView):

    def __init__(self):
        
        self.serializer         = None
        self.permission_classes = (
                permissions.IsAuthenticatedOrReadOnly,
                IsOwnerOrReadOnly
        )
        self.parsers = (FormParser, MultiPartParser, )

    ''' Retrieve the property if it exists. Returns a 404 otherwise.
        Args:
            request: Property data. Necessary for the permissions check.
    '''
    def get_object(self, pk):

        # Get the object in question and its serializer. Note, we're also going
        # to increment its `views`.
        try:
            model_type = Property.objects.filter(pk=pk).values_list('_type', flat=True)
            model = apps.get_model(app_label='kproperty', model_name=model_type)
            kproperty = model.objects.get(pk=pk)
            self.check_object_permissions(self.request, kproperty)
            self.serializer = kproperty.get_serializer()
            kproperty.views += 1; kproperty.save()
            return kproperty
        except Property.DoesNotExist:
            error_msg = {'error': 'property with id=' + str(pk) + ' does not exist.'}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = status.HTTP_400_BAD_REQUEST
            
            raise dne_exc
    
    ''' Returns the property details.
        Args:
            request: Handler for request field.
            pk: The primary key of the property.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, pk, format=None):
        
        kproperty = self.get_object(pk)
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
        self.serializer = self.serializer(kproperty, data=request.data,
                            context=request.data, partial=True)
        if self.serializer.is_valid(raise_exception=True):
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

