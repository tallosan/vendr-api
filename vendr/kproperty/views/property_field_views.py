#
# Property Field Endpoints.
#
# These endpoints are for any foreign key (one-to-many) related sub-models
# on Property objects.
#
# =======================================================================

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import APIException

from kproperty.models import Property, Features, TaxRecords, Images
from kproperty.serializers import FeaturesSerializer, TaxRecordsSerializer,\
                                    ImagesSerializer
import kproperty.permissions as kproperty_permissions


'''   Custom mixin for Nested model lists and creates. This should always be passed
      as the furthest left parent on a class, as Python resolves inherited
      classes from left-to-right. I.e. we want this mixin's methods to be
      called rather than those of the generic view's. '''
class NestedListCreateModelMixin(object):
     
    ''' Returns a queryset of all nested models, identified by field name,
        that exist on a given Property. '''
    def get_queryset(self):

        kproperty = Property.objects.get(pk=self.kwargs['pk'])
        return getattr(kproperty, self.field_name).all()
   
    ''' Create a Nested object on the given Property model.
        Args:
            request -- The POST request.
    '''
    def create(self, request, *args, **kwargs):
        
        kproperty = Property.objects.get(pk=self.kwargs['pk'])
        self.check_object_permissions(request, kproperty)
        
        serializer = self.serializer_class(data=request.data, context=request.FILES)
        if serializer.is_valid():
            serializer.save(kproperty=kproperty)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Custom mixin for Nested model retrievals, updates, and deletions. This
      should always be passed as the furthest left parent on a class, as Python
      resolves inherited classes from left-to-right. I.e. we want this mixin's
      methods to be called rather than those of the generic view's. '''
class NestedRetrieveUpdateDestroyAPIView(object):

    ''' Returns the nested model, identified by its lookup field, that exists
        on the given Property. '''
    def get_object(self):

        try:
            kproperty = Property.objects.get(pk=self.kwargs['pk'])
            instance = getattr(kproperty, self.field_name).\
                       get(pk=self.kwargs[self.pk_field])
            self.check_object_permissions(self.request, kproperty)
        except ObjectDoesNotExist:
            error_msg = {'error': 'nested model with pk {} does not exist.'.\
                                  format(self.kwargs['pk'])}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status = 404; raise dne_exc
        
        return instance

    ''' Updates a nested model, identified by its pk field, that exists on the
        given Property.
        Args:
            request -- The PUT request.
    '''
    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.serializer_class(instance, data=request.data,
                        context=request.FILES, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Create and List endpoint on Feature objects. '''
class FeaturesList(NestedListCreateModelMixin, ListCreateAPIView):
    
    queryset = Features.objects.all()
    field_name = 'features'
    serializer_class = FeaturesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )

'''   Retrieve, Update, and Delete endpoint on Features objects. '''
class FeaturesDetail(NestedRetrieveUpdateDestroyAPIView, RetrieveUpdateDestroyAPIView):

    queryset = Features.objects.all()
    field_name = 'features'
    pk_field = 'ft_pk'
    serializer_class = FeaturesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )


'''   Create and List endpoint on Tax Records objects. '''
class TaxRecordsList(NestedListCreateModelMixin, ListCreateAPIView):

    queryset = TaxRecords.objects.all()
    field_name = 'tax_records'
    serializer_class = TaxRecordsSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )
        
'''   Retrieve, Update, and Delete endpoint on Tax Record objects. '''
class TaxRecordsDetail(NestedRetrieveUpdateDestroyAPIView, RetrieveUpdateDestroyAPIView):

    queryset = TaxRecords.objects.all()
    field_name = 'tax_records'
    pk_field = 'tr_pk'
    serializer_class = TaxRecordsSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )


'''   Create and List endpoint on Image objects. '''
class ImagesList(NestedListCreateModelMixin, ListCreateAPIView):

    queryset = Images.objects.all()
    field_name = 'images'
    serializer_class = ImagesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )
        
'''   Retrieve, Update, and Delete endpoint on Image objects. '''
class ImagesDetail(NestedRetrieveUpdateDestroyAPIView, RetrieveUpdateDestroyAPIView):

    queryset = Images.objects.all()
    field_name = 'images'
    pk_field = 'i_pk'
    serializer_class = ImagesSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
                           kproperty_permissions.IsOwnerOrReadOnly
    )

