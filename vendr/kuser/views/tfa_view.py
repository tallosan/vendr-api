#
# Two-Factor Authentication for users.
#
# =========================================================================

import messagebird

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status, permissions 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from vendr_core.permissions import IsOwner

from kuser.serializers import TwoFactorAuthSerializer

User = get_user_model()


class TwoFactorAuth(APIView):
    
    queryset = User.objects.all()
    serializer_class = TwoFactorAuthSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

    def get_object(self, pk):

        try:
            kuser = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, self)
            return kuser
        except User.DoesNotExist:
            dne_exc = APIException(
                    detail={'error': 'user {} does not exist.'.format(pk)}
            )
            dne_exc.status_code = 404; raise dne_exc
    
    """ Generate a random two-factor authenticatino code of length `length`.
        Note, we're only using uppercase characters and digits. This will
        give us an entroy of ...
                    (26 + 10)^6 == 36^6 == 2176782336 ~ 31-bits.
        Args:
            length (int) -- The length of the TFA code.
    """
    def _generate_tfa_code(self, length=6):

        import string
        import random

        tfa_code = ''
        for i in range(length):
            tfa_code +=  random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits
            )

        return tfa_code

    """ Create an SMS message containing an SMS code, and send it to a
        given user.
    """
    def post(self, request, pk, *args, **kwargs):

        kuser = self.get_object(pk=pk)

        # Ensure that the user has a phone number, and has enabled
        # two-factor-auth
        error_msg = None
        if not hasattr(kuser, 'phone_num'):
            error_msg = 'user {} has no attribute `phone_num`.'.format(kuser.pk)
        if kuser.tfa_enabled is False:
            error_msg = 'user {} does not have two-factor authentication ' \
                'enabled.'.format(kuser.pk)
        if error_msg:
            user_exc = APIException(detail={'error': error_msg})
            user_exc.status_code = 403; raise user_exc

        # Generate a two-factor auth code.
        tfa_code = self._generate_tfa_code()

        # Send an SMS message to the user's phone.
        client = messagebird.Client(settings.MESSAGEBIRD_ACCESS_KEY)
        try:
            message = client.message_create(
                    originator=settings.MESSAGEBIRD_SENDER,
                    recipients=kuser.phone_num,
                    body=tfa_code,
            )
        except messagebird.client.ErrorException as e:
            sms_exc = APIException(
                    detail={'error': 'the SMS message failed to send.'}
            )
            sms_exc.status_code = 403; raise sms_exc

        # Set the user's TFA code, and reset its validation status.
        kuser.tfa_code = tfa_code; kuser._tfa_code_validated = False
        kuser.save()

        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def get(self, request, pk, *args, **kwargs):

        kuser = self.get_object(pk=pk)
        serializer = self.serializer_class(kuser)

        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):

        kuser = self.get_object(pk=pk)
        serializer = self.serializer_class(kuser, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValueError as protected_field_error:
                pf_exc = APIException(
                        detail={'error': protected_field_error.message}
                )
                pf_exc.status_code = 403; raise pf_exc

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

