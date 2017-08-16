import json
from django.core.cache import cache


class ComFunc(object):
    """
    可以通用的函数
    """

    @classmethod
    def cache(cls, key, **kwargs):
        """
        读取，与写入 cache数据
        :param key:
        :return:
        """
        update = kwargs.get('update', False)
        writing_data = kwargs.get('data')
        # 3600秒的默认过期时间
        duration = kwargs.get('duration', 3600)

        # 如果不存在写入数据，则默认当作读取操作
        if not writing_data:
            json_res = cache.get(key)
            if json_res and not update:
                return json_res
            return False
        # 当作写入操作
        else:
            cache.set(key, writing_data, duration)

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
        if not _bytes:
            return 0

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
        if not _number:
            return 0

        if _type == 'm':
            _d = _number / 1000000
        elif _type == 'k':
            _d = _number / 1000
        else:
            _d = _number

        return round(_d, 2)
