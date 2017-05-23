#
# Property field models.
#
# ===========================================================================


from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from hashlib import sha256

from .property import Property
from custom_storage import ZappMediaStorage


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


'''   Features model. Contains the property features (e.g. fireplace, garden, etc). '''
class Features(models.Model):
    
    kproperty   = models.ForeignKey('Property', related_name='features',
                    on_delete=models.CASCADE)
    
    feature     = models.CharField(max_length=50, blank=True)


'''   Tax Record model. Contains the tax data for the property. '''
class TaxRecords(models.Model):

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


''' (Helper) Generates a file name for an image model. '''
def listing_file_name(instance, filename):
        
        BASE_URL = '/listings/images/'
        FILE_EXT = sha256(instance.encode('utf-8')).hexdigest()

        return BASE_URL + FILE_EXT

'''   Images model. Contains all images associated with the property. '''
class Images(models.Model):
    
    kproperty = models.ForeignKey('Property', related_name='images',
                    on_delete=models.CASCADE)
    #thumbnail = models.ImageField(upload_to=listing_file_name,
                    #storage=ZappMediaStorage())
    image = models.ImageField(upload_to=listing_file_name,
                    storage=ZappMediaStorage())
    #low_resolution = models.ImageField(upload_to=listing_file_name,
                    #storage=ZappMediaStorage())
    #standard_resolution = models.ImageField(upload_to=listing_file_name,
                    #storage=ZappMediaStorage())


'''   Open house model. Contains scheduling info about open house / showing times. '''
class OpenHouse(models.Model):

    pass

