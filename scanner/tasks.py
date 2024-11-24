import requests
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 3})
def fetch_ip_info(self, ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "ip_scan", {"type": "scan.result", "result": response.json()}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'ip': ip}
