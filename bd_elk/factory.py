from ultis.exceptions import MnetException
from bd_elk.stats_ip import (
    SrcIp,
    DstIp,
    NetflowRaw
)


class EsFactory(object):

    @classmethod
    def ip_init(cls, **kwargs):
        _type = kwargs.get('type')

        # 按类型返回对应的类
        if _type == 'src':
            _class = SrcIp
        elif _type == 'dst':
            _class = DstIp
        elif _type == 'netflow_raw':
            _class = NetflowRaw
        else:
            raise MnetException('需要指定type')

        # 分配参数
        _class._type = _type

        return _class
