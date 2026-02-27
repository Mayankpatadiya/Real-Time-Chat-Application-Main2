import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from chat.models import Chat, Message, ChatGroup, UserProfile

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'online_status'
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.update_user_status(True)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'status_update',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'online': True
                }
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.update_user_status(False)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'status_update',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'online': False
                }
            )
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def status_update(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def update_user_status(self, status):
        UserProfile.objects.filter(user=self.user).update(is_online=status)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("🔥 WebSocket connect attempt")

        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        if not await self.is_chat_member():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"✅ WebSocket connected to room: {self.room_group_name} for user: {self.user.username}")


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        # Handle typing events
        if 'typing' in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_message',
                    'typing': data['typing'],
                    'sender': self.user.username,
                    'sender_id': self.user.id,
                }
            )
            return

        # Handle file messages (broadcast only, file already saved via HTTP)
        if data.get('type') == 'file_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'file_message',
                    'file_url': data['file_url'],
                    'file_name': data['file_name'],
                    'is_image': data['is_image'],
                    'caption': data.get('caption', ''),
                    'sender': self.user.username,
                    'sender_id': self.user.id,
                }
            )
            return

        message = (data.get('message') or '').strip()
        if not message:
            return

        # Save message to database
        await self.save_message(message)
        print(f"DEBUG: Message received and saved: {message[:30]}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'sender_id': self.user.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
        }))

    async def typing_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'typing': event['typing'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
        }))

    async def file_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'file_message',
            'file_url': event['file_url'],
            'file_name': event['file_name'],
            'is_image': event['is_image'],
            'caption': event.get('caption', ''),
            'sender': event['sender'],
            'sender_id': event['sender_id'],
        }))

    @database_sync_to_async
    def is_chat_member(self):
        return Chat.objects.filter(id=self.chat_id).filter(
            Q(user1=self.user) | Q(user2=self.user)
        ).exists()

    @database_sync_to_async
    def save_message(self, message):
        chat = Chat.objects.get(id=self.chat_id)
        Message.objects.create(
            chat=chat,
            sender=self.user,
            content=message,
            message_type='text'
        )


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f'group_{self.group_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        if not await self.is_group_member():
            await self.close()
            return

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
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        # Handle typing events
        if 'typing' in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_message',
                    'typing': data['typing'],
                    'sender': self.user.username,
                    'sender_id': self.user.id,
                }
            )
            return

        # Handle file messages (broadcast only, file already saved via HTTP)
        if data.get('type') == 'file_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'file_message',
                    'file_url': data['file_url'],
                    'file_name': data['file_name'],
                    'is_image': data['is_image'],
                    'caption': data.get('caption', ''),
                    'sender': self.user.username,
                    'sender_id': self.user.id,
                }
            )
            return

        message = (data.get('message') or '').strip()
        if not message:
            return

        # Save message to database
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'sender_id': self.user.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
        }))

    async def typing_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'typing': event['typing'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
        }))

    async def file_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'file_message',
            'file_url': event['file_url'],
            'file_name': event['file_name'],
            'is_image': event['is_image'],
            'caption': event.get('caption', ''),
            'sender': event['sender'],
            'sender_id': event['sender_id'],
        }))

    @database_sync_to_async
    def is_group_member(self):
        try:
            group = ChatGroup.objects.get(id=self.group_id)
            return group.members.filter(user=self.user).exists() or group.created_by.user == self.user
        except ChatGroup.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, message):
        group = ChatGroup.objects.get(id=self.group_id)
        Message.objects.create(
            group=group,
            sender=self.user,
            content=message,
            message_type='text'
        )
