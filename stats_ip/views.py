# -*- coding: UTF-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from bd_elk.factory import EsFactory


class TestApi(APIView):
    def get(self, request, format=None):
        return Response("test")


class TotalStats(APIView):
    def get(self, request, format=None):
        _type = request.GET.get('type')
        res = EsFactory.ip_init(type=_type).get_total_stats()
        return Response(res)


class DateHistory(APIView):
    def get(self, request, format=None):
        _type = request.GET.get('type')
        ip = request.GET.get('ip')

        _class = EsFactory.ip_init(type=_type)
        if not ip:
            res = _class.get_top_date_history()
        else:
            res = _class.get_ip_date_history(ip=ip)

        return Response(res)
