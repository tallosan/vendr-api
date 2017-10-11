
from rest_framework import serializers

from kproperty.models import OpenHouse, RSVP


class RSVPSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.pk')

    class Meta:
        model = RSVP
        fields = ('pk', 'owner')


class OpenHouseSerializer(serializers.ModelSerializer):
    
    rsvp_list = RSVPSerializer(RSVP.objects.all(), many=True, required=False)

    class Meta:
        model = OpenHouse
        fields = ('pk',
                  'rsvp_list',
                  'start', 'end',
                  '_is_active'
        )

