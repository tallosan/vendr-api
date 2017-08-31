#
# Custom generics.
#
# ===============================================================================

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from vendr_core import mixins


'''   Custom mixin for Nested model lists and creates. This should always be passed
      as the furthest left parent on a class, as Python resolves inherited
      classes from left-to-right. I.e. we want this mixin's methods to be
      called rather than those of the generic view's. '''
class NestedListCreateAPIView(mixins.ListNestedModelMixin,
                              mixins.CreateNestedModelMixin):
     pass


'''   Custom mixin for Nested model retrievals, updates, and deletions. This
      should always be passed as the furthest left parent on a class, as Python
      resolves inherited classes from left-to-right. I.e. we want this mixin's
      methods to be called rather than those of the generic view's. '''
class NestedRetrieveUpdateDestroyAPIView(mixins.RetrieveNestedModelMixin,
                                         mixins.UpdateNestedModelMixin):
    pass

