#
#   Custom generics for nested models.
#
# ===============================================================================

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from vendr_core import mixins


class NestedGenericAPIView(GenericAPIView):

    parent_pk_field = 'pk'

    """ Returns a queryset of all nested models, identified by field name,
        that exist on the given parent. """
    def get_queryset(self):

        parent = self.parent.objects.get(pk=self.kwargs[self.parent_pk_field])
        nested_queryset = getattr(parent, self.field_name, self.parent.objects.none())

        # Check if we're dealing with a foreign key.
        if hasattr(nested_queryset, 'all'):
            return nested_queryset.all()

        return [nested_queryset]

    """ Returns the nested model, identified by its lookup field, that exists
        on the given parent. """
    def get_object(self):

        # Note, we can determine if the object to be returned is a `ForeignKey`
        # or `OneToOneField` by checking if it has a `get()` method.
        try:
            parent = self.parent.objects.get(pk=self.kwargs[self.parent_pk_field])
            self.check_object_permissions(self.request, parent)
            instance = getattr(parent, self.field_name)
            if hasattr(instance, 'get'):
                instance = instance.get(pk=self.kwargs[self.pk_field])
        except instance.model.DoesNotExist:
            error_msg = {'error': 'nested model with pk {} does not exist.'.\
                                  format(self.kwargs[self.pk_field])}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = 404; raise dne_exc
        
        return instance

    """ Include any files in the serializer context. """
    def get_serializer_context(self):

        context = super(NestedGenericAPIView, self).get_serializer_context()
        context['files'] = self.request.FILES
        return context

# ================================================================================

"""   Concrete view for creating a nested model instance. """
class NestedCreateAPIView(mixins.CreateNestedModelMixin, NestedGenericAPIView):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


"""   List a nested model queryset. """
class NestedListAPIView(mixins.ListNestedModelMixin, NestedGenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


"""   Concrete view for retrieving a nested model instance. """
class NestedRetrieveAPIView(mixins.RetrieveNestedModelMixin, NestedGenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


"""   Concrete view for destroying a nested model instance. """
class NestedDestroyAPIView(mixins.DestroyNestedModelMixin, NestedGenericAPIView):

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


"""   Concrete view for updating a nested model instance. """
class NestedUpdateAPIView(mixins.UpdateNestedModelMixin,
                          NestedGenericAPIView):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


"""   Concrete view for nested one-to-one resources.
      Example: `/parents/nestedmodel/` """
class NestedListUpdateAPIView(NestedListAPIView, NestedUpdateAPIView):

    """ We're going to make a slight modification here, as we only have one
        Profile object / User. Thus, it makes sense to pop the one Profile out
        of the queryset list so that it's easier to work with. """
    def get(self, request, *args, **kwargs):

        response = super(NestedListUpdateAPIView, self).get(
                request, *args, **kwargs)
        return Response(response.data[0])

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


"""   Concrete view for listing a queryset or creating a nested model instance. """
class NestedListCreateAPIView(mixins.ListNestedModelMixin,
                              mixins.CreateNestedModelMixin,
                              NestedGenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


"""   Concrete view for retrieving and updating a nested model instance. """
class NestedRetrieveUpdateAPIView(mixins.RetrieveNestedModelMixin,
                                  mixins.UpdateNestedModelMixin,
                                  NestedGenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


"""   Concrete view for retrieving or deleting a nested model instance. """
class NestedRetrieveDestroyAPIView(mixins.RetrieveNestedModelMixin,
                                   mixins.DestroyNestedModelMixin,
                                   NestedGenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


"""   Concrete view for retrieving, updating, or deleting a nested model instance. """
class NestedRetrieveUpdateDestroyAPIView(mixins.RetrieveNestedModelMixin,
                                         mixins.UpdateNestedModelMixin,
                                         mixins.DestroyNestedModelMixin,
                                         NestedGenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

