from .common import CommonIp
from elasticsearch_dsl import Keyword, Long


class SrcIp(CommonIp):
    """
    src ip
    """
    flows = Long()
    bytes = Long()
    packets = Long()
    ip = Keyword()

    class Meta:
        index = 'src-ip-stats-2017.08.02'
