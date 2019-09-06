from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, window

conf = SparkConf()
conf.set("spark.master", "spark://192.168.33.50:7077")
conf.set('spark.driver.host', '192.168.33.50')

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .option('includeTimestamp', 'true') \
    .load()

lines.printSchema()

# Split the lines into words
words = lines.select(
    explode(
        split(lines.value, " ")
    ).alias("word"),
    lines.timestamp
)

# Generate running word count
windowedCounts = words.withWatermark(
    'timestamp', '1 minutes'
).groupBy(
    window(words.timestamp, "1 minutes", "1 minutes"),
    words.word
).count().orderBy('window')

# Start running the query that prints the running counts to the console
query = windowedCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option('truncate', 'false') \
    .start()

query.awaitTermination()
