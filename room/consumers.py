import json
from django.views.decorators.csrf import csrf_exempt


from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

# @csrf_exempt
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()



    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # async def websocket_disconnect(self, message):
    #     """
    #     Called when the WebSocket closes for any reason.
    #     """
    #     await self.disconnect()


    async def receive(self, text_data):
        data = json.loads(text_data)
        message  = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "room": room
            }
        )

   
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room
        }))
    
    @sync_to_async
    def save_message(self, username, room, message):
        from django.contrib.auth.models import User
        from .models import Room,Message
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        
        Message.objects.create(user=user, room=room,  content=message,)




