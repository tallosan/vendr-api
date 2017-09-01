#
# Serializer for a User's Profile model.
#
# =========================================================================

from rest_framework import serializers
from kuser.models import Profile


'''   Serializer for Profile models. '''
class ProfileSerializer(serializers.ModelSerializer):

    prof_pic = serializers.ReadOnlyField(source='prof_pic.name')
    
    class Meta:
        model   = Profile
        fields  = ('first_name', 'last_name',
                   'location',
                   'prof_pic',
                   'bio')

