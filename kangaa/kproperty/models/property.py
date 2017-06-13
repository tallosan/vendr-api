#
# Property models.
#
# ===========================================================================


from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from model_utils.managers import InheritanceManager


'''   [Abstract] Property model. Contains all data pertaining to a particular 
      Property instance. '''
class Property(models.Model):

    # Allows us to use polymorphism.
    objects      = InheritanceManager()
    
    # Owner of this property listing.
    owner        = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='properties',
                    on_delete=models.CASCADE, db_index=True)

    # Main attributes.
    price        = models.FloatField(blank=False, db_index=True)
    sqr_ftg      = models.FloatField(blank=False, db_index=True)
    n_bedrooms   = models.IntegerField(blank=False, db_index=True)
    n_bathrooms  = models.IntegerField(blank=False, db_index=True)
    
    # Foreign key attributes.
    # [ location, history, tax_records, features, images ]

    # Meta data.
    created_time = models.DateTimeField(auto_now_add=True)
    views        = models.IntegerField(default=0)
    offers       = models.IntegerField(default=0)
    is_featured  = models.BooleanField(default=False)
    
    description  = models.CharField(max_length=350, blank=True, null=True)

    ''' (Abstract) Returns the serializer type for this model. '''
    def get_serializer(self):
        raise NotImplementedError("'get_serializer()' must be implemented.")

    ''' Custom string representation. '''
    def __str__(self):

        return self.location.address + ', ' + self.location.city + ' ' + \
                self.location.province


'''   Parent for all cooperative ownership properties. '''
class CoOp(Property):
    
    unit_num   = models.IntegerField()
    
    ''' (Abstract) Raises a NotImplementedError, as this should be implemented
        in the child models. '''
    def get_serializer(self):
        raise NotImplementedError("no 'get_serializer()' method for parent Freehold.")


'''   Condo model. '''
class Condo(CoOp):
    
    ''' Returns a CondoSerializer object. '''
    def get_serializer(self):
    
        from kproperty.serializers import CondoSerializer
        return CondoSerializer


'''   Parent for all freehold ownership properties. '''
class Freehold(Property):
    
    freehold_contract = models.IntegerField(default=0)
    
    ''' (Abstract) Raises a NotImplementedError, as this should be implemented
        in the child models. '''
    def get_serializer(self):
        raise NotImplementedError("no 'get_serializer()' method for parent Freehold.")


'''   POTL model. '''
class POTL(Freehold):

    monthly_expenses = models.FloatField()
    
    ''' Returns a HouseSerializer object. '''
    def get_serializer(self):

        from kproperty.serializers import POTLSerializer
        return POTLSerializer


'''   Multiplex model. '''
class Multiplex(Freehold):

    degree = models.IntegerField()

    ''' Returns a MultiplexSerializer object. '''
    def get_serializer(self):

        from kproperty.serializers import MultiplexSerializer
        return MultiplexSerializer

