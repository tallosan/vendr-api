from rest_framework import permissions


'''   Ensure that the user accessing the object is its owner. '''
class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Allow write permissions if the user is also the owner.
        return int(view.kwargs['pk']) == request.user.pk

