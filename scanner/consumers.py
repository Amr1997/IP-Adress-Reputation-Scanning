from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ScanConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("ip_scan", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("ip_scan", self.channel_name)

    async def scan_result(self, event):
        await self.send(text_data=json.dumps(event['result']))
