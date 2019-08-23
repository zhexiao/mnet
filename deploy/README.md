# 项目部署
整套服务项目部署流程，整套操作都在deploy目录下进行。

# Zookeeper
```
$ docker run --name zoo1 --restart always -d zookeeper:3.5.5 --network zxnet
```

# Kafka
```
$ wget -P ./pkg http://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.3.0/kafka_2.12-2.3.0.tgz
$ 
```