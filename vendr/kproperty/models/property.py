#
# Property models.
#
# ===========================================================================


from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from rest_framework.exceptions import APIException

from model_utils.managers import InheritanceManager


class PropertyManager(InheritanceManager):

    """ Queue of Property objects to unfeature. """
    def unfeature_queue(self):

        # We only feature properties for one day.
        feature_limit = timedelta(days=7)
        feature_duration = timezone.now() - feature_limit
        unfeature_queue = super(PropertyManager, self).get_queryset().\
                filter(is_featured=True).\
                filter(created_time__lte=feature_duration)

        return unfeature_queue


'''   [Abstract] Property model. Contains all data pertaining to a particular 
      Property instance. '''
class Property(models.Model):

    # Allows us to use polymorphism.
    objects = PropertyManager()
    
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
    _TYPES       = (
            ('coop', 'CoOp'),
            ('condo', 'Condo'),
            ('house', 'House'),
            ('townhouse', 'Townhouse'),
            ('manufactured', 'Manufactured'),
            ('vacant_land', 'Vacant Land')
    )
    _type        = models.CharField(choices=_TYPES, max_length=12, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    views        = models.IntegerField(default=0)
    offers       = models.IntegerField(default=0)
    is_featured  = models.BooleanField(default=True)
    display_pic  = models.PositiveIntegerField(default=0)
    
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

    ''' Custom field validation. '''
    def clean(self):
    
        # Ensure that we have no negative values.
        if any((field < 0) for field in [self.price, self.sqr_ftg,
            self.n_bedrooms, self.n_bathrooms]):
            raise ValidationError('error: field cannot have a negative value.')
        
        # Ensure that the display pic is pointing to an actual image.
        if self.display_pic > self.images.count():
            raise ValidationError('error: display pic index out of range.')

        super(Property, self).clean()


'''   Parent for all cooperative ownership properties. '''
class CoOp(Property):
    
    unit_num = models.PositiveIntegerField()
    parking_spaces = models.PositiveIntegerField()
    corporation_name = models.CharField(max_length=20, blank=True, null=True)

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

    ''' (Abstract) Raises a NotImplementedError, as this should be implemented
        in the child models. '''
    def get_serializer(self):
        raise NotImplementedError("no 'get_serializer()' method for parent CoOp.")


'''   Condo model. '''
class Condo(CoOp):

    """ We're overriding `save()` here to set the `_type` field. """
    def save(self, *args, **kwargs):

        if self._state.adding:
            self._type = 'condo'

        super(Condo, self).save(*args, **kwargs)

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

    """ We're overriding `save()` here to set the `_type` field. """
    def save(self, *args, **kwargs):

        if self._state.adding:
            self._type = 'house'

        super(House, self).save(*args, **kwargs)

    ''' Returns a HouseSerializer object. '''
    def get_serializer(self):

        from kproperty.serializers import HouseSerializer
        return HouseSerializer


'''   Townhouse model. '''
class Townhouse(Freehold):

    degree = models.IntegerField()

    """ We're overriding `save()` here to set the `_type` field. """
    def save(self, *args, **kwargs):

        if self._state.adding:
            self._type = 'townhouse'

        super(Townhouse, self).save(*args, **kwargs)

    ''' Returns a TownhouseSerializer object. '''
    def get_serializer(self):

        from kproperty.serializers import TownhouseSerializer
        return TownhouseSerializer


'''   Manufactured model. This includes properties such as mobile homes. '''
class Manufactured(Property):

    manufacturer = models.CharField(max_length=20)
    serial_num = models.CharField(max_length=15, blank=True, null=True)
    year = models.PositiveIntegerField(null=True)
    length = models.DecimalField(decimal_places=2, max_digits=100, blank=True,
                validators=MinValueValidator)
    width = models.DecimalField(decimal_places=2, max_digits=100, blank=True,
                validators=MinValueValidator)
    mobile_park = models.CharField(max_length=15, default='No Park')

    """ We're overriding `save()` here to set the `_type` field. """
    def save(self, *args, **kwargs):

        if self._state.adding:
            self._type = 'manufactured'

        super(Manufactured, self).save(*args, **kwargs)

    def get_serializer(self):

        from kproperty.serializers import ManufacturedSerializer
        return ManufacturedSerializer


'''   Vacant Land model. '''
class VacantLand(Property):

    """ We're overriding `save()` here to set the `_type` field. """
    def save(self, *args, **kwargs):

        if self._state.adding:
            self._type = 'vacant_land'

        super(VacantLand, self).save(*args, **kwargs)

    def get_serializer(self):

        from kproperty.serializers import VacantLandSerializer
        return VacantLandSerializer

