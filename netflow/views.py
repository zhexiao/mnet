# -*- coding: UTF-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from bd_elk.stats_ip import (
    SrcIp,
    DstIp,
    Netflow
)
from bd_elk.common_doc import MnetError


class TestApi(APIView):
    def get(self, request, format=None):
        Netflow.get_stats_by_ip(ip='10.0.2.15')
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
            raise MnetError('请指定type（src, dst）')
        return Response(res)


class IpDateRecord(APIView):
    """
    Ip record by date
    """
    def get(self, request, format=None):
        type = request.GET.get('type')
        ip = request.GET.get('ip')

        if type == 'src':
            if not ip:
                res = SrcIp.get_all_date_record(type=type)
            else:
                res = SrcIp.get_date_record(ip=ip, type=type)
        elif type == 'dst':
            if not ip:
                res = DstIp.get_all_date_record(type=type)
            else:
                res = DstIp.get_date_record(ip=ip, type=type)
        else:
            raise MnetError('请指定type（src, dst）')

        return Response(res)


class NetflowIpStats(APIView):
    def get(self, request, format=None):
        _ip = request.GET.get('ip')
        _type = request.GET.get('type')

        if not _ip:
            raise MnetError('请指定IP')

        if _type == 'src':
            res = Netflow.get_stats_by_src_ip(ip=_ip)
        elif _type == 'dst':
            res = Netflow.get_stats_by_src_ip(ip=_ip)
        else:
            raise MnetError('请指定type（src, dst）')
        return Response(res)
