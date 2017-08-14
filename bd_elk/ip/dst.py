from .common import CommonIp
from elasticsearch_dsl import Keyword, Long


class DstIp(CommonIp):
    """
    dst ip
    """
    flows = Long()
    bytes = Long()
    packets = Long()
    ip = Keyword()

    class Meta:
        index = 'dst-ip-stats-2017.08.02'
