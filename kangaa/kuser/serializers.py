from django.contrib.auth.models import User

from rest_framework import serializers

from kproperty.models import Property


'''   Serializer for User models. '''
class UserSerializer(serializers.ModelSerializer):

    # User listings, by Property ID.
    listings = serializers.PrimaryKeyRelatedField(many=True,
                    queryset=Property.objects.select_subclasses())


    class Meta:

        model   = User
        fields  = ('id',
                    'username', 'password',
                    'email',
                    'listings')

