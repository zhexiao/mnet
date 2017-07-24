# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


class SparkStreaming:
    spark_master = "spark://192.168.33.32:7077"
    zookeeper_host = '192.168.33.31:2181'
    group_id = 'spark-consumer'
    topics = {
        'mnet': 1
    }

    def __init__(self):
        # 创建streaming context
        sc = SparkContext(master=self.spark_master, appName="spark_streaming")
        ssc = StreamingContext(sc, 2)

        # 链接到kafka zookeeper
        dstream = KafkaUtils.createStream(
            ssc, self.zookeeper_host, self.group_id, self.topics)
        netflow_dstream = dstream.map(lambda ds: ds[1])

        # 打印数据
        # netflow_dstream.pprint()
        self.count_protocol(netflow_dstream)

        # 启动服务
        ssc.start()
        ssc.awaitTermination()

    @staticmethod
    def count_protocol(netflow_dstream):
        """
        给每个MAC地址统计protocol
        :param netflow_dstream:
        :return:
        """


# 运行类
SparkStreaming()
