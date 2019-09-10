"""
模拟 streaming  每分钟的数据聚合一次
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, window

spark = SparkSession.builder.master(
    "spark://192.168.33.50:7077"
).getOrCreate()

stream_data = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .option('includeTimestamp', 'true') \
    .load()
stream_data.printSchema()

# 数据分割转成列
words = stream_data.select(
    explode(
        split(stream_data.value, " ")
    ).alias("zhexiao"),
    stream_data.timestamp
)
words.printSchema()

window_words = words.withWatermark(
    "timestamp", "1 minutes"
).groupBy(
    window(
        words.timestamp,
        '1 minutes',
        '1 minutes'
    ),
    words.zhexiao
).count()

# Start running the query that prints the running counts to the console
query = window_words \
    .writeStream \
    .trigger(processingTime='1 minutes') \
    .outputMode("update") \
    .format("console") \
    .option('truncate', 'false') \
    .start() \
    .awaitTermination()
