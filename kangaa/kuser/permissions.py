from rest_framework import permissions


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

