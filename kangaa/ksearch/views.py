from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import FieldError

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from kproperty.models import *
from kproperty.serializers import *
from kuser.serializers import *


''' Handles search requests by routing to the appropriate view depending
    on the 'type' specified.
    Args:
        request: HttpResponse object containing 'type' parameter.
'''
def search_router(request):
    
    # We can return either search for properties, or users. Anything else
    # will raise a 404.
    if request.GET.get('type') == 'property':

        return PropertySearch.as_view()(request)
    
    elif request.GET.get('type') == 'user':
        
        return UserSearch.as_view()(request)

    else:
        raise Http404('Invalid search type.')


''' Seach view for all Property models. '''
class PropertySearch(generics.ListAPIView):

    #TODO: Add sorting feature.
    #TODO: Find users by username, not ID.
    ''' Filters the queryset according to the specified parameters. '''
    def get_queryset(self):
        
        filter_args = {}
        
        # Construct the filter chain.
        filters = self.request.GET
        for kfilter in filters.keys():
            if kfilter != 'type':
                filter_args[kfilter] = filters[kfilter]
        
        # Build the query set by querying each Property model in the database.
        queryset = []
        for subclass in Property.__subclasses__():
            try:
                queryset += subclass.objects.filter(**filter_args)
            except FieldError:
                pass
        
        return queryset

    ''' Overrides the default 'list()' method. Serializes each object according
        to their type. '''
    def list(self, request):
        
        queryset = self.get_queryset()
        
        # Divide the property objects accordingly.
        condos, houses = [], []
        for kproperty in queryset:
            if type(kproperty) == Condo:
                condos.append(kproperty)

            elif type(kproperty) == House:
                houses.append(kproperty)

        # Now serialize using the appropriate serializer, and return.
        condo_serializer = CondoSerializer(condos, many=True)
        house_serializer = HouseSerializer(houses, many=True)
        
        response = condo_serializer.data + house_serializer.data
        
        return Response(response)


'''   Search view for User objects. '''
class UserSearch(generics.ListAPIView):

    serializer_class = UserSerializer
    
    #TODO: Add sorting feature.
    ''' Filters the queryset according to the specified parameters. '''
    def get_queryset(self):
        
        filter_args = {}
        
        # Construct the filter chain.
        #TODO: Sanitize input.
        filters = self.request.GET
        for kfilter in filters.keys():
            if kfilter != 'type':
                filter_args[kfilter] = filters[kfilter]
                
        queryset = User.objects.filter(**filter_args)
        
        return queryset

