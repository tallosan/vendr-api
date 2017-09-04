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

    """ Update a Profile model.
        Args:
            instance (Profile) -- The Profile model to be updated.
            validated_data (OrderedDict) -- The update data.
    """
    def update(self, instance, validated_data):

        if self.context['files']:
            for key in self.context['files']:
                validated_data[key] = self.context['files'][key]
            
        return super(ProfileSerializer, self).update(instance, validated_data)

