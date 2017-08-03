
from rest_framework import serializers

from kproperty.models import OpenHouse, RSVP


class RSVPSerializer(serializers.ModelSerializer):

    kuser = serializers.ReadOnlyField(source='kuser.pk')

    class Meta:
        model = RSVP
        fields = ('pk', 'kuser')

class OpenHouseSerializer(serializers.ModelSerializer):
    
    rsvp_list = RSVPSerializer(RSVP.objects.all(), many=True)

    class Meta:
        model = OpenHouse
        fields = ('pk',
                  'rsvp_list',
                  'start', 'end')

