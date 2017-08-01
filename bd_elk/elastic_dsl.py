import json
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Keyword, Long

ELASTIC_HOST = "192.168.33.35"
ELASTIC_PORT = 9200
connections.create_connection(hosts=['{0}:{1}'.format(
    ELASTIC_HOST, ELASTIC_PORT
)])


class CommonDoc(object):
    """
    common class for es
    """
    @classmethod
    def to_json_string(cls, _json):
        return json.dumps(_json)


class SrcIp(DocType, CommonDoc):
    """
    src ip doc class
    """
    flows = Long()
    bytes = Long()
    packets = Long()
    ip = Keyword()

    class Meta:
        index = 'src-ip-stats-2017.07.31'

    @classmethod
    def search_all(cls):
        """
        search all docs
        :return:
        """
        s = cls.search()
        response = s.scan()
        print(cls.to_json_string(s.to_dict()))
        print('Total %d hits found.' % s.count())
        for h in response:
            print(h.to_dict())

    @classmethod
    def get_ip_flows(cls):
        """
        get flows group by ip
        :return:
        """
        s = cls.search()
        s.aggs.bucket('ip_terms', 'terms', field='ip')
        s.aggs['ip_terms'].metric('flows_per_ip', 'sum', field='flows')
        print(cls.to_json_string(s.to_dict()))
