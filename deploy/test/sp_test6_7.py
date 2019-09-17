"""
./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4 /vagrant/mnet/deploy/test/sp_test6.py

spark-sql-kafka-0-10_2.11:2.4.4 ===> 2.11代表scala版本，2.4.4代表spark版本
kafka:kafka_2.11-2.3.0.tgz
spark:spark-2.4.4-bin-hadoop2.7.tgz
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, window
from pyspark.sql.types import StructType, IntegerType, StringType, TimestampType

"""
常量
"""
spark_master = "spark://192.168.33.50:7077"
kafka_master = "192.168.33.50:9092"
mnet_topic = "test"
mnet_agg_topic = "testres"
window_time = "30 seconds"

spark = SparkSession.builder.master(
    spark_master
).getOrCreate()

stream_data = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_master) \
    .option("subscribe", mnet_topic) \
    .load()
stream_data.printSchema()

# kafka json数据解析
data_schema = StructType().add(
    "host", StringType()
).add(
    "create_time", TimestampType()
).add(
    "netflow", StructType().add(
        "ipv4_src_addr", StringType()
    ).add(
        "ipv4_dst_addr", StringType()
    ).add(
        "in_bytes", IntegerType()
    ).add(
        "in_pkts", IntegerType()
    ).add(
        "protocol", IntegerType()
    )
)
new_stream_data = stream_data.select(
    stream_data.key.cast("string"),
    from_json(stream_data.value.cast("string"), data_schema).alias('json_data')
)
new_stream_data.printSchema()

new_df = new_stream_data.filter(
    (new_stream_data.json_data.netflow.protocol == 6) | (new_stream_data.json_data.netflow.protocol == 8)
).select(
    (new_stream_data.json_data.netflow.ipv4_src_addr).alias('src_ip'),
    (new_stream_data.json_data.netflow.ipv4_dst_addr).alias('dest_ip'),
    (new_stream_data.json_data.netflow.in_bytes).alias('in_bytes'),
    (new_stream_data.json_data.netflow.in_pkts).alias('in_pkts'),
    (new_stream_data.json_data.create_time).alias('create_time'),
)
new_df.printSchema()

# 聚合
net_df = new_df.withWatermark(
    'create_time', window_time
).groupBy(
    new_df.src_ip,
    new_df.dest_ip,
    window(new_df.create_time, window_time, window_time),
).sum('in_bytes', 'in_pkts')

res_df = net_df.withColumnRenamed(
    "sum(in_bytes)","in_bytes"
).withColumnRenamed(
    "sum(in_pkts)","in_pkts"
)
res_df.printSchema()

# Start running the query that prints the running counts to the console
query = res_df \
    .selectExpr("CAST(window AS STRING) AS key", "to_json(struct(*)) AS value") \
    .writeStream \
    .trigger(processingTime=window_time) \
    .outputMode("update") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.33.50:9092") \
    .option("topic", mnet_agg_topic) \
    .option("checkpointLocation", "/tmp/{}".format(mnet_agg_topic)) \
    .start() \
    .awaitTermination()
