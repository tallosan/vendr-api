from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from model_utils.managers import InheritanceManager


'''   Property model. Contains all data pertaining to a particular 
      Property instance. '''
class Property(models.Model):

    # Allows us to use polymorphism.
    objects     = InheritanceManager()
    
    # Owner of this property listing.
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='listings',
                    on_delete=models.CASCADE, db_index=True)

    # Main attributes.
    price       = models.FloatField(blank=False, db_index=True)
    sqr_ftg     = models.FloatField(blank=False, db_index=True)
    n_bedrooms  = models.IntegerField(blank=False, db_index=True)
    n_bathrooms = models.IntegerField(blank=False, db_index=True)
    
    # Foreign key attributes.
    # [ location, history, tax_records, features ]
    
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


###  Detail objects. ###
'''   Location model. Contains locational data for a particular listing. '''
class Location(models.Model):

    kproperty   = models.OneToOneField('Property', related_name='location',
                    on_delete=models.CASCADE)

    country     = models.CharField(max_length=50, blank=False, db_index=True)
    province    = models.CharField(max_length=20, blank=False, db_index=True)
    city        = models.CharField(max_length=30, blank=False, db_index=True)
    address     = models.CharField(max_length=100, blank=False, db_index=True)
    postal_code = models.CharField(max_length=10, blank=False, db_index=True)
    
    longitude   = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    latitude    = models.DecimalField(max_digits=9, decimal_places=6, blank=False)


'''   Feature model. Contains the property features (e.g. fireplace, garden, etc). '''
class Features(models.Model):
    
    kproperty   = models.ForeignKey('Property', related_name='features',
                    on_delete=models.CASCADE)
    
    feature     = models.CharField(max_length=50, blank=True)


'''   Tax model. Contains the tax data for the property. '''
class TaxRecord(models.Model):

    kproperty   = models.ForeignKey('Property', related_name='tax_records',
                    on_delete=models.CASCADE)

    # Most recent tax assessment, and the year in which it was made.
    assessment      = models.FloatField(blank=True, null=True)
    assessment_year = models.IntegerField(blank=True, null=True)


'''   Historical model. Contains data about the history of the property. '''
class Historical(models.Model):
    
    kproperty   = models.OneToOneField('Property', related_name='history',
                    on_delete=models.CASCADE)

    # Price the property was last sold for, and the date it was sold.
    last_sold_price = models.FloatField(blank=True, null=True)
    last_sold_date  = models.DateField(blank=True, null=True)

    # The year the property was built.
    year_built      = models.IntegerField(blank=True, null=True)


'''   Open house model. Contains scheduling info about open house / showing times. '''
class OpenHouse(models.Model):

    pass

