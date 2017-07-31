from rest_framework.views import APIView
from rest_framework.response import Response
from bd_elk.elastic_dsl import SrcIp


class TestApi(APIView):
    def get(self, request, format=None):
        s = SrcIp.search()
        response = s.scan()
        print('Total %d hits found.' % s.count())
        for h in response:
            print(h.to_dict())
        return Response("test")
