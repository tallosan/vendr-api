#
# Schedule serializers.
#
# ========================================================================

from rest_framework import serializers

from kproperty.models import RSVP


class ScheduleSerializer(serializers.ModelSerializer):

    open_house_pk = serializers.ReadOnlyField(source='open_house.pk')
    kproperty = serializers.ReadOnlyField(source='open_house.kproperty.pk')
    start = serializers.ReadOnlyField(source='open_house.start')
    end = serializers.ReadOnlyField(source='open_house.end')

    class Meta:
        model = RSVP
        fields = ('pk', 'open_house_pk', 'kproperty', 'start', 'end')

