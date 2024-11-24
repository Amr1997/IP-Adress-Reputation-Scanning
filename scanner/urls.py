from django.urls import path
from scanner.views import IPScannerView

urlpatterns = [
    path('scan/', IPScannerView.as_view(), name='ip_scan'),
]
