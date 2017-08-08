#
# Chat Serializers.
#
# =======================================================================

from rest_framework import serializers

from kuser.models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('pk', 'sender', 'content', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = ('pk', 'participants')

    def create(self, validated_data):
        
        participants = validated_data.pop('participants')
        
        chat = Chat.objects.create()
        sender = self.context.pop('sender'); chat.participants.add(sender)
        for participant in participants:
            chat.participants.add(participant)

        return chat

