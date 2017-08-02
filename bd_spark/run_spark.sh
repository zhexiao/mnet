#!/bin/bash

/opt/spark/sbin/stop-master.sh
/opt/spark/sbin/stop-slaves.sh

/opt/spark/sbin/start-master.sh
/opt/spark/sbin/start-slaves.sh

/opt/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.1 /home/hdgs/mnet/bd_spark/spark.py
