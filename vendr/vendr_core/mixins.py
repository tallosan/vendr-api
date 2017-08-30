#
# Custom Mixins.
#
# ===============================================================================

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException


'''   Custom mixin for Nested model lists and creates. This should always be passed
      as the furthest left parent on a class, as Python resolves inherited
      classes from left-to-right. I.e. we want this mixin's methods to be
      called rather than those of the generic view's. '''
class NestedListCreateModelMixin(object):
     
    parent_pk_field = 'pk'
    relation_type = 'foreign_key'

    ''' Returns a queryset of all nested models, identified by field name,
        that exist on the given parent. '''
    def get_queryset(self):

        parent = self.parent.objects.get(pk=self.kwargs[self.parent_pk_field])
        nested_queryset = getattr(parent, self.field_name, self.parent.objects.none())

        # Check if we're dealing with a foreign key.
        if hasattr(nested_queryset, 'all'):
            return nested_queryset.all()

        return [nested_queryset]
   
    ''' Create a Nested object on the given parent model.
        Args:
            request -- The POST request.
    '''
    def create(self, request, *args, **kwargs):
        
        parent = self.parent.objects.get(pk=self.kwargs[self.parent_pk_field])
        self.check_object_permissions(request, parent)
        
        serializer = self.serializer_class(data=request.data, context=request.FILES)
        if serializer.is_valid():
            serializer.save(**{self.parent_field_name: parent})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Custom mixin for Nested model retrievals, updates, and deletions. This
      should always be passed as the furthest left parent on a class, as Python
      resolves inherited classes from left-to-right. I.e. we want this mixin's
      methods to be called rather than those of the generic view's. '''
class NestedRetrieveUpdateDestroyAPIView(object):

    parent_pk_field = 'pk'

    ''' Returns the nested model, identified by its lookup field, that exists
        on the given parent. '''
    def get_object(self):

        try:
            parent = self.parent.objects.get(pk=self.kwargs[self.parent_pk_field])
            instance = getattr(parent, self.field_name)
            if hasattr(instance, 'get'):
                instance = instance.get(pk=self.kwargs[self.pk_field])

            self.check_object_permissions(self.request, parent)
        except ObjectDoesNotExist:
            error_msg = {'error': 'nested model with pk {} does not exist.'.\
                                  format(self.kwargs[self.pk_field])}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status = 404; raise dne_exc
        
        return instance

    ''' Updates a nested model, identified by its pk field, that exists on the
        given parent.
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

