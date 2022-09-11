
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from  django.contrib.auth.models import User
from chat.models import Group, Messages

class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print("websocket is connected")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        
        command = text_data_json['command']
        
        send_by = text_data_json['send_by_user']
        send_to_group = text_data_json['group']
        
        if command == "send":
            message = text_data_json['message']
            grp = Group.objects.get(id=send_to_group)
            user = User.objects.get(username=send_by)
            Messages.objects.create(
                group = grp,
                sender = user,
                text = message
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender' : send_by,
                    'command' : 'send'
                }
            )

    # Receive message from room group
    def chat_message(self, messages):

        print("chat message is called")
        message = messages['message']
        sender = messages['sender']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'command' : 'send'
        }))

