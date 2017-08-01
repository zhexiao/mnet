from rest_framework.views import APIView
from rest_framework.response import Response
from bd_elk.elastic_dsl import SrcIp


class TestApi(APIView):
    def get(self, request, format=None):
        SrcIp.get_ip_stats()
        return Response("test")


class SrcIpStats(APIView):
    def get(self, request, format=None):
        res = SrcIp.get_ip_stats()
        return Response(res)
