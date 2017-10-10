#
# User favourite properties.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import permissions

from kuser.serializers import SubscriptionsSerializer

from vendr_core.permissions import IsOwner
from kproperty.models import Property


User = get_user_model()


class SubscriptionsList(RetrieveAPIView, UpdateAPIView):
    
    queryset = User.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

    def get(self, request, *args, **kwargs):

        self.check_object_permissions(request, self)
        return super(SubscriptionsList, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        self.check_object_permissions(request, self)
        try:
            kproperty_pk = request.data.pop('kproperty')
        except KeyError:
            key_exc = APIException(
                    detail={'error': "field `kproperty` not specified."}
            )
            key_exc.status_code = status.HTTP_400_BAD_REQUEST; raise key_exc

        try:
            kproperty = Property.objects.get(pk=kproperty_pk)
        except Property.DoesNotExist:
            dne_exc = APIException(
                    detail={'error': "property with pk {} does not exist.".format(
                        kproperty_pk)
                    }
            )
            dne_exc.status_code = status.HTTP_400_BAD_REQUEST; raise dne_exc

        # Add the user to property's subscription list.
        kproperty._subscribers.add(request.user); kproperty.save()

        response = Response({}, status=status.HTTP_201_CREATED)
        response.data['subscribed'] = kproperty_pk

        return response
        
