from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from kuser.models import *
from kuser.permissions import IsNotificationOwner
from kuser.exceptions import NotificationNotFound, InvalidFieldRequest


User = get_user_model()


class WSAuth(APIView):

    permission_classes =  ( permissions.IsAuthenticated, IsNotificationOwner,)
    
    def get(self, request, pk):

        # Ensure the user has permission.
        if request.user.pk != int(pk):
            error_msg = 'error: you do not have permission to view this resource'
            no_auth_exc = APIException(detail=error_msg)
            no_auth_exc.status_code = status.HTTP_403_FORBIDDEN
            raise no_auth_exc

        return Response(status=status.HTTP_200_OK)

