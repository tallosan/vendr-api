#
# Property models.
#
# ===========================================================================


from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.exceptions import APIException

from model_utils.managers import InheritanceManager


'''   [Abstract] Property model. Contains all data pertaining to a particular 
      Property instance. '''
class Property(models.Model):

    # Allows us to use polymorphism.
    objects = InheritanceManager()
    
    # Owner of this property listing.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='properties',
                    on_delete=models.CASCADE, db_index=True)

    # Main attributes.
    price        = models.FloatField(blank=False, db_index=True)
    sqr_ftg      = models.FloatField(blank=False, db_index=True)
    n_bedrooms   = models.IntegerField(blank=False, db_index=True)
    n_bathrooms  = models.IntegerField(blank=False, db_index=True)
    description  = models.CharField(max_length=350, blank=True, null=True)
    
    # Foreign key attributes.
    # [ location, history, tax_records, features, images ]

    # Meta data.
    created_time = models.DateTimeField(auto_now_add=True)
    views        = models.IntegerField(default=0)
    offers       = models.IntegerField(default=0)
    is_featured  = models.BooleanField(default=False)
    
    ''' (Abstract) Returns the serializer type for this model. '''
    def get_serializer(self):
        raise NotImplementedError("'get_serializer()' must be implemented.")

    def save(self, *args, **kwargs):

        #TODO: Move the exception raising to child classes.
        if not self.pk:
            try:
                self.full_clean()
            except ValidationError as validation_error:
                validation_exc = APIException(detail=validation_error.messages[0])
                validation_exc.status_code = 403
                raise validation_exc
            
        super(Property, self).save(*args, **kwargs)

    ''' Unfeature a property after a set amount of time.
        Args:
            kproperty -- The property we're unfeaturing.
            eta -- The time for the task to execute.
    @app.task
    def _unfeature(self, kproperty, eta):
        pass
    '''

    ''' Custom field validation. '''
    def clean(self):
    
        # Ensure that we have no negative values.
        if any((field < 0) for field in [self.price, self.sqr_ftg,
            self.n_bedrooms, self.n_bathrooms]):
            raise ValidationError('error: field cannot have a negative value.')

        super(Property, self).clean()


'''   Parent for all cooperative ownership properties. '''
class CoOp(Property):
    
    unit_num = models.IntegerField()

    ''' (Abstract) Raises a NotImplementedError, as this should be implemented
        in the child models. '''
    def get_serializer(self):
        raise NotImplementedError("no 'get_serializer()' method for parent Freehold.")

    ''' Custom field validation. '''
    def clean(self):

        # Ensure the unit number is valid.
        if self.unit_num <= 0:
            raise ValidationError('error: unit number cannot be negative.')

        super(CoOp, self).clean()
    
    ''' CoOps have a unit # attached to them, so naturally we can have multiple
        with the same address. We cannot, however, have more than one with the
        same address and the same unit number.
    '''
    def validate_unique(self, exclude=None):

        try:
            if CoOp.objects.filter(location__address=self.location.address) \
                           .filter(unit_num=self.unit_num).count() > 1:
                raise ValidationError('error: a property with this address '
                                      'and unit number already exists')
        except CoOp.location.RelatedObjectDoesNotExist:
            pass

        super(CoOp, self).validate_unique(exclude=exclude)

'''   Condo model. '''
class Condo(CoOp):
    
    ''' Returns a CondoSerializer object. '''
    def get_serializer(self):
    
        from kproperty.serializers import CondoSerializer
        return CondoSerializer


'''   Parent for all freehold ownership properties. '''
class Freehold(Property):
    
    ''' (Abstract) Raises a NotImplementedError, as this should be implemented
        in the child models. '''
    def get_serializer(self):
        raise NotImplementedError("no 'get_serializer()' method for parent Freehold.")


'''   House model. '''
class House(Freehold):

    ''' Returns a HouseSerializer object. '''
    def get_serializer(self):

        from kproperty.serializers import HouseSerializer
        return HouseSerializer


'''   Townhouse model. '''
class Townhouse(Freehold):

    degree = models.IntegerField()

    ''' Returns a TownhouseSerializer object. '''
    def get_serializer(self):

        from kproperty.serializers import TownhouseSerializer
        return TownhouseSerializer


class Manufactured(Property):

    def get_serializer(self):

        from kproperty.serializers import ManufacturedSerializer
        return ManufacturedSerializer


class VacantLand(Property):

    def get_serializer(self):

        from kproperty.serializers import VacantLandSerializer
        return VacantLandSerializer

