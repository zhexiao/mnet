import datetime


from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import explode, window
from pyspark.sql.functions import split, DataFrame

spark = SparkSession.builder.master(
    "spark://192.168.33.50:7077"
).getOrCreate()

# 模拟数据发生
lines = spark.createDataFrame([
    Row(value='hadoop apache', word='cat')
])

# new_col = explode(
#     split(lines.value, " ")
# ).alias("word")
# print(type(new_col))

# 数据分割转成列
# words = lines.select(new_col)
# print(type(words))

# df = spark.createDataFrame([(["abc zhe", "2"], {"key": "value valu1"})], ["l", "d"])
# df.printSchema()
# df.show()

# new_df = df.select(split(df.l[0], " ").alias('z'), explode(split(df.d["key"], " ")).alias('v'))
# new_df.printSchema()
# new_df.show()

# new_df.select(explode(new_df.z), new_df.v).show()
# print(words)



df = spark.createDataFrame([
    ("2016-03-11 09:00:07", 1),
    ("2016-03-11 09:00:08", 1),
    ("2016-03-11 09:00:09", 20),
    ("2016-03-11 09:00:18", 5),
]).toDF("date", "val")
df.printSchema()
df.show()
w = df.groupBy(window("date", "5 seconds"))
print(w, type(w))
d = w.max('val').collect()
print(d)

now_datetime = datetime.datetime.now()
delta = datetime.timedelta(minutes=1)
print(now_datetime-delta, now_datetime+delta)