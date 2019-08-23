# 项目部署
整套服务项目部署流程，整套操作都在deploy目录下进行。

# Zookeeper
```
$ docker run \
    --name zoo1 \
    --restart always \
    --network zxnet \
    --detach \
    zookeeper:3.5.5 
```

# Kafka
```
$ wget -P ./pkg http://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.3.0/kafka_2.12-2.3.0.tgz

$ docker build -t java-base -f Dockerfile-java-base .
$ docker build -t kafka -f Dockerfile-kafka .

$ docker run \
    --name kf1 \
    --publish 9092:9092 \
    --link=zoo1:zoo1 \
    --env KAFKA_BROKER_ID=1 \
    --env KAFKA_LISTENERS=PLAINTEXT://:9092 \
    --env KAFKA_ZOOKEEPER_CONNECT=zoo1:2181 \
    --restart always \
    --network zxnet \
    --detach \
    kafka 
```

测试
```
$ docker exec -it kf1 /kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --zookeeper zoo1:2181 --replication-factor 1 --partitions 1 --topic mytest
$ docker exec -it kf1 /kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --describe --zookeeper zoo1:2181 --topic mytest

$ docker exec -it kf1 /kafka/kafka_2.12-2.3.0/bin/kafka-console-consumer.sh --bootstrap-server kf1:9092 --topic mytest --from-beginning
$ docker exec -it kf1 /kafka/kafka_2.12-2.3.0/bin/kafka-console-producer.sh --broker-list kf1:9092 --topic mytest
```

# Elasticsearch
```
$ docker run \
    --name es1 \
    --publish 9200:9200 \
    --publish 9300:9300 \
    --env "discovery.type=single-node" \
    --restart always \
    --network zxnet \
    --detach \
    elasticsearch:6.4.3
```

# Kibana
```
$ docker run \
    --name kb1 \
    --publish 5601:5601 \
    --link=es1:es1 \
    --env "ELASTICSEARCH_URL=http://es1:9200" \
    --restart always \
    --network zxnet \
    --detach \
    kibana:6.4.3 
```

# Logstash
```
$ cp default.conf.example default.conf
$ cp logstash.yml.example logstash.yml
```