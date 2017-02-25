#
#   Serializers for nested models.
#

from django.contrib.auth.models import User

from rest_framework import serializers

from kproperty.models import *


'''   Serializer for Location models. '''
class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Location
        fields  = ('country', 'province', 'city',
                   'address', 'postal_code',
                   'longitude', 'latitude')


'''   Serializer for Feature models. '''
class FeaturesSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Features
        fields  = ('feature', )


'''   Serializer for Tax Record models. '''
class TaxRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model   = TaxRecord
        fields  = ('assessment', 'assessment_year')


'''   Serializer for Historical models. '''
class HistoricalSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Historical
        fields  = ('last_sold_price', 'last_sold_date',
                   'year_built')

'''   Serializer for Images models. '''
class ImagesSerializer(serializers.ModelSerializer):
    
    thumbnail           = serializers.ImageField(use_url=True, required=False)
    low_resolution      = serializers.ImageField(use_url=True, required=False)
    standard_resolution = serializers.ImageField(use_url=True, required=False)
    
    class Meta:
        model   = Images
        fields  = ('thumbnail',
                   'low_resolution', 'standard_resolution')

