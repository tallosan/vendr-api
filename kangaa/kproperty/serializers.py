from django.contrib.auth.models import User

from rest_framework import serializers

from kproperty.models import *


#TODO: Refactor this. Move these secondary serializers elsewhere.
## Secondary.
'''   Serializer for Location models. '''
class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Location
        fields  = ('country', 'province', 'city',
                   'address', 'postal_code',
                   'longitude', 'latitude')

        
class TaxRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model   = TaxRecord
        fields  = ('assessment', 'assessment_year')


class HistoricalSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Historical
        fields  = ('last_sold_price', 'last_sold_date',
                   'year_built')
        
## Main.
'''   Serializer for Property models. '''
class PropertySerializer(serializers.ModelSerializer):

    owner       = serializers.ReadOnlyField(source='owner.username')
    
    # Primary fields.
    location    = LocationSerializer()

    # Secondary fields.
    tax_records = TaxRecordSerializer()
    history     = HistoricalSerializer()
    
    class Meta:
        model   = Property
        fields  = ('id', 'owner',
                   'price',
                   'sqr_ftg',
                   'n_bedrooms', 'n_bathrooms',
                   'location',
                   'tax_records',
                   'history')

    ''' Handles the creation of a Property object.
        N.B. -- It is up to the child classes to pass the correct property class
                to this function.
        Args:
            property_class: The class of property we are creating (e.g. House).
            validated_data: The request data we create the new model from.
    '''
    def create(self, property_class, validated_data):

        # We need to explicitly declare these nested fields so we can create
        # them later on.
        nested_keys = {
                        'location': Location(),
                        'tax_records': TaxRecord(),
                        'history': Historical()
        }

        # Go through the validated data, and create the nested objects using
        # the given data. We then set the respective fields for our property object.
        kproperty = property_class
        for key in validated_data.keys():
            if key in nested_keys.keys():
                nested_data    = validated_data.pop(key)
                instance_class = nested_keys[key].__class__
                instance = instance_class.objects.create(**nested_data)
                setattr(kproperty, key, instance)

        # Now we pass through the regular (non-nested) field data.
        setattr(kproperty, 'kwargs', validated_data)
        for k, v in validated_data.iteritems():
            setattr(kproperty, k, v)
        
        kproperty.save()
        return kproperty
 
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
            
            # Nested object.
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

    ''' Overrides parent by passing a Condo model as the 'property_class'. '''
    def create(self, validated_data):

        return super(CondoSerializer, self).create(Condo(), validated_data)


'''   Serializer for House models. '''
class HouseSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):

        model = House
   
    ''' Overrides parent by passing a House model as the 'property_class'. '''
    def create(self, validated_data):

        return super(HouseSerializer, self).create(House(), validated_data)

