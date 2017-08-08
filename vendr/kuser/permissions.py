#
# Permissions for User models & all user associated sub-models, like
# Notifications, Chats, & Messages.
#
# ========================================================================

from rest_framework import permissions

from kuser.exceptions import BadUserRequest


'''   Gives full permissions if the user is the owner of the posting, read
      permissions if not. '''
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        # If the request is safe (i.e. one that will not modify data), then
        # we can return True.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write permissions if the user is also the owner.
        return obj == request.user

class IsNotificationOwner(permissions.BasePermission):

    ''' Ensures that only users can access their resources. '''
    def has_object_permission(self, request, view, obj):
        
        # Raise an exception if the user does not own this notification.
        if not obj.recipient == request.user:
            error_msg = {'error': 'user cannot access this notification.'}
            raise BadUserRequest(detail=error_msg)

        return True


class ChatListPermissions(permissions.BasePermission):

    ''' A user simply needs to prove that they are the one owning this
        endpoint. Anyone can read or create on THEIR OWN chat list.
        Args:
            request -- The request object.
            view -- The ChatList view.
            obj -- The KUser object that owns the endpoint.
    '''
    def has_object_permission(self, request, view, obj):
        
        return request.user == obj


class ChatDetailPermissions(permissions.BasePermission):

    ''' Only chat participants can view and update an chat.
        Args:
            request -- The request object.
            view -- The ChatDetail view.
            obj -- The Chat object we're acting on.
    '''
    def has_object_permission(self, request, view, obj):
        
        # If the user is accessing a chat they're part of on another user's
        # endpoint then we should decline their request.
        if int(view.kwargs['pk']) != request.user.pk:
            return False
       
        return request.user in obj.participants.all()


class MessageListPermissions(permissions.BasePermission):
    
    ''' Only a convo participant can read, and/or create a message on
        a chat.
        Args:
            request -- The request object.
            view -- The MessageList view.
            obj -- The Chat object we're acting on.
    '''
    def has_object_permission(self, request, view, obj):
        
        # If the user is accessing a chat they're part of on another user's
        # endpoint then we should decline their request.
        if int(view.kwargs['pk']) != request.user.pk:
            return False

        return request.user in obj.participants.all()
        
