from __future__ import unicode_literals

from django.db import models

from model_utils.managers import InheritanceManager


#TODO: Add indexing to primary key / primary fields. (db_index=True)
'''   Property model. Contains all data pertaining to a particular 
      Property instance. '''
class Property(models.Model):

    # Allows us to use polymorphism.
    objects     = InheritanceManager()
    
    # Owner of this property listing.
    owner       = models.ForeignKey('auth.User',
                    related_name='listings',
                    on_delete=models.CASCADE)

    # Main attributes.
    price       = models.FloatField(blank=False)
    sqr_ftg     = models.FloatField(blank=False)
    n_bedrooms  = models.IntegerField(blank=False)
    n_bathrooms = models.IntegerField(blank=False)
    location    = models.ForeignKey('Location',
                    related_name='location',
                    on_delete=models.CASCADE, blank=False)
    
    ''' Returns the serializer type for this model. '''
    def get_serializer(self):
        raise NotImplementedError("'get_serializer()' must be implimented.")


'''   Condo model. Contains all data pertaining to a particular Condo
      instance. Child of 'Property'. '''
class Condo(Property):
    
    floor_num   = models.IntegerField()

    ''' Returns a CondoSerializer object. '''
    def get_serializer(self):
    
        from kproperty.serializers import CondoSerializer
        return CondoSerializer
 

'''   House model. Contains all data pertaining to a particular House
      instance. Child of 'Property'. '''
class House(Property):
    
    ''' Returns a HouseSerializer object. '''
    def get_serializer(self):

        from kproperty.serializers import HouseSerializer
        return HouseSerializer


'''   Location model. Contains locational data for a particular listing. '''
class Location(models.Model):

    country     = models.CharField(max_length=50, blank=False)
    province    = models.CharField(max_length=20, blank=False)
    city        = models.CharField(max_length=30, blank=False)
    
    address     = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=10, blank=False)
    
    longitude   = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    latitude    = models.DecimalField(max_digits=9, decimal_places=6, blank=False)

