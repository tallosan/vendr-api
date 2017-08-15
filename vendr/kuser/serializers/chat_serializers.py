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
        fields = ('pk', 'sender', 'content', 'timestamp')


class ChatUserSerializer(serializers.RelatedField):
    
    ''' Custom representation of a User. For chat we only need the user's
        pk & their profile pic URL.
        Args:
            instance -- The user to be serialized.
    '''
    def to_representation(self, instance):
        
        kuser = {
                    'user_pk': instance.pk,
                    'prof_pic': instance.profile.prof_pic.name
        }

        return kuser


class ChatSerializer(serializers.ModelSerializer):
    
    participants = ChatUserSerializer(many=True, read_only=True)
    
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
