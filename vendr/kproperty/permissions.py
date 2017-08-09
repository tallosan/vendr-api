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
        return obj.owner == request.user


'''   Ensures that only the property owner can create open houses for a
      given property. '''
class OpenHouseListPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method == 'POST':
            return request.user == obj.owner


'''   Ensure that only the open house owner can view, update, and delete
      their open houses. '''
class OpenHouseDetailPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user; open_house_owner = obj.owner

        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Ensure the user is the open house owner.
        elif request.method in ['PUT', 'DELETE']:
            return request.user == open_house_owner


'''   Ensure that open house owners are not RSVP'ing to their own open houses, but
      are the only ones able to view their open house's RSVP list. '''
class RSVPListPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        user = request.user; open_house_owner = obj.owner
        
        # Ensure the open house owner is not scheduling an appointment on their
        # own home.
        if request.method == 'POST':
            return request.user != open_house_owner

        # Ensure that only the home owner can view the RSVP list.
        elif request.method == 'GET':
            return request.user == open_house_owner


'''   Ensure that only the user who has RSVP'd can view, update, and delete
      their RSVP. '''
class RSVPDetailPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user; rsvp_owner = obj.owner
        return user == rsvp_owner

