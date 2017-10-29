#
# Chat views.
#
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from kuser.models import Chat, Message
from kuser.serializers import ChatSerializer, MessageSerializer

import kuser.permissions as kuser_permissions

User = get_user_model()


'''   Chat list view. '''
class ChatList(APIView):

    serializer_class   = ChatSerializer
    permission_classes = ( permissions.IsAuthenticated,
                           kuser_permissions.ChatListPermissions
    )

    ''' Gets all Chats that a given user is part of.
        Args:
            pk -- The primary key of the user we're querying over.
    '''
    def get_queryset(self, pk):

        queryset = User.objects.get(pk=pk).chat_set.all()
        return queryset

    ''' Handles LIST / GET requests.
        Args:
            request: The GET request.
            pk: The primary key of the user we're querying over.
            *format: Specified data format.
    ''' 
    def get(self, request, pk, format=None):
        
        queryset = self.get_queryset(pk)
        self.check_object_permissions(request, User.objects.get(pk=pk))
        context = {'sender': request.user}
        
        chats = []
        for convo in queryset:
            chats.append(self.serializer_class(
                convo,
                context=context).data
        )

        # Add the number of uonpened chats to our response.
        response = Response({'chats': chats})
        response.data['unopened_count'] = Chat.objects.\
                filter(opened=False).count()

        return response
    
    ''' Handles POST requests.
        Args:
            request: The POST request.
            user_pk: The primary key of the user we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, pk, format=None):

        self.check_object_permissions(request, User.objects.get(pk=pk))
        context = {'sender': request.user}

        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatDetail(APIView):

    serializer_class = ChatSerializer
    permission_classes = ( permissions.IsAuthenticated,
                           kuser_permissions.ChatDetailPermissions
    )

    ''' Return the Chat object with the given pk. Raises an exception if
        none exists.
        Args:
            chat_pk -- The chat object's primary key.
    '''
    def get_object(self, pk, chat_pk):
        
        try:
            chat = Chat.objects.get(pk=chat_pk)
            self.check_object_permissions(self.request, chat)
            
            # Update Chat status.
            if not chat.opened:
                chat.opened = True; chat.save()
            
            return chat

        except Chat.DoesNotExist:
            error_msg = {'error': 'chat with id={} does not exist'}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = status.HTTP_400_BAD_REQUEST; raise dne_exc
    
    ''' Handles GET requests on Chat models.
        Args:
            request: The GET request.
            pk: The user that the chat belongs to.
            chat_pk: The primary key of the chat to get.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, pk, chat_pk, format=None):
        
        chat = self.get_object(pk, chat_pk)
        serializer = self.serializer_class(chat)

        return Response(serializer.data)
    
    ''' Handles DELETE requests on Chat models.
        Args:
            request: The DELETE request.
            pk: The user that the chat belongs to.
            chat_pk: The primary key of the chat to get.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, pk, chat_pk, format=None):

        chat = self.get_object(pk, chat_pk)
        chat.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageList(APIView):
    
    serializer_class = MessageSerializer
    permission_classes = ( permissions.IsAuthenticated,
                           kuser_permissions.MessageListPermissions
    )

    ''' Gets all Messages in a given chat.
        Args:
            chat_pk -- The primary key of the Chat we're querying over.
    '''
    def get_queryset(self, chat_pk):
    
        queryset = Chat.objects.get(pk=chat_pk).messages.all()
        return queryset

    ''' Handles LIST / GET requests.
        Args:
            request: The GET request.
            pk: The primary key of the user we're querying over.
            chat_pk: The primary key of the chat we're querying over.
            *format: Specified data format.
    ''' 
    def get(self, request, pk, chat_pk, format=None):

        self.check_object_permissions(request, Chat.objects.get(pk=chat_pk))
        queryset = self.get_queryset(chat_pk)
        
        response = []
        for message in queryset:
            response.append(self.serializer_class(message).data)

        return Response(response)
    
    ''' Handles POST requests.
        Args:
            request: The POST request.
            pk: The primary key of the user we're querying over.
            chat_pk: The primary key of the chat we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, pk, chat_pk, format=None):
        
        chat = Chat.objects.get(pk=chat_pk)
        self.check_object_permissions(request, chat)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_name = '{} {}'.format(request.user.profile.first_name,
                                       request.user.profile.last_name)
            serializer.save(
                    sender=request.user.pk,
                    sender_name=user_name,
                    chat=chat
            )
            chat.opened = False; chat.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

