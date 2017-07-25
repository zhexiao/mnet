# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
from pprint import pprint


class SparkStreaming:
    # 定义时间duration
    batch_duration = 2
    window_duration = 15*2
    slide_duration = 5*2

    # 定义初始化需要的参数
    spark_master = "spark://192.168.33.32:7077"
    zookeeper_host = '192.168.33.31:2181'
    group_id = 'spark-consumer'
    topics = {
        'mnet': 1
    }

    # 网络数据参数
    protocol_num = [6, 17]

    def __init__(self):
        # 创建streaming context
        sc = SparkContext(master=self.spark_master, appName="spark_streaming")
        ssc = StreamingContext(sc, self.batch_duration)

        # 链接到kafka zookeeper
        dstream = KafkaUtils.createStream(
            ssc, self.zookeeper_host, self.group_id, self.topics)
        netflow_dstream = dstream.map(lambda ds: json.loads(ds[1]))

        # 打印数据
        # netflow_dstream.pprint()

        # 统计数据
        p_stats = self.count_protocol(netflow_dstream)

        # 对统计后的数据进行后续操作
        p_stats.foreachRDD(
            lambda rdd: self.process_result(rdd.collectAsMap())
        )

        # 启动服务
        ssc.start()
        ssc.awaitTermination()

    def count_protocol(self, netflow_dstream):
        """
        给每个MAC地址统计protocol
        :param netflow_dstream:
        :return:
        """
        # 过滤，只返回tcp和udp的DStream数据
        p_flow = netflow_dstream.filter(
            lambda n_dt: (n_dt['netflow']['protocol'] in self.protocol_num)
        )

        # 重新map一个DStream，以源IP为key组装起来
        p_mapped = p_flow.map(lambda dt: ((dt['netflow']['ipv4_src_addr']), (
            1, dt['netflow']['in_pkts'], dt['netflow']['in_bytes']
        )))

        # 先对数据做个小的统计
        p_reduced = p_mapped.reduceByKey(lambda v1, v2: (
            v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]
        ))

        # 然后对数据按时间区间(每30秒)做个大的统计
        p_stats = p_reduced.window(
            self.window_duration, self.slide_duration
        ).reduceByKey(
            lambda v1, v2: (v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2])
        )

        return p_stats

    def process_result(self, result):
        """
        处理统计得到的数据
        :return:
        """
        for ip, val in result.iteritems():
            pprint('+'*50)
            pprint(ip)
            pprint(val)
            pprint('+' * 50)


# 运行类
SparkStreaming()
