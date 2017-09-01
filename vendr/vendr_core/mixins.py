#
# Custom mixins for nested models.
#
# ===============================================================================

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException


'''   List a nested model queryset. '''
class ListNestedModelMixin(object):

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


'''   Create a nested object instance. '''
class CreateNestedModelMixin(object):

    def create(self, request, *args, **kwargs):
 
        parent = self.parent.objects.get(pk=self.kwargs[self.parent_pk_field])
        self.check_object_permissions(request, parent)
        
        serializer = self.get_serializer(data=request.data, context=request.FILES)
        if serializer.is_valid():
            serializer.save(**{self.parent_field_name: parent})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Retrieve a nested model instance. '''
class RetrieveNestedModelMixin(object):

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


'''   Update a nested model instance. '''
class UpdateNestedModelMixin(object):

   def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data,
                        context=request.FILES, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Destroy a nested model instance. '''
class DestroyNestedModelMixin(object):

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


