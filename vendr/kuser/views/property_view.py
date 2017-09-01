#
# User schedule.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView

from kuser.serializers import UserPropertySerializer


User = get_user_model()


class PropertyList(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserPropertySerializer

