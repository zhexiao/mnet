from pyspark import SparkConf
from pyspark.sql import SparkSession, Row

conf = SparkConf()
conf.set("spark.master", "spark://192.168.33.50:7077")
conf.set('spark.driver.host', '192.168.33.50')

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

# 模拟数据发生
lines = spark.createDataFrame([
    Row(ipv4_src_addr='122.204.161.240', in_bytes=120, in_pkts=2),
    Row(ipv4_src_addr='122.204.161.240', in_bytes=100, in_pkts=3),
    Row(ipv4_src_addr='122.204.161.240', in_bytes=200, in_pkts=10),
    Row(ipv4_src_addr='122.204.161.241', in_bytes=150, in_pkts=7),
    Row(ipv4_src_addr='122.204.161.241', in_bytes=170, in_pkts=3),
    Row(ipv4_src_addr='122.204.161.242', in_bytes=220, in_pkts=5),
])
lines.printSchema()

d1 = lines.groupBy(lines.ipv4_src_addr).sum('in_bytes', 'in_pkts')
d2 = d1.withColumnRenamed("sum(in_bytes)","in_bytes").withColumnRenamed("sum(in_pkts)","in_pkts")
d2.printSchema()

d2.show()