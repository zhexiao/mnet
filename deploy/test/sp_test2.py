from datetime import datetime
import json

from pyspark import SparkConf
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import explode
from pyspark.sql.functions import split, DataFrame

conf = SparkConf()
conf.set("spark.master", "spark://192.168.33.50:7077")
conf.set('spark.driver.host', '192.168.33.50')

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

# 模拟数据发生
lines = spark.createDataFrame([
    Row(value='hadoop apache', time=datetime.now(), word='cat')
])

# 数据分割转成列
words = lines.select(
    explode(
        split(lines.value, " ")
    ).alias("word"),
    lines.time
)

res_df =  spark.createDataFrame([
    Row(value=json.dumps(words.toJSON().collect()), key='mnet')
])
print(res_df)

