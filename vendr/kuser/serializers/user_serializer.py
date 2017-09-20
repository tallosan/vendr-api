#
# Serializer for User models.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from kuser.models import KUser
from .profile_serializer import ProfileSerializer

User = get_user_model()


"""   Serializer for User model creation and updates. """
class UserCreateUpdateSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()
    class Meta:
        model   = KUser
        fields  = ('id', 'email', 'password', 'join_date', 'profile')
    
    """ Handles the creation of a Kangaa User object.
        Args:
            validated_data: The request data we create the new model from.
    """
    def create(self, validated_data):

        email       = validated_data.pop('email')
        password    = validated_data.pop('password')
        kuser       = User.objects.create_user(email=email, password=password)
        
        # Create the user profile if any data is given.
        try:
            prof = validated_data.pop('profile')
            if self.context: validated_data.update(self.get_file_data())
            for key in prof.keys():
                setattr(kuser.profile, key, prof.pop(key))
            
            kuser.profile.save()
        except KeyError: pass
        
        return kuser

    """ Update all target fields.
        Args:
            instance: The actual user object to be updated.
            validated_data: Fields to be updated, and their updates.
    """
    def update(self, instance, validated_data):
        
        # Files are passed through the context.
        if self.context:
            validated_data.update(self.get_file_data())

        for term in validated_data.keys():
            target_data = validated_data.pop(term)
            target = getattr(instance, term)
            
            # One-to-one relation update.
            if issubclass(target_data.__class__, dict):
                for field in target_data.keys():
                    setattr(target, field, target_data[field])
                
                target.save()
            
            # Handle password updates.
            elif term == 'password':
                instance.set_password(target_data)
 
            # Regular field update.
            else:
                setattr(instance, term, target_data)
        
            instance.save()

        return instance

    """ Get file objects from the context. N.B. -- only the Profile object
        contains a file (image) field.
    """
    def get_file_data(self):

        file_data = { 'profile': {} }
        for file_key in self.context.keys():
            file_data['profile'][file_key] = self.context[file_key]

        return file_data


class UserReadSerializer(serializers.ModelSerializer):

    class Meta:
        model   = KUser
        fields  = ('id', 'email', 'password', 'join_date')

    """ Adds a quick profile (i.e. stripped down profile object) to the
        serializers User.
        Args:
            instance (User) -- The user being serialized.
    """
    def to_representation(self, instance):

        user = super(UserReadSerializer, self).to_representation(instance)
        profile = instance.profile
        user['quick_profile'] = {
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'last_name': profile.last_name,
                'prof_pic':  profile.prof_pic.name
        }

        return user

