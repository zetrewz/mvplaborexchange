import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from chat.models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['application_id']
        self.room_group_name = f'chat_{self.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await database_sync_to_async(ChatMessage.objects.create)(
            user=self.user,
            content=message,
            room_group_name=self.room_group_name
        )

        now = timezone.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         self.id = self.scope['url_route']['kwargs']['application_id']
#         self.room_group_name = f'chat_{self.id}'
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#         await self.send_chat_history()
#
#     @sync_to_async
#     def send_chat_history(self):
#         chat_history = ChatMessage.objects.filter(
#             room_group_name=self.room_group_name)
#         messages = []
#
#         for message in chat_history:
#             messages.append({
#                 'type': 'chat_message',
#                 'message': message.content,
#                 'user': message.user.username,
#                 'datetime': message.timestamp.isoformat(),
#             })
#
#         self.send(text_data=json.dumps(messages))
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         await database_sync_to_async(ChatMessage.objects.create)(
#             user=self.user,
#             content=message,
#             room_group_name=self.room_group_name
#         )
#
#         now = timezone.now()
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'user': self.user.username,
#                 'datetime': now.isoformat(),
#             }
#         )
#
#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps(event))
