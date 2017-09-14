from rest_framework import serializers

from django.core.files.uploadedfile import UploadedFile

from kproperty.models import *
from .property_field_serializers import *
from .open_house_serializers import RSVPSerializer, OpenHouseSerializer


'''   Serializer for Property models. '''
class PropertySerializer(serializers.ModelSerializer):

    owner       = serializers.ReadOnlyField(source='owner.id')
    
    # Primary fields.
    location    = LocationSerializer()

    # Secondary fields.
    features    = FeaturesSerializer(Features.objects.all(), many=True,
                    ignore_unused_fields=True)
    tax_records = TaxRecordsSerializer(TaxRecords.objects.all(), many=True,
                    ignore_unused_fields=True)
    history     = HistoricalSerializer()
    images      = ImagesSerializer(Images.objects.all(), many=True,
                    ignore_unused_fields=True)
    open_houses = OpenHouseSerializer(OpenHouse.objects.all(), many=True,
                    required=False, ignore_unused_fields=True)

    class Meta:
        model   = Property
        fields  = ('id', 'owner',
                   'price',
                   'sqr_ftg',
                   'n_bedrooms', 'n_bathrooms',
                   'location',
                   'features',
                   'tax_records',
                   'history',
                   'images',
                   'open_houses',
                   '_type',
                   'description',
                   'created_time',
                   'is_featured',
                   'display_pic',
                   'views',
                   'offers')

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
        foreign_keys = {
                        'location': Location(),
                        'tax_records': TaxRecords(),
                        'history': Historical(),
                        'features': Features(),
                        'images': Images()
        }
        
        # Go through the validated data, and pop any foreign key data. We can't
        # create these models before our Property model, so this is all we can
        # do for now.
        foreign_key_buf = {}
        for key in validated_data.keys():
            if key in foreign_keys.keys():
                foreign_key_buf[key] = (foreign_keys[key], validated_data.pop(key))
        
        # Create the Property model using non-FK data (e.g. n_bedrooms).
        kproperty = property_class.objects.create(**validated_data)
        
        # Now we can create our foreign keys models, using our fk buffer.
        for fkey in foreign_key_buf.keys():
            fkey_class = foreign_key_buf[fkey][0].__class__
            data       = foreign_key_buf[fkey][1]
            
            # Create a one-to-one model [e.g Location].
            if issubclass(data.__class__, dict):
                fkey_class.objects.create(kproperty=kproperty, **data)
            
            # Create multiple foreign key models [e.g Feature set].
            elif issubclass(data.__class__, list):
                for ins_data in data:
                    fkey_class.objects.create(kproperty=kproperty, **ins_data)

        kproperty.save()
        return kproperty
 
    ''' Update all target fields. Can handle nested objects.
        Args:
            instance: The actual object to be updated.
            validated_data: Fields to be updated, and their updates.
    '''
    def update(self, instance, validated_data):
        
        validated_data = self.adapt_context(validated_data)
        
        # For each term, perform the necessary updates on the target field.
        # Special cases exist for nested objects & foreign key objects.
        for term in validated_data.keys():
            target_data = validated_data.pop(term)
            target      = getattr(instance, term)
            
            # Unique Foreign Key model (i.e. one-to-one relation).
            if issubclass(target_data.__class__, dict):
                for field in target_data.keys():
                    setattr(target, field, target_data[field])
                
                target.save()
            
            # Nested Foreign Key models (i.e. one-to-many relation).
            # If we're given an empty list, we assume that the foreign keys should
            # be deleted. Otherwise, check if the foreign key already exists. If
            # not, then we can create it.
            elif issubclass(target_data.__class__, list):
                if len(target_data) == 0:
                    target.all().delete()
                else:
                    for data in target_data:    # TODO: Refactor.
                        model_class = target.all().model
                        if issubclass(data.__class__, UploadedFile):
                            model_class.objects.create(kproperty=instance, image=data)
                        else:
                            if target.filter(**data).count() == 0:
                                model_class.objects.create(kproperty=instance, **data)
            
            # Regular field update.
            else:
                setattr(instance, term, target_data)
            
            instance.save()
        
        return instance
        
    # TODO: Refactor this!
    def adapt_context(self, validated_data):
        for key in self.context.keys():
            validated_data[key] = self.context.pop(key)
        
        return validated_data


'''   Serializer for cooperative living properties. '''
class CoOpSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):

        fields = PropertySerializer.Meta.fields + ('unit_num', 'parking_spaces',
                    'corporation_name')

'''   Serializer for Condo models. '''
class CondoSerializer(CoOpSerializer):

    class Meta(CoOpSerializer.Meta):
        model = Condo

    ''' Overrides parent by passing a Condo model as the 'property_class'. '''
    def create(self, validated_data):

        return super(CondoSerializer, self).create(Condo().__class__, validated_data)


'''   Serializer for freehold properties. '''
class FreeholdSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields


'''   Serializer for House models. '''
class HouseSerializer(FreeholdSerializer):

    class Meta(PropertySerializer.Meta):
        model  = House
        fields = FreeholdSerializer.Meta.fields
   
    ''' Overrides parent by passing a House model as the 'property_class'. '''
    def create(self, validated_data):

        return super(HouseSerializer, self).create(House().__class__, validated_data)


'''   Serializer for Townhouse models. '''
class TownhouseSerializer(FreeholdSerializer):

    class Meta(FreeholdSerializer.Meta):
        model  = Townhouse
        fields = FreeholdSerializer.Meta.fields + ('degree', )

    ''' Overrides parent by passing a House model as the 'property_class'. '''
    def create(self, validated_data):

        return super(TownhouseSerializer, self).create(Townhouse().__class__, validated_data)


'''   Serializer for Manufactured properties. '''
class ManufacturedSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):
        model  = Manufactured
        fields = PropertySerializer.Meta.fields + ('manufacturer', 'serial',
                    'year', 'length', 'width', 'mobile_park')


'''   Serializer for Vacant Land properties. '''
class VacantLandSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):
        model  = VacantLand
        fields = PropertySerializer.Meta.fields

