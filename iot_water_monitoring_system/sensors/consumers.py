import logging
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print("WebSocket connection initiated")
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()
        # print(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        # print(f"WebSocket disconnected: {self.channel_name}, Close code: {close_code}")
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def receive(self, text_data):
        # print(f"WebSocket message received: {text_data}")
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "notifications",
            {
                "type": "send_notification",
                "message": data.get("message", "No message content"),
            },
        )

    async def send_notification(self, event):
        message = event["message"]
        # print(f"Sending notification: {message}")
        await self.send(text_data=json.dumps({"message": message}))
