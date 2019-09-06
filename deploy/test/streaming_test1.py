from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, window
from pyspark.sql.functions import split
from pyspark.sql.types import TimestampType

def debug_dt(str):
    print('='*100)
    print(str)
    print('=' * 100)

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()


debug_dt(type(lines))
debug_dt(lines)
debug_dt(lines.value)

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()



 # Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()