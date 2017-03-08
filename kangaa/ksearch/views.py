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
    
    request.GET._mutable = True
    search_type = request.GET.pop('type')[0]
    
    # We can return either search for properties, or users. Anything else
    # will raise a 404.
    if search_type == 'property':
        return PropertySearch.as_view()(request)
    
    elif search_type == 'user':
        return UserSearch.as_view()(request)

    else:
        raise Http404('Invalid search type.')


''' Seach view for all Property models. '''
class PropertySearch(generics.ListAPIView):

    ''' Filters the queryset according to the specified parameters. '''
    def get_queryset(self):
        
        filters = self.request.GET
        #ptypes = filters['ptype']
        
        # Construct the filter chain. We have both multi-value, and single-value cases.
        # If our data is in a list, we assume it's multi-value. If not, single.
        filter_args = {}
        for kfilter in filters.keys():
            if (filters[kfilter][0] == '[') and (filters[kfilter][-1] == ']'):
                next_filter = self.parse_multikey(filters[kfilter])
            else:
                next_filter = filters[kfilter]
            
            filter_args[kfilter] = next_filter
        
        # Build the query set by querying each Property model in the database.
        queryset = []
        for subclass in Property.__subclasses__():
            try:
                queryset += subclass.objects.filter(**filter_args)
            except FieldError:
                pass
        
        return queryset

    ''' (Helper Function) Parses a multi-key value into something we can pass
        through a Django filter.
        Args:
            multi_value: The multi-value key, contained in a list (e.g. [..., ...])
    '''
    def parse_multikey(self, multi_value):
        
        multi_value = [
                            q.strip('[').strip(']').lstrip(' ')
                            for q in multi_value.encode('utf8').split(',')
                      ]
        
        return multi_value
    
    ''' Overrides the default 'list()' method. Serializes each object according
        to their type. '''
    def list(self, request):
        
        queryset = self.get_queryset()
        
        # Construct our response by serializing each object in the queryset.
        response = []
        for kproperty in queryset:
            serializer = kproperty.get_serializer()
            response.append(serializer(kproperty).data)
        
        return Response(response)


'''   Search view for User objects. '''
class UserSearch(generics.ListAPIView):

    serializer_class = UserSerializer
    
    ''' Filters the queryset according to the specified parameters. '''
    def get_queryset(self):
        
        filter_args = {}
        
        # Construct the filter chain.
        #TODO: Sanitize input.
        filters = self.request.GET
        for kfilter in filters.keys():
            filter_args[kfilter] = filters[kfilter]
                
        queryset = User.objects.filter(**filter_args)
        
        return queryset

