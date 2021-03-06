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

window_words = words.where(
    words.timestamp > "2019-09-10 06:49:38.0"
).withWatermark(
    "timestamp", "1 minutes"
).groupBy(
    window(
        words.timestamp,
        '1 minutes',
        '1 minutes'
    ),
    words.zhexiao
).count().orderBy('window')


# Start running the query that prints the running counts to the console
query = window_words \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option('truncate', 'false') \
    .start() \
    .awaitTermination()
