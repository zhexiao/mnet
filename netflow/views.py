# -*- coding: UTF-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from bd_elk.stats_ip import SrcIp, DstIp
from bd_elk.common_doc import MnetError


class TestApi(APIView):
    def get(self, request, format=None):
        SrcIp.get_ip_stats()
        return Response("test")


class IpStats(APIView):
    """
    IP stats
    """
    def get(self, request, format=None):
        type = request.GET.get('type')
        if type == 'src':
            res = SrcIp.get_stats(type=type)
        elif type == 'dst':
            res = DstIp.get_stats(type=type)
        else:
            raise MnetError('请指定type（src, dst）。')
        return Response(res)


class IpDateRecord(APIView):
    """
    Ip record by date
    """
    def get(self, request, format=None):
        type = request.GET.get('type')
        ip = request.GET.get('ip')
        if not ip:
            raise MnetError('ip不存在')

        if type == 'src':
            res = SrcIp.get_date_record(ip=ip, type=type)
        elif type == 'dst':
            res = DstIp.get_date_record(ip=ip, type=type)
        else:
            raise MnetError('请指定type（src, dst）。')

        return Response(res)
