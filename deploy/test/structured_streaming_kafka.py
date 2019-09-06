"""
jar:
https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10_2.11/2.4.3
https://mvnrepository.com/artifact/org.apache.kafka/kafka-clients/2.2.0
https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-10-assembly_2.11/2.4.3

启动：./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3 /vagrant/mnet/deploy/test/structured_streaming_kafka.py
"""
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, window

conf = SparkConf()
conf.set("spark.master", "spark://192.168.33.50:7077")
conf.set('spark.driver.host', '192.168.33.50')

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test1") \
    .load() \
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

df.printSchema()
res_df = df.select(df['value'])

ds = df \
  .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
  .writeStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "test2") \
  .start()