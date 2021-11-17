import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'binary01'
        self.room_group_name = 'chat_binary01'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        password = text_data_json['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            Chat.objects.create(user=user, username=user.username, message=message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        chat_messages = Chat.objects.all().order_by('-id').values()[:20]
        chat_messages = reversed(chat_messages)
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'messages': list(chat_messages)
        }))