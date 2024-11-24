# scanner/routing.py
from django.urls import path
from scanner.consumers import ScanConsumer

websocket_urlpatterns = [
    path('ws/scan/', ScanConsumer.as_asgi()),
]
