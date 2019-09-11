from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

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

# Start running the query that prints the running counts to the console
query = words \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option('truncate', 'false') \
    .start() \
    .awaitTermination()
