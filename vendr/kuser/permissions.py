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

