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
        fields  = ('pk', 'feature', )


'''   Serializer for Tax Record models. '''
class TaxRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model   = TaxRecords
        fields  = ('pk', 'assessment', 'assessment_year')


'''   Serializer for Historical models. '''
class HistoricalSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Historical
        fields  = ('last_sold_price', 'last_sold_date',
                   'year_built')


'''   Serializer for Images models. '''
class ImagesSerializer(serializers.ModelSerializer):
    
    image = serializers.ReadOnlyField(source='image.name')
    
    class Meta:
        model  = Images
        fields = ('pk', 'image', 'timestamp')

    ''' Create an Image object. Note, we are not handling batch creations. '''
    def create(self, validated_data):

        kproperty = validated_data.pop('kproperty')
        image_data = self.context.pop('images')[0]
        
        image = Images.objects.create(kproperty=kproperty, image=image_data)

        return image

    ''' Update an Image object. Note, we're recieving files through the context. '''
    def update(self, instance, validated_data):
        
        image = self.context.pop('images')[0]
        instance.image = image
        
        instance.save()
        return instance

