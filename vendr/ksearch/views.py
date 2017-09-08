#
# View for searching Property and User models.
#
# ==========================================================================

from operator import and_

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import FieldError
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.gis.geos import Polygon

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.settings import api_settings

import kproperty.models
from kproperty.models import *
from kproperty.serializers import *
from kuser.serializers import *

User = get_user_model()


''' Handles search requests by routing to the appropriate view depending
    on the 'type' specified.
    Args:
        request: HttpResponse object containing 'type' parameter.
'''
@api_view(['GET'])
def search_router(request):
    
    request.GET._mutable = True
    
    # Get the search type (assuming one is specified).
    try:
        search_type = request.GET.pop('stype')[0]
    except KeyError:
        error_msg = {'error': "'stype' (search type) must be specified."}
        return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
    
    # We can return either search for properties, or users. Anything else
    # will raise a 400.
    if search_type == 'property':
        return PropertySearch.as_view()(request)
    
    elif search_type == 'user':
        return UserSearch.as_view()(request)

    else:
        return Response(data={'error': 'invalid search type.'},
                        status=status.HTTP_400_BAD_REQUEST)


''' Seach view for all Property models. '''
class PropertySearch(generics.ListAPIView):

    # We're using Limit Offset pagination by default, but this gives us a bit
    # of flexibility if, for some inexplicable reason, we decide to use a different
    # pagination scheme.
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    
    ''' Overrides the default 'list()' method. We have a number of different model
        types, and a number of different (optional) filters.
        The first step is to parse the pagination parameters (if any) because we
        don't want to mix them up with the Property filter parameters. Once this is
        taken care of, we can construct our queryset. We then apply our paginator
        to its results and return the serialized response.
        Args:
            request (OrderedDict) -- The GET request.
    '''
    def list(self, request):
        
        # Parse the pagination parameters (if any).
        paginator = self.get_paginator(request)

        # Get the queryset, and apply pagination if applicable.
        queryset = self.get_queryset()
        if paginator:
            request.GET['limit'] = paginator.limit
            request.GET['offset'] = paginator.offset
            queryset = paginator.paginate_queryset(queryset, request, self)
        
        # Serialize queryset.
        response = []
        for kproperty in queryset:
            serializer = kproperty.get_serializer()
            response.append(serializer(kproperty).data)
        
        return Response(response)
    
    ''' Handle pagination, if any pagination parameters are passed in. If the
        appropriate params are present and valid, then we'll return an instance
        of our pagination class (we're using Limit Offset Pagination). Otherwise,
        we'll return None.
        Args:
            request (OrderedDict) -- The GET request.
    '''
    def get_paginator(self, request):
        
        try:
            limit, offset = request.GET.pop('limit')[0], request.GET.pop('offset')[0]
            if (int(limit) <= 0) or (int(offset) < 0):
                exc = APIException(detail={
                    'error': 'pagination params cannot be negative.'
                })
                exc.status_code = 401; raise exc
            
            paginator = self.pagination_class()
            paginator.limit = limit; paginator.offset = offset
            return paginator
        except KeyError:
            return None
 
    ''' Filters the queryset according to the specified parameters. '''
    def get_queryset(self):
        
        queryset = Property.objects.select_subclasses()

        # Construct a filter chain from the given parameters.
        filter_args = self.generate_filter_chain(self.request.GET)
        if filter_args:
            queryset = queryset.filter(reduce(and_, filter_args))

        return queryset
 
    ''' (Helper Function) Parses a set of filters and generate a filter
        chain of Q objects from them.
        Args:
            filters (dict) -- A dictionary of filter type-filter value, parameters.
    '''
    def generate_filter_chain(self, filters):

        filter_args = []
        
        # Parse any map filters.
        map_filters = {}; map_coordinates = ['ne_lng', 'ne_lat', 'sw_lng', 'sw_lat']
        if any(map_filter in filters.keys() for map_filter in map_coordinates):
            if not all(map_filter in filters.keys() for map_filter in map_coordinates):
                exc = APIException(detail={'error': 'incomplete map query.'})
                exc.status_code = 401; raise exc
        
            for coordinate in map_coordinates:
                map_filters[coordinate] = filters.pop(coordinate)[0]
            
            filter_args.append(self.parse_mapkeys(map_filters))
        
        # Construct the filter chain.
        for kfilter in filters.keys():
            next_filter = Q((kfilter, filters[kfilter]))
            filter_args.append(next_filter)

        return filter_args

    ''' Create and return a bounding box, given a set of coordinate pairs.
        Args:
            map_keys (dict) -- Map coordinates for the north east and south west.
    '''
    def parse_mapkeys(self, map_keys):

        # Create a bounding box from the given longitude & latitude.
        lng = (float(map_keys['ne_lng']), float(map_keys['sw_lng']))
        lat = (float(map_keys['ne_lat']), float(map_keys['sw_lat']))
        box = Polygon.from_bbox((min(lng), min(lat), max(lng), max(lat)))
        
        return Q(location__geo_point__intersects=box)


'''   Search view for User objects. '''
class UserSearch(generics.ListAPIView):

    serializer_class = UserSerializer
    
    ''' Filters the queryset according to the specified parameters. '''
    def get_queryset(self):
        
        filter_args = {}
        
        # Construct the filter chain.
        filters = self.request.GET
        for kfilter in filters.keys():
            filter_args[kfilter] = filters[kfilter]
                
        queryset = User.objects.filter(**filter_args)
        
        return queryset

