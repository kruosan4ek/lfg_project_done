"""
WebSocket consumers для live-чата LFG.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer для чата внутри LFG объявления.
    Комната называется 'chat_<post_id>'.
    """

    async def connect(self):
        """Подключение к WebSocket."""
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'chat_{self.post_id}'
        self.user = self.scope['user']

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        # Приветствие
        username = self.user.username if self.user.is_authenticated else 'Гость'
        await self.send(text_data=json.dumps({
            'type': 'system',
            'message': f'{username} присоединился к чату',
        }))

    async def disconnect(self, close_code):
        """Отключение от WebSocket."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        """Получение сообщения от клиента."""
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message = data.get('message', '').strip()
        if not message:
            return

        username = self.user.username if self.user.is_authenticated else 'Гость'

        # Рассылаем всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            },
        )

    async def chat_message(self, event):
        """Отправка сообщения клиенту."""
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'username': event['username'],
        }))