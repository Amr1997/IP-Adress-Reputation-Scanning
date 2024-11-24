import ipaddress
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scanner.tasks import fetch_ip_info


class IPScannerView(APIView):
    def post(self, request):
        ips = request.data.get('ips', [])
        if not isinstance(ips, list):
            return Response({'error': 'Invalid input format. Provide a list of IPs.'}, status=status.HTTP_400_BAD_REQUEST)
        
        valid_ips, invalid_ips = [], []
        for ip in ips:
            try:
                ipaddress.ip_address(ip)
                valid_ips.append(ip)
            except ValueError:
                invalid_ips.append(ip)
        
        if invalid_ips:
            return Response({'error': 'Invalid IPs detected.', 'invalid_ips': invalid_ips}, status=status.HTTP_400_BAD_REQUEST)
        
        task_ids = [fetch_ip_info.delay(ip).id for ip in valid_ips]
        return Response({'message': 'Tasks queued.', 'task_ids': task_ids}, status=status.HTTP_200_OK)
