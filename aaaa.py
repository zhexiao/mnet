# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import json
from pprint import pprint
from socket import socket, AF_INET, SOCK_DGRAM


class SparkStreaming:
    # 定义时间duration
    batch_duration = 2
    window_duration = 15 * 2
    slide_duration = 5 * 2

    # 定义初始化需要的参数
    spark_master = "spark://spark-master:7077"
    zookeeper_host = 'zoo1:2181'
    group_id = 'spark-consumer'
    topics = {
        'mnet': 1
    }

    # 网络数据参数
    protocol_num = [6, 17]
    udp_buffer_size = 1024

    logstash_server_host = 'lg1'
    logstash_server_src_ip_port = 21561
    logstash_server_dst_ip_port = 21562
    logstash_server_src_ip_addr = (
        logstash_server_host, logstash_server_src_ip_port
    )
    logstash_server_dst_ip_addr = (
        logstash_server_host, logstash_server_dst_ip_port
    )

    def __init__(self):
        # 创建streaming context
        sc = SparkContext(master="spark://spark-master:7077",
                          appName="spark_streaming")
        ssc = StreamingContext(sc, 2)

        # 链接到kafka zookeeper
        dstream = KafkaUtils.createStream(
            ssc,
            'zoo1:2181',
            'spark-consumer',
            {
                'mnet': 1
            }
        )
        netflow_dstream = dstream.map(lambda ds: json.loads(ds[1]))

        # 打印数据
        # netflow_dstream.pprint()

        # 统计数据
        src_ip_stats, dst_ip_stats = self.count_protocol(netflow_dstream)

        # 对统计后的数据进行后续操作
        src_ip_stats.foreachRDD(
            lambda rdd: self.process_src_ip_result(rdd.collectAsMap())
        )
        dst_ip_stats.foreachRDD(
            lambda rdd: self.process_dst_ip_result(rdd.collectAsMap())
        )

        # 启动服务
        ssc.start()
        ssc.awaitTermination()

    def count_protocol(self, netflow_dstream):
        """
        统计IP地址数据
        :param netflow_dstream:
        :return:
        """
        # 过滤，只返回tcp和udp的DStream数据
        p_flow = netflow_dstream.filter(
            lambda n_dt: (n_dt['netflow']['protocol'] in self.protocol_num)
        )

        # 重新map一个DStream，以源IP为key组装起来
        src_ip_mapped = p_flow.map(lambda dt: (
            (dt['netflow']['ipv4_src_addr']),
            (1, dt['netflow']['in_pkts'], dt['netflow']['in_bytes'])
        ))
        dst_ip_mapped = p_flow.map(lambda dt: (
            (dt['netflow']['ipv4_dst_addr']),
            (1, dt['netflow']['in_pkts'], dt['netflow']['in_bytes'])
        ))

        # 先对数据做个小的统计
        src_ip_reduced = src_ip_mapped.reduceByKey(lambda v1, v2: (
            v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
        ))
        dst_ip_reduced = dst_ip_mapped.reduceByKey(lambda v1, v2: (
            v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
        ))

        # 然后对每30秒数据每10秒钟统计一次
        src_ip_stats = src_ip_reduced.window(
            self.window_duration, self.slide_duration
        ).reduceByKey(
            lambda v1, v2: (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])
        )
        dst_ip_stats = dst_ip_reduced.window(
            self.window_duration, self.slide_duration
        ).reduceByKey(
            lambda v1, v2: (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])
        )

        return src_ip_stats, dst_ip_stats

    def process_src_ip_result(self, result):
        """
        处理统计得到的src ip数据
        :return:
        """
        for ip, val in result.iteritems():
            json_data = {
                'ip': ip,
                'flows': val[0],
                'packets': val[1],
                'bytes': val[2]
            }
            pprint('src ip - ' * 50)
            pprint('+' * 50)
            pprint('+' * 50)
            pprint(json.dumps(json_data))
            pprint('+' * 50)
            pprint('+' * 50)
            pprint('src ip - ' * 50)

            self.send_src_ip_data(json.dumps(json_data))

    def process_dst_ip_result(self, result):
        """
        处理统计得到的dst ip数据
        :return:
        """
        for ip, val in result.iteritems():
            json_data = {
                'ip': ip,
                'flows': val[0],
                'packets': val[1],
                'bytes': val[2]
            }
            pprint('dst ip - ' * 50)
            pprint('+' * 50)
            pprint('+' * 50)
            pprint(json.dumps(json_data))
            pprint('+' * 50)
            pprint('+' * 50)
            pprint('dst ip -' * 50)

            self.send_dst_ip_data(json.dumps(json_data))

    def send_src_ip_data(self, json_string):
        """
        使用网络传输src ip数据到input server的logstash
        :param json_string:
        :return:
        """
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_socket.sendto(json_string, self.logstash_server_src_ip_addr)
        except socket.error:
            pprint("cannot connect to udp server")
        finally:
            udp_socket.close()

    def send_dst_ip_data(self, json_string):
        """
        使用网络传输dst ip数据到input server的logstash
        :param json_string:
        :return:
        """
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_socket.sendto(json_string, self.logstash_server_dst_ip_addr)
        except socket.error:
            pprint("cannot connect to udp server")
        finally:
            udp_socket.close()


# 运行类
SparkStreaming()
