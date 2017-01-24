from django.contrib.auth.models import User

from rest_framework import serializers

from kproperty.models import *


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Location
        fields  = ('country', 'province', 'city',
                   'address', 'postal_code',
                   'longitude', 'latitude')


'''   Serializer for Property models. '''
class PropertySerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    location = LocationSerializer()
    
    class Meta:
        model   = Property
        fields  = ('id', 'owner',
                   'location',
                   'price',
                   'sqr_ftg',
                   'n_bedrooms', 'n_bathrooms')

    ''' Update all target fields. Can handle nested objects.
        Args:
            instance: The actual object to be updated.
            validated_data: Fields to be updated, and their updates.
    '''
    def update(self, instance, validated_data):
        
        import collections    # Used for model update check.
        
        # For each term, perform the necessary updates on the target field.
        # Special case here is for nested object updates.
        for term in validated_data.keys():
            target_data = validated_data.pop(term)
            target = getattr(instance, term)
            if type(target_data) == collections.OrderedDict:
                for field in target_data.keys():
                    setattr(target, field, target_data[field])
                target.save()
            else:
                setattr(instance, term, target_data)
            
            instance.save()

        return instance


'''   Serializer for Condo models. '''
class CondoSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):

        model   = Condo
        fields  = PropertySerializer.Meta.fields + ('floor_num', )

    #TODO: Pull this up into the parent?
    ''' Handles the creation of a Condo object.
        Args:
            validated_data: The request data we create the new model from.
    '''
    def create(self, validated_data):

        location_data   = validated_data.pop('location')
        location        = Location.objects.create(**location_data)
        condo           = Condo.objects.create(location=location, **validated_data)
        
        return condo


'''   Serializer for House models. '''
class HouseSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):

        model = House

