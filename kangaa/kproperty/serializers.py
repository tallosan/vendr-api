from rest_framework import serializers

from kproperty.models import *
from kproperty.nested_serializers import *       


'''   Serializer for Property models. '''
class PropertySerializer(serializers.ModelSerializer):

    owner       = serializers.ReadOnlyField(source='owner.id')
    
    # Primary fields.
    location    = LocationSerializer()

    # Secondary fields.
    features    = FeaturesSerializer(Features.objects.all(), many=True)
    tax_records = TaxRecordsSerializer(TaxRecords.objects.all(), many=True)
    history     = HistoricalSerializer()
    images      = ImagesSerializer()
    
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
                   'created_time',
                   'is_featured')

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
            
            #TODO: Condense this into just a for-loop.
            # Create a one-to-one model [e.g Location].
            if type(data).__name__ == 'OrderedDict':
                fkey_class.objects.create(kproperty=kproperty, **data)
            
            # Create multiple foreign key models [e.g Feature set].
            elif type(data).__name__ == 'list':
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
        
        # For each term, perform the necessary updates on the target field.
        # Special cases exist for nested objects, & foreign key objects.
        for term in validated_data.keys():
            target_data = validated_data.pop(term)
            target      = getattr(instance, term)
            
            # Unique Foreign Key model (i.e. one-to-one relation).
            if type(target_data).__name__ == 'OrderedDict':
                for field in target_data.keys():
                    setattr(target, field, target_data[field])
                
                target.save()
            
            # Nested Foreign Key models (i.e. one-to-many relation).
            elif type(target_data).__name__ == 'list':
                
                # If we're given an empty list, we assume that the foreign keys should
                # be deleted.
                if len(target_data) == 0:
                    target.all().delete()
                
                # Otherwise, check if the foreign key already exists. If not, then
                # we can create it.
                else:
                    for data in target_data:
                        model_class = target.all().model
                        if target.filter(**data).count() == 0:
                            model_class.objects.create(kproperty=instance, **data)

            # Regular field update.
            else:
                setattr(instance, term, target_data)
            
            instance.save()
        
        return instance


'''   Serializer for cooperative living properties. '''
class CoOpSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):

        fields  = PropertySerializer.Meta.fields + ('floor_num', )


'''   Serializer for Condo models. '''
class CondoSerializer(CoOpSerializer):

    class Meta(CoOpSerializer.Meta):

        model   = Condo

    ''' Overrides parent by passing a Condo model as the 'property_class'. '''
    def create(self, validated_data):

        return super(CondoSerializer, self).create(Condo().__class__, validated_data)


'''   Serializer for freehold properties. '''
class FreeholdSerializer(PropertySerializer):

    class Meta(PropertySerializer.Meta):
        
        fields  = PropertySerializer.Meta.fields + ('freehold_contract', )


'''   Serializer for House models. '''
class HouseSerializer(FreeholdSerializer):

    class Meta(PropertySerializer.Meta):

        model   = House
        fields  = FreeholdSerializer.Meta.fields
   
    ''' Overrides parent by passing a House model as the 'property_class'. '''
    def create(self, validated_data):

        return super(HouseSerializer, self).create(House().__class__, validated_data)


'''   Serializer for Multiplex models. '''
class MultiplexSerializer(FreeholdSerializer):

    class Meta(FreeholdSerializer.Meta):

        model   = Multiplex
        fields  = FreeholdSerializer.Meta.fields + ('degree', )

    ''' Overrides parent by passing a House model as the 'property_class'. '''
    def create(self, validated_data):

        return super(MultiplexSerializer, self).create(Multiplex().__class__, validated_data)

