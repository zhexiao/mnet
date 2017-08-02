# -*- coding: UTF-8 -*-
import json
from elasticsearch_dsl.connections import connections
from rest_framework.exceptions import APIException

# server connect
ELASTIC_HOST = "192.168.9.199"
ELASTIC_PORT = 9200
connections.create_connection(hosts=['{0}:{1}'.format(
    ELASTIC_HOST, ELASTIC_PORT
)])


class MnetError(APIException):
    """
    自定义error
    """
    status_code = 400
    default_detail = 'Unexcepted error.'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return self.detail


class CommonDoc(object):
    """
    common class for es
    """

    @classmethod
    def to_json_string(cls, _json):
        return json.dumps(_json)

    @classmethod
    def bytes_convert(cls, _bytes, _type='mb'):
        """
        byte to readable number
        :param _bytes:
        :param _type:
        :return:
        """
        if _type == 'gb':
            _d = _bytes/(1024*1024*1024)
        elif _type == 'mb':
            _d = _bytes / (1024 * 1024)
        elif _type == 'kb':
            _d = _bytes / 1024
        else:
            _d = _bytes

        return round(_d, 2)

    @classmethod
    def debug_query(cls, s):
        """
        debug search query dict
        :param s: search object
        :return:
        """
        print('=' * 30)
        print(cls.to_json_string(s.to_dict()))
        print('=' * 30)

    @classmethod
    def number_convert(cls, _number, _type=None):
        """
        number convert
        :param _number:
        :param _type:
        :return:
        """
        if _type == 'm':
            _d = _number / 1000000
        elif _type == 'k':
            _d = _number / 1000
        else:
            _d = _number

        return round(_d, 2)
