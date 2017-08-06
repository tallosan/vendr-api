#
# Convo views.
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from kuser.models import Convo
from kuser.serializers import ConvoSerializer, ConvoSerializer

from kuser.permissions import IsConvoOwner
from kuser.exceptions import ConvoNotFound, InvalidFieldRequest


User = get_user_model()


class ConvoWSAuth(APIView):

    permission_classes =  ( permissions.IsAuthenticated, IsConvoOwner,)

''' Return the actual serializer class given a serializer class string. Note, we
    can do this simply by querying over our user serializer module.
    Args:
        serializer_class: The serializer name in string form.
'''
def resolve_serializer(serializer_class):

    serializer = getattr(kuser.serializers, serializer_class)

    return serializer


'''   Convo list view. '''
class ConvoList(APIView):

    serializer_class   = ConvoSerializer
    permission_classes = ( permissions.IsAuthenticated, IsConvoOwner, )
    
    ''' Get the given user's messages.
        Args:
            user_pk: The primary key of the user we're querying over.
    '''
    def get_queryset(self, user_pk):

        user = User.objects.get(pk=user_pk)
        return user.convos.all().order_by('-timestamp')

    ''' Get a list of messages for a given user.
        Args:
            request: The GET request data.
            user_pk: The primary key of the user we're querying over.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, user_pk, format=None):
        
        # Get the message queryset.
        queryset = self.get_queryset(user_pk)

        # Serialize each message.
        response = []
        for message in queryset:
            response.append(self.serializer_class(message).data)

        return Response(response)

    ''' Create a new conversation with the given users. '''
    def post(self, request, user_pk, format=None):
        
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Convo detail view. '''
class ConvoDetail(APIView):

    serializer         = ConvoSerializer
    permission_classes = ( IsConvoOwner, )
    valid_fields       = [ 'is_viewed' ]

    def get_object(self, user_pk, pk):

	# Attempt to get the message, and set the appropriate serializer.
        try:

            # Get the user and message, and check their permissions.
            user = User.objects.get(pk=user_pk)
            message = user.notifications.all().get(pk=pk)
            self.check_object_permissions(self.request, message)

            return message

	# Raise exception if the message does not exist.
	except (TransactionConvo.DoesNotExist, OfferNotification.DoesNotExist, \
	       ContractConvo.DoesNotExist) as dne:
		error_msg = {'error': 'message with id ' + str(pk) + \
				      ' does not exist.'}
		raise ConvoNotFound(detail=error_msg)

    ''' Handles GET requests for Convo models.
        Args:
            request: Handler for the request field.
            user_pk: The primary key of the user.
            pk: The primary key of the message.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, user_pk, pk):

        message    = self.get_object(user_pk, pk)
        self.serializer = self.serializer(message)

        return Response(self.serializer.data)

