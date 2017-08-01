import json
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Keyword, Long

ELASTIC_HOST = "192.168.9.199"
ELASTIC_PORT = 9200
connections.create_connection(hosts=['{0}:{1}'.format(
    ELASTIC_HOST, ELASTIC_PORT
)])


class CommonDoc(object):
    """
    common class for es
    """

    local_pc_ip = ['10.0.2.15', '10.0.2.3']

    @classmethod
    def to_json_string(cls, _json):
        return json.dumps(_json)

    @classmethod
    def bytes_convert(cls, _bytes, _type='mb'):
        """
        byte to mb
        :param _bytes:
        :param _type:
        :return:
        """
        if _type == 'gb':
            _d = _bytes/(1024*1024*1024)
        elif _type == 'kb':
            _d = _bytes / 1024
        _d = _bytes/(1024*1024)

        return round(_d, 2)


class SrcIp(DocType, CommonDoc):
    """
    src ip doc class
    """
    flows = Long()
    bytes = Long()
    packets = Long()
    ip = Keyword()

    class Meta:
        index = 'src-ip-stats-2017.08.01'

    @classmethod
    def debug_query(cls, s):
        """
        debug search query dict
        :param s:
        :return:
        """
        print('='*30)
        print(cls.to_json_string(s.to_dict()))
        print('=' * 30)

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
    def get_ip_stats(cls):
        """
        get ip stats
        :return:
        """
        s = cls.search()
        s.aggs.bucket('ip_terms', 'terms', field='ip.keyword',
                      exclude=cls.local_pc_ip)
        s.aggs['ip_terms'].metric('flows_per_ip', 'sum', field='flows')
        s.aggs['ip_terms'].metric('bytes_per_ip', 'sum', field='bytes')
        s.aggs['ip_terms'].metric('packets_per_ip', 'sum', field='packets')

        # cls.debug_query(s)

        response = s.execute()
        json_res = {'ip': [], 'flows': [], 'bytes': [], 'packets': []}
        for stats in response.aggregations.ip_terms.buckets:
            json_res['ip'].append(stats.key)
            json_res['flows'].append(stats.flows_per_ip.value)
            json_res['bytes'].append(
                cls.bytes_convert(stats.bytes_per_ip.value, 'kb')
            )
            json_res['packets'].append(stats.packets_per_ip.value)

        return json_res
