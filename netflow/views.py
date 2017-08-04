# -*- coding: UTF-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from ultis.exceptions import MnetException
from bd_elk.factory import EsFactory


class TestApi(APIView):
    def get(self, request, format=None):
        return Response("test")


class IpStats(APIView):
    """
    IP stats
    """
    def get(self, request, format=None):
        _type = request.GET.get('type')
        res = EsFactory.ip_init(type=_type).get_stats()
        return Response(res)


class IpDateRecord(APIView):
    """
    Ip record by date
    """
    def get(self, request, format=None):
        _type = request.GET.get('type')
        ip = request.GET.get('ip')

        _class = EsFactory.ip_init(type=_type)
        if not ip:
            res = _class.get_all_date_record()
        else:
            res = _class.get_date_record(ip=ip)

        return Response(res)


class NetflowIpStats(APIView):
    def get(self, request, format=None):
        _ip = request.GET.get('ip')

        if not _ip:
            raise MnetException('请指定IP')

        res = EsFactory.ip_init(type='netflow_raw').get_stats_by_src_ip(ip=_ip)
        return Response(res)
