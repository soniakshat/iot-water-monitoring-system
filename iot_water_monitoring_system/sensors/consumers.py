from channels.generic.websocket import AsyncWebsocketConsumer
import json

class WaterQualityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("water_quality_alerts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("water_quality_alerts", self.channel_name)

    async def send_water_quality_alert(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))