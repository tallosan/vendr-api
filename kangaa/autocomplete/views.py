from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import FieldError

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

import json

from kproperty.models import *


''' Handles search requests by routing to the appropriate view depending
    on the 'type' specified.
    Args:
        request: HttpResponse object containing 'type' parameter.
'''
def search_router(request):
    
    if request.GET.get('type') == 'location':

        return LocationSearch.as_view()(request)

    else:
        raise Http404('Invalid search type.')


'''   Autocomplete for Locations. '''
class LocationSearch(generics.ListAPIView):

    ''' Filters the queryset according to the specified paramters. '''
    def get_queryset(self):
        
        term = self.request.GET.get('term')
        if not term:
            raise Http404('Term must be specified.')

        queryset = Location.objects.filter(city__istartswith=term).distinct('city')
        return queryset

    ''' Custom list method. Retrieves the queryset of Location models and
        serializes each entry as a dictionary containing the city name, and the
        number of properties in the database (count) in that city. '''
    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        # Get the city name and overall count for each city.
        data = { 'cities': [] }
        for location in queryset:
            count = Property.objects.filter(location__city=location.city).count()
            city = {
                        'city': location.city,
                        'count': count
            }
            data['cities'].append(city)

        # Sort results by count.
        data['cities'] = sorted(data['cities'], key=lambda k: k['count'], reverse=True)

        return Response(data)

