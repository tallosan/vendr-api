#
# Email verification for users.
#
# =========================================================================

import uuid

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import status, permissions 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from vendr_core.permissions import IsOwner

from kuser.serializers import TwoFactorAuthSerializer

User = get_user_model()


class RequestEmailVerification(APIView):

    def get_object(self, pk):

        try:
            kuser = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, self)
            return kuser
        except User.DoesNotExist:
            pass

    """ A user can verify their account via email by POST'ing the randomly
        generated token they receive in their email. If the tokens match
        then they're verified.
    """
    def post(self, request, pk, *args, **kwargs):

        kuser = self.get_object(pk)
        status = self.send_mail(kuser)

        return Response({'success': status}, status=200)

    """ Send the given user an email containing a randomly generated
        authentication token. Returns the status of the email sending call.
        Args:
            kuser (User) -- The user being verified.
    """
    def send_mail(self, kuser):

        # Genreate random string, and set the user's verification token.
        token = str(uuid.uuid4())
        kuser._verification_token = token; kuser.verified = False
        kuser.save()

        # Construct our verification email.
        recipient = kuser.email
        subject = 'Authorize your Vendr Account'

        header = """<h2 style="text-align:center;" style="color:#0bb3a2;" style="font-family:Circular,Helvetica Neue,Helvetica,Arial,sans-serif;">Vendr Accounts</h2>"""
        greeting = """<p style="text-align:center;" style="font-family:Circular,Helvetica Neue,Helvetica,Arial,sans-serif;">Hey {}, it's Andrew, CEO of Vendr. You're just a click away from verifying your Vendr account!</p>""".format(kuser.profile.first_name)
        verify = """<h3 style="text-align:center;"><a style="color:#0bb3a2;" style="text-decoration:none" style="font-weight:500;" style="font-family:Circular,Helvetica Neue,Helvetica,Arial,sans-serif;" href="http://api.vendr.xyz/v1/users/1/{}/">Verify</a></h3>""".format(token)
        body = """<p style="text-align:center;" style="font-family:Circular,Helvetica Neue,Helvetica,Arial,sans-serif;">We're delighted to have you be a part of our movement, and hope you have a great experience with us!"""
        footer = """<p style="text-align:center;" style="font-family:Circular,Helvetica Neue,Helvetica,Arial,sans-serif;">If you have any questions, feel free to email us at:<a style="font-family:Circular,Helvetica Neue,Helvetica,Arial,sans-serif;" href="support@vendr.xyz"></a>Our 24 hour on-staff assistants will be happy to help!</p>"""
        html_message = '{}{}{}{}{}'.format(header, greeting, verify, body, footer)

        # Send the email. Note, we only need the HTML message.
        status = send_mail(
                subject=subject,
                message='',
                from_email=settings.EMAIL_VERIFICATION_ADDRESS,
                #recipient_list=[kuser.email],
                recipient_list=['andrew.tallos@mail.utoronto.ca'],
                #html_message=html_message,
                fail_silently=False
        )

        return status == 1


class VerifyEmailVerification(APIView):

    def get_object(self, pk):

        try:
            kuser = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, self)
            return kuser
        except User.DoesNotExist:
            pass

    """ A user can verify their account by POST'ing to an endpoint that
        ends with their verification token.
    """
    def post(self, request, pk, token, *args, **kwargs):

        kuser = self.get_object(pk)

        # Ensure that the verification tokens are the same.
        status = str(kuser._verification_token) == token
        kuser.verified = status; kuser.save()

        return Response({'success': status}, status=200)

