# -*- coding: utf-8 -*-
from pyspark import SparkContext , SparkConf

conf = SparkConf()
conf.set("spark.master", "spark://spark-master:7077")
conf.set('spark.driver.host', 'spark-master')

# 设置任务使用的核数
# conf.set("spark.cores.max", 1)

sc = SparkContext(conf=conf)
ts = sc.parallelize([3, 1, 2, 5])
print(ts)

print(ts.count())
print(ts.collect())