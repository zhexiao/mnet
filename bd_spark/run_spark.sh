#!/bin/bash

echo "stop spark master ......"
/opt/spark/sbin/stop-master.sh
sleep 3

echo "stop spark slaves ......"
/opt/spark/sbin/stop-slaves.sh
sleep 3

echo "start spark master ......."
/opt/spark/sbin/start-master.sh
sleep 3

echo "start spark slaves ......"
/opt/spark/sbin/start-slaves.sh
sleep 3

echo "kill spark.py ......"
pkill -f spark.py

echo "start spark.py ......"
/opt/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.1 /home/hdgs/mnet/bd_spark/spark.py
