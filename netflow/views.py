from rest_framework.views import APIView
from rest_framework.response import Response
from bd_elk.elastic_dsl import Logs


class TestApi(APIView):
    def get(self, request, format=None):
        # s = ElasticDsl().search(index="src-ip-stats-2017.07.27")
        # s.query("match", ip="36.110.147.35")
        # response = s.execute()
        # print(s)
        # print(json.dumps(s.to_dict()))

        dt = Logs.get(id="AV2EG7SSKstPrjF46rlT")
        print(dt.to_dict())

        s = Logs.search().query("match", ip="36.110.147.35")
        response = s.scan()
        print('Total %d hits found.' % s.count())
        for h in response:
            print(h)
        return Response("test")
