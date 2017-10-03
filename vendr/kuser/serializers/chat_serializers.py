#
# Chat Serializers.
#
# =======================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from kuser.models import Chat, Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('pk', 'sender', 'sender_name', 'content', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = ('pk', 'participants', 'opened')

    def create(self, validated_data):
        
        participants = validated_data.pop('participants')
        
        chat = Chat.objects.create()
        sender = self.context.get('sender'); chat.participants.add(sender)
        for participant in participants:
            chat.participants.add(participant)

        return chat
    
    ''' Custom representation of a Chat. We want to serialize the user's
        profile pic in addition to their pk.
        Args:
            instance -- The chat to be serialized.
    '''
    def to_representation(self, instance):
        
        chat = super(ChatSerializer, self).to_representation(instance)

        # Get all participants minus the user making the request.
        participants = []
        request_sender = self.context.get('sender')
        for participant in instance.participants.all():
            if participant != request_sender:
                participants.append({
                            'user_pk': participant.pk,
                            'name': participant.profile.first_name,
                            'prof_pic': participant.profile.prof_pic.name
                })
        
        # Get the latest message (if any).
        try:
            last_message = MessageSerializer(
                    instance.messages.latest('timestamp')
            ).data
        except Message.DoesNotExist:
            last_message = ''
        
        chat['participants'] = participants
        chat['last_message'] = last_message

        return chat

