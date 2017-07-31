from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, String, Long

ELASTIC_HOST = "192.168.33.35"
ELASTIC_PORT = 9200
connections.create_connection(hosts=['{0}:{1}'.format(
    ELASTIC_HOST, ELASTIC_PORT
)])


class SrcIp(DocType):
    flows = Long()
    bytes = Long()
    packets = Long()
    ip = String()

    class Meta:
        index = 'src-ip-stats-2017.07.31'
