#
# Notification views.
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

import kuser.serializers

from kuser.models import *
from kuser.permissions import IsNotificationOwner
from kuser.exceptions import NotificationNotFound, InvalidFieldRequest


User = get_user_model()


''' Return the actual serializer class given a serializer class string. Note, we
    can do this simply by querying over our user serializer module.
    Args:
        serializer_class: The serializer name in string form.
'''
def resolve_serializer(serializer_class):

    serializer = getattr(kuser.serializers, serializer_class)

    return serializer


'''   Notification list view. '''
class NotificationList(APIView):

    permission_classes = ( permissions.IsAuthenticated, IsNotificationOwner, )
    
    ''' Get the given user's notifications.
        Args:
            user_pk: The primary key of the user we're querying over.
    '''
    def get_queryset(self, user_pk):

        user = self.request.user
        return user.notifications.all()

    ''' Get a list of notifications for a given user.
        Args:
            request: The GET request data.
            user_pk: The primary key of the user we're querying over.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, user_pk, format=None):
        
        # Get the notification queryset.
        queryset = self.get_queryset(user_pk)

        # Serialize each notification. Note, our queryset only contains parent
        # notifications, so we'll want to downcast so that we can their serializer.
        response = []
        for notification in queryset:
            
            # Downcast if necessary to get the correct type.
            if notification.actual_type:
                notification = notification.actual_type
        
            notification_class = notification.__class__
            
            # Get the appropriate serializer and serialize the data.
            serializer_class = notification_class().get_serializer()
            serializer       = resolve_serializer(serializer_class)

            response.append(serializer(notification).data)

        return Response(response)


'''   Notification detail view. '''
class NotificationDetail(APIView):

    serializer         = None
    permission_classes = ( IsNotificationOwner, )
    valid_fields       = [ 'is_viewed' ]

    def get_object(self, user_pk, pk):

	# Attempt to get the notification, and set the appropriate serializer.
        try:

            # Get the user and notification, and check their permissions.
            user = User.objects.get(pk=user_pk)
            notifications = user.all_notifications
            notification = [_notification
                            for _notification in notifications
                            if str(_notification.pk) == str(pk)
            ][0]
            self.check_object_permissions(self.request, notification)
            
            if notification.actual_type:
                notification = notification.actual_type

            notification_class = notification.__class__

            serializer_class = notification_class().get_serializer()
            self.serializer = resolve_serializer(serializer_class)

            return notification

	# Raise exception if the notification does not exist.
	except (IndexError,
                TransactionNotification.DoesNotExist,
                OfferNotification.DoesNotExist, \
	        ContractNotification.DoesNotExist) as dne:
		error_msg = {'error': 'notification with id ' + str(pk) + \
				      ' does not exist.'}
		raise NotificationNotFound(detail=error_msg)

    ''' Handles GET requests for Notification models.
        Args:
            request: Handler for the request field.
            user_pk: The primary key of the user.
            pk: The primary key of the notification.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, user_pk, pk):

        notification    = self.get_object(user_pk, pk)
        self.serializer = self.serializer(notification)

        return Response(self.serializer.data)

    ''' Handles PUT requests for Notification models. Note, we can only update
        certain fields on a notification.
        Args:
            request: The update data for the notification.
            user_pk: The primary key of the user.
            pk: The primary key of the notification.
            *format: Specified data format (e.g. JSON).
    '''
    def put(self, request, user_pk, pk):

        for key in request.data.keys():
            if key not in self.valid_fields:
                error_msg = {'error': "'" + key + "'" + ' cannot be altered.'}
		raise InvalidFieldRequest(detail=error_msg)

        notification = self.get_object(user_pk, pk)
        self.serializer = self.serializer(notification, data=request.data, partial=True)
        if self.serializer.is_valid():
            self.serializer.save()
            return Response(self.serializer.data)

        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)

