from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.hotel_id = self.scope['url_route']['kwargs']['hotel_id']
        self.room_group_name = f'chat_{self.hotel_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if 'content' not in text_data_json:
            return

        message = text_data_json['content']
        user_id = text_data_json.get('userId')
        avatar_url = text_data_json.get('avatarUrl')

        print(f"Received message: {message}, userId: {user_id}, avatarUrl: {avatar_url}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'avatarUrl': avatar_url,
                'message': message,
                'userId': user_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['userId']
        avatar_url = event['avatarUrl']

        await self.send(text_data=json.dumps({
            'content': message,
            'userId': user_id,
            'avatarUrl': avatar_url,
        }))
