from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import FieldError

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

import kproperty.models
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
    try:
        search_type = request.GET.pop('stype')[0]
    except KeyError:
        raise Http404("error: 'stype' (search type) must be specified.")
    
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
        
        # Construct a filter chain from the given parameters.
        try:
            filter_args = self.gen_filter_chain(self.request.GET)
        except IndexError:
            filter_args = {}
       
        # Get the Property types arguments, if any are given.
        try:
            ptypes = filter_args.pop('ptypes')
        except KeyError:
            ptypes = []

        # Build the query set by querying each model type.
        queryset = []
        for model in self.get_models(ptypes):
            try:
                queryset += model.objects.filter(**filter_args)
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
    
    ''' (Helper Function) Parses a set of filters and generate a filter
        chain from them.
        Args:
            filters: A dictionary of filter type-filter value, parameters.
    '''
    def gen_filter_chain(self, filters):

        # Construct the filter chain. We have both multi-value, and single-value cases.
        # If our data is in a list, we assume it's multi-value. If not, single.
        filter_args = {}
        for kfilter in filters.keys():
            if (filters[kfilter][0] == '[') and (filters[kfilter][-1] == ']'):
                next_filter = self.parse_multikey(filters[kfilter])
            else:
                next_filter = filters[kfilter]
            
            filter_args[kfilter] = next_filter

        return filter_args
 
    ''' (Helper Function) Using the property types parameter, return the
        specified model subclasses.
        Args:
            ptypes: A list of strings specifying property types. 
    '''
    def get_models(self, ptypes):
        
        # Get the models.
        try:
            models = [
                        getattr(kproperty.models, model)
                        for model in ptypes
                     ]
        except AttributeError:
            raise Http404('error: invalid model type. \
                           n.b. -- this function is NOT case insensitive')
        
        # No models specified, so we'll just return all types.
        if not models:
            models = [Condo, House, Multiplex]
        
        return models

    
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

