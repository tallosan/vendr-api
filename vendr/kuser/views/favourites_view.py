#
# User favourite properties.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import permissions

from kuser.serializers import FavouritesSerializer

from vendr_core.permissions import IsOwner


User = get_user_model()


class FavouritesList(RetrieveAPIView, UpdateAPIView):
    
    queryset = User.objects.all()
    serializer_class = FavouritesSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

    def get(self, request, *args, **kwargs):

        self.check_object_permissions(request, self)
        return super(FavouritesList, self).get(request, *args, **kwargs)

