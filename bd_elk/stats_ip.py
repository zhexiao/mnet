# -*- coding: UTF-8 -*-
from elasticsearch_dsl import DocType, Keyword, Long
from bd_elk.common_doc import CommonDoc
from django.core.cache import cache


class CommonIp(DocType):
    # todo should use pandas to do json format
    """
    Common Ip Func
    """
    local_pc_ip = ['10.0.2.15', '10.0.2.3']

    @classmethod
    def get_stats(cls, **kwargs):
        """
        get ip stats
        :return:
        """
        type = kwargs.get('type')

        cache_key = 'ip-stats-{0}'.format(type)
        json_res = cache.get(cache_key)

        if not json_res:
            s = cls.search().extra(size=0)
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

            cache.set(cache_key, json_res)

        return json_res

    @classmethod
    def get_date_record(cls, **kwargs):
        """
        get ip records and group by date
        :param kwargs:
        :return:
        """
        ip_str = kwargs.get('ip')
        _type = kwargs.get('type')
        _interval = kwargs.get('interval', '1h')

        cache_key = 'date-record-{0}-{1}'.format(
            ip_str, _type
        )
        json_res = cache.get(cache_key)

        if not json_res:
            s = cls.search().query("match", ip=ip_str).extra(size=0)

            # agg data
            s.aggs.bucket('ip_per_hour', 'date_histogram', field='@timestamp',
                          interval=_interval)
            s.aggs['ip_per_hour'].bucket('ip_term', 'terms',
                                         field='ip.keyword')
            s.aggs['ip_per_hour']['ip_term'].metric('flows_per_hour', 'sum',
                                                    field='flows')
            s.aggs['ip_per_hour']['ip_term'].metric('bytes_per_hour', 'sum',
                                                    field='bytes')
            s.aggs['ip_per_hour']['ip_term'].metric('packets_per_hour', 'sum',
                                                    field='packets')

            # cls.debug_query(s)
            response = s.execute()

            json_res = {'datetime': [], 'flows': [],
                        'bytes': [], 'packets': []}
            for dt in response.aggregations.ip_per_hour.buckets:
                datetime = dt.key_as_string
                for stats in dt.ip_term.buckets:
                    json_res['datetime'].append(datetime)
                    json_res['flows'].append(stats.flows_per_hour.value)
                    json_res['bytes'].append(
                        cls.bytes_convert(stats.bytes_per_hour.value, 'mb')
                    )
                    json_res['packets'].append(
                        cls.number_convert(stats.packets_per_hour.value, 'k')
                    )
            cache.set(cache_key, json_res)
        return json_res

    @classmethod
    def get_all_date_record(cls, **kwargs):
        """
        get all ip adress date record
        :param kwargs:
        :return:
        """
        _type = kwargs.get('type')
        _interval = kwargs.get('interval', '1h')

        cache_key = 'all-ip-date-record-{0}'.format(_type)
        json_res = cache.get(cache_key)

        if not json_res:
            s = cls.search().extra(size=0)
            # agg data, 1:ips, 2:group by date, 3:ip-avg flows
            s.aggs.bucket('ips', 'terms', field='ip.keyword', size=7,
                          exclude=cls.local_pc_ip)
            s.aggs['ips'].bucket('date_avg_flow', 'date_histogram',
                                 field='@timestamp',
                                 interval=_interval)
            s.aggs['ips']['date_avg_flow'].metric('ip_avg_flow', 'avg',
                                                  field='flows')

            # cls.debug_query(s)
            response = s.execute()

            json_res = {'datetime': []}
            for dt in response.aggregations.ips.buckets:
                _ip = dt.key
                json_res[_ip] = {'avg_flow': []}
                datetime_len = len(dt.date_avg_flow.buckets)
                for date_flow in dt.date_avg_flow.buckets:
                    if datetime_len != len(json_res['datetime']):
                        json_res['datetime'].append(
                            date_flow.key_as_string
                        )

                    json_res[_ip]['avg_flow'].append(
                        date_flow.ip_avg_flow.value
                    )

            cache.set(cache_key, json_res)
        return json_res


class SrcIp(CommonDoc, CommonIp):
    """
    src ip doc class
    """
    flows = Long()
    bytes = Long()
    packets = Long()
    ip = Keyword()

    class Meta:
        index = 'src-ip-stats-2017.08.01'


class DstIp(CommonDoc, CommonIp):
    """
    dst ip doc class
    """
    flows = Long()
    bytes = Long()
    packets = Long()
    ip = Keyword()

    class Meta:
        index = 'dst-ip-stats-2017.08.01'
