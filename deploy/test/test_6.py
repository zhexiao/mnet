from datetime import datetime

from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import explode
from pyspark.sql.functions import split, DataFrame

spark = SparkSession.builder.master(
    "spark://192.168.33.50:7077"
).getOrCreate()

# 模拟数据发生
# lines = spark.createDataFrame([
#     Row(value='hadoop apache', time=datetime.now(), word='cat')
# ])

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# 数据分割转成列
words = lines.select(
    explode(
        split(lines.value, " ")
    ).alias("word")
)
words.printSchema()

# Generate running word count
wordCounts = words.groupBy("word").count()

# Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("checkpointLocation", "/tmp/checkpoint/test6") \
    .option("path", "/tmp/test6") \
    .start() \
    .awaitTermination()
