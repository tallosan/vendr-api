#
# Property Field Endpoints.
#
# These endpoints are for any foreign key (one-to-many) related sub-models
# on Property objects.
#
# =======================================================================

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import APIException

from kproperty.models import Property, Features, TaxRecords, Images
from kproperty.serializers import FeaturesSerializer, TaxRecordsSerializer,\
                                    ImagesSerializer
import kproperty.permissions as kproperty_permissions

from vendr_core.generics import NestedListCreateAPIView, \
    NestedRetrieveUpdateDestroyAPIView


'''   Create and List endpoint on Feature objects. '''
class FeaturesList(NestedListCreateAPIView):
    
    parent = Property
    parent_field_name = 'kproperty'
    field_name = 'features'

    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )


'''   Retrieve, Update, and Delete endpoint on Features objects. '''
class FeaturesDetail(NestedRetrieveUpdateDestroyAPIView):

    parent = Property
    field_name = 'features'
    pk_field = 'ft_pk'
    
    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )


'''   Create and List endpoint on Tax Records objects. '''
class TaxRecordsList(NestedListCreateAPIView):

    parent = Property
    parent_field_name = 'kproperty'
    field_name = 'tax_records'

    queryset = TaxRecords.objects.all()
    serializer_class = TaxRecordsSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )
        

'''   Retrieve, Update, and Delete endpoint on Tax Record objects. '''
class TaxRecordsDetail(NestedRetrieveUpdateDestroyAPIView):

    parent = Property
    field_name = 'tax_records'
    pk_field = 'tr_pk'

    queryset = TaxRecords.objects.all()
    serializer_class = TaxRecordsSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )


'''   Create and List endpoint on Image objects. '''
class ImagesList(NestedListCreateAPIView):

    parent = Property
    parent_field_name = 'kproperty'
    field_name = 'images'

    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )

        
'''   Retrieve, Update, and Delete endpoint on Image objects. '''
class ImagesDetail(NestedRetrieveUpdateDestroyAPIView):

    parent = Property
    field_name = 'images'
    pk_field = 'i_pk'

    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )

