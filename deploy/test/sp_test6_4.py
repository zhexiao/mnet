"""
./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4 /vagrant/mnet/deploy/test/sp_test6.py

spark-sql-kafka-0-10_2.11:2.4.4 ===> 2.11代表scala版本，2.4.4代表spark版本
kafka:kafka_2.11-2.3.0.tgz
spark:spark-2.4.4-bin-hadoop2.7.tgz
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, from_json, window
from pyspark.sql.types import StructType, IntegerType, StringType, TimestampType


spark = SparkSession.builder.master(
    "spark://192.168.33.50:7077"
).getOrCreate()

stream_data = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.33.50:9092") \
    .option("subscribe", "test") \
    .load()
stream_data.printSchema()

# kafka json数据解析
data_schema = StructType().add(
    "msg", StringType()
).add(
    "count", IntegerType()
).add(
    "create_time", TimestampType()
)
new_stream_data = stream_data.select(
    stream_data.key.cast("string"),
    from_json(stream_data.value.cast("string"), data_schema).alias('json_data')
)
new_stream_data.printSchema()

# msg按空格分隔
word_df = new_stream_data.select(
    explode(split(new_stream_data.json_data.msg, " ")).alias('word'),
    (new_stream_data.json_data.create_time).alias('create_time')
)
word_df.printSchema()

# 聚合
wordCounts = word_df.withWatermark(
    'create_time', '1 minutes'
).groupBy(
    window(word_df.create_time, '1 minutes', '1 minutes'),
    word_df.word
).count()

# Start running the query that prints the running counts to the console
query = wordCounts \
    .selectExpr("CAST(window AS STRING) AS key", "to_json(struct(*)) AS value") \
    .writeStream \
    .outputMode("update") \
    .trigger(processingTime='1 minutes') \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.33.50:9092") \
    .option("topic", "testres") \
    .option("checkpointLocation", "/tmp/testres") \
    .start() \
    .awaitTermination()
