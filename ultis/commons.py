import json


class ComFunc(object):
    """
    可以通用的函数
    """

    @classmethod
    def to_json_string(cls, _json):
        return json.dumps(_json)

    @classmethod
    def bytes_convert(cls, _bytes, _type='mb'):
        """
        对bytes进行转换
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
    def number_convert(cls, _number, _type=None):
        """
        数字进行转换
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
