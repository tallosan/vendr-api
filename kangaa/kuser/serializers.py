from django.contrib.auth import get_user_model

from rest_framework import serializers

from kproperty.models import Property
from kuser.models import KUser, Profile

User = get_user_model()


'''   Serializer for Profile models. '''
class ProfileSerializer(serializers.ModelSerializer):

    prof_pic = serializers.ImageField(use_url=True)
    
    class Meta:
        model   = Profile
        fields  = ('first_name', 'last_name',
                   'location',
                   'prof_pic',
                   'bio')


'''   Serializer for User models. '''
class UserSerializer(serializers.ModelSerializer):

    profile    = ProfileSerializer(required=False)
    properties = serializers.PrimaryKeyRelatedField(many=True, required=False,
                    queryset=Property.objects.select_subclasses())

    class Meta:
        model   = KUser
        fields  = ('id', #'href',
                   'email', #'password',
                   'profile',
                   'properties',
                   'join_date')

    ''' Handles the creation of a Kangaa User object.
        Args:
            validated_data: The request data we create the new model from.
    '''
    def create(self, validated_data):

        email       = validated_data.pop('email')
        password    = validated_data.pop('password')
        
        kuser       = User.objects.create_user(email=email, password=password)

        return kuser

    ''' Update all target fields.
        Args:
            instance: The actual user object to be updated.
            validated_data: Fields to be updated, and their updates.
    '''
    def update(self, instance, validated_data):
        
        for term in validated_data.keys():
            target_data = validated_data.pop(term)
            target = getattr(instance, term)
            
            # One-to-one relation update.
            if type(target_data).__name__ == 'OrderedDict':
                for field in target_data.keys():
                    setattr(target, field, target_data[field])

                target.save()
            
            # Regular field update.
            else:
                setattr(instance, term, target_data)
        
            instance.save()

        return instance

