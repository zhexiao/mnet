from elasticsearch_dsl import DocType
from bd_elk.common_es import CommonEs
from ultis.commons import ComFunc


class CommonIp(DocType, CommonEs):
    # todo should use pandas to do json format
    """
    基于Ip 数据公用的类
    """

    # 指定的类型（src，dst...）
    _type = None

    @classmethod
    def get_total_stats(cls, **kwargs):
        """
        get ip stats
        :return:
        """
        cache_key = 'ip-stats-{0}'.format(cls._type)
        json_res = ComFunc.cache(cache_key)

        if not json_res:
            s = cls.search().extra(size=0)
            s.aggs.bucket('ip_terms', 'terms', field='ip.keyword')
            s.aggs['ip_terms'].metric('flows_per_ip', 'sum', field='flows')
            s.aggs['ip_terms'].metric('bytes_per_ip', 'sum', field='bytes')
            s.aggs['ip_terms'].metric('packets_per_ip', 'sum', field='packets')

            # cls.debug_query(s)
            response = s.execute()

            json_res = []
            for stats in response.aggregations.ip_terms.buckets:
                json_res.append({
                    'ip': stats.key,
                    'flows': ComFunc.number_convert(
                        stats.flows_per_ip.value, 'k'
                    ),
                    'packets': ComFunc.number_convert(
                        stats.packets_per_ip.value, 'k'
                    ),
                    'bytes': ComFunc.bytes_convert(
                        stats.bytes_per_ip.value, 'mb'
                    )
                })

            ComFunc.cache(cache_key, data=json_res)
        return json_res

    @classmethod
    def get_ip_date_history(cls, **kwargs):
        """
        读取某IP基于时间段的数据
        :param kwargs:
        :return:
        """
        ip_str = kwargs.get('ip')
        _interval = kwargs.get('interval', '1h')

        cache_key = 'date-record-{0}-{1}'.format(
            ip_str, cls._type
        )
        json_res = ComFunc.cache(cache_key)

        if not json_res:
            s = cls.search().query("match", ip=ip_str).extra(size=0)
            s.aggs.bucket(
                'ip_per_hour', 'date_histogram', field='@timestamp',
                interval=_interval, time_zone=cls.time_zone
            )

            s.aggs['ip_per_hour'].metric(
                'flows_per_hour', 'avg', field='flows'
            )
            s.aggs['ip_per_hour'].metric(
                'bytes_per_hour', 'avg', field='bytes'
            )
            s.aggs['ip_per_hour'].metric(
                'packets_per_hour', 'avg', field='packets'
            )

            # cls.debug_query(s)
            response = s.execute()

            json_res = []
            for dt in response.aggregations.ip_per_hour.buckets:
                datetime = dt.key_as_string
                json_res.append({
                    'datetime': datetime,
                    'flows': ComFunc.number_convert(
                        dt.flows_per_hour.value, 'k'
                    ),
                    'packets': ComFunc.number_convert(
                        dt.packets_per_hour.value, 'k'
                    ),
                    'bytes': ComFunc.bytes_convert(
                        dt.bytes_per_hour.value, 'mb'
                    )
                })

            ComFunc.cache(cache_key, data=json_res)
        return json_res

    @classmethod
    def get_top_date_history(cls, **kwargs):
        """
        按时间段，读取top7 IP的平均数据流
        :param kwargs:
        :return:
        """
        # 默认获取每1小时的数据
        _interval = kwargs.get('interval', '1h')

        cache_key = 'all-ip-date-record-{0}'.format(cls._type)
        json_res = ComFunc.cache(cache_key)

        if not json_res:
            s = cls.search().extra(size=0)
            s.aggs.bucket(
                'ips', 'terms', field='ip.keyword', size=7,
                order={"avg_flow": "desc"}
            )
            s.aggs['ips'].metric('avg_flow', 'avg', field='flows')
            s.aggs['ips'].bucket(
                'date_avg_flow', 'date_histogram', field='@timestamp',
                time_zone=cls.time_zone, interval=_interval
            )
            s.aggs['ips']['date_avg_flow'].metric(
                'ip_avg_flow', 'avg', field='flows'
            )

            # cls.debug_query(s)
            response = s.execute()

            json_res = {}
            for dt in response.aggregations.ips.buckets:
                _ip = dt.key
                json_res[_ip] = []
                for date_flow in dt.date_avg_flow.buckets:
                    json_res[_ip].append({
                        'avg_flow': ComFunc.number_convert(
                            date_flow.ip_avg_flow.value
                        ),
                        'datetime': date_flow.key_as_string
                    })

            ComFunc.cache(cache_key, data=json_res)
        return json_res
