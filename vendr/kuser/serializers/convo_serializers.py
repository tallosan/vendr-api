
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    pass


class ConvoSerializer(serializers.ModelSerializer):

    messages = MessageSerializer(Message.objects.all(), many=True, required=True)
    
    def create(self, validated_data):
        pass


