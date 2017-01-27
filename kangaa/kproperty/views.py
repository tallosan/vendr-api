from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from kproperty.models import *
from kproperty.serializers import *


'''   Lists all properties. '''
class PropertyList(APIView):
        
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

        # Determine the serializer type, as specified by the '?model' param.
        if request.GET.get('model') == 'condo':
            serializer = CondoSerializer(data=request.data)
        elif request.GET.get('model') == 'house':
            serializer = HouseSerializer(data=request.data)
        else:
            raise Http404("Invalid model.")
        
        # Save the valid serializer along with data about the user who created it.
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Lists an individual property's (identified by primary key) details. '''
class PropertyDetail(APIView):

    def __init__(self):
        
        self.serializer = None

    ''' Retrieve the property if it exists. Returns a 404 otherwise.
        Args:
            pk: The primary key of the property.
    '''
    def get_object(self, pk):

        # Get the object in question, and its serializer.
        try:
            target = Property.objects.get_subclass(pk=pk)
            self.serializer = target.get_serializer()
            return target
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

        kproperty       = self.get_object(pk)
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

