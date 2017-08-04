# -*- coding: UTF-8 -*-
from elasticsearch_dsl.connections import connections
from ultis.commons import ComFunc

# server connect
ELASTIC_HOST = "192.168.9.199"
ELASTIC_PORT = 9200
connections.create_connection(hosts=['{0}:{1}'.format(
    ELASTIC_HOST, ELASTIC_PORT
)])


class CommonEs(object):
    """
    es可以共用的函数
    """

    @classmethod
    def debug_query(cls, s):
        """
        debug search query dict
        :param s: search object
        :return:
        """
        print('=' * 30)
        print(ComFunc.to_json_string(s.to_dict()))
        print('=' * 30)
