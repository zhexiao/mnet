# 项目部署
整套服务项目部署流程，整套操作都在deploy目录下进行。

# 架构
![image](https://github.com/zhexiao/mnet/blob/dev/deploy/architecture.png?raw=true)

# docker跨主机通信
现有机器vm1（192.168.71.148）、vm2（192.168.71.152）和vm3（192.168.71.153）。设vm1为管理主节点，其余为工作节点。

跨主机
```
在 148 上创建manager
$ docker swarm init --advertise-addr 192.168.71.148

在其余的工作机器加入节点
$ docker swarm join --token SWMTKN-1-5hcor53t93skr6k8sacb54n8sipo1za7oqa4wgywid8ugjhkjd-6giddshlk9dsa5213ay80um8s 192.168.71.148:2377

如果找不到了加入命令，则可以在管理节点输入
$ docker swarm join-token worker
```

网络
```
创建网络，--attachable  是为了swarm集群外的容器能够加入该网络
$ docker network create -d overlay --attachable zxnet

148机器（manager）测试alpine1 
$ docker run -it --name alpine1 --network zxnet alpine

152机器(worker)测试alpine2，注意 -d 表示detached 
$ docker run -it --name alpine2 --network zxnet alpine

互相启动ping命令
$ ping alpine2
```

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
# 版本修改需要对应修改 Dockerfile-kafka
$ wget -P ./pkg http://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.3.0/kafka_2.11-2.3.0.tgz

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
    
$ docker run \
    --name kf2 \
    --publish 9093:9092 \
    --link=zoo1:zoo1 \
    --env KAFKA_BROKER_ID=2 \
    --env KAFKA_LISTENERS=PLAINTEXT://:9092 \
    --env KAFKA_ZOOKEEPER_CONNECT=zoo1:2181 \
    --restart always \
    --network zxnet \
    --detach \
    kafka 
```

测试
```
$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-topics.sh --create --zookeeper zoo1:2181 --replication-factor 2 --partitions 1 --topic mnet
$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-topics.sh --create --zookeeper zoo1:2181 --replication-factor 2 --partitions 1 --topic mnet_agg

$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-topics.sh --describe --zookeeper zoo1:2181 --topic mnet
$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-topics.sh --describe --zookeeper zoo1:2181 --topic mnet_agg

$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-console-consumer.sh --bootstrap-server kf1:9092,kf2:9092 --topic mnet --from-beginning
$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-console-producer.sh --broker-list kf1:9092,kf2:9092 --topic mnet

$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-topics.sh --list  --zookeeper zoo1:2181
$ docker exec -it kf1 /kafka/kafka_2.11-2.3.0/bin/kafka-topics.sh --delete --zookeeper zoo1:2181 --topic mnet 
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
# default.conf定义数据流动，与下方测试紧密关联
$ cp logstash_default.conf.example logstash_default.conf
$ cp logstash.yml.example logstash.yml

$ docker build -t mylogstash -f Dockerfile-logstash .

$ docker run \
    --name lg1 \
    --publish 4739:4739/udp \
    --publish 21561:21561/udp \
    --publish 21562:21562/udp \
    --link=es1:es1 \
    --restart always \
    --network zxnet \
    --detach \
    mylogstash 
```

# Spark
```
安装包，包名对应Dockerfile-spark-base里面的ENV，如果版本有变化，需要对应修改
$ wget -P ./pkg http://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
$ wget -P ./pkg http://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz

镜像
$ docker build -t spark-base -f Dockerfile-spark-base .
$ docker build -t spark-master -f Dockerfile-spark-master .
$ docker build -t spark-worker -f Dockerfile-spark-worker .

运行master，如果报错UnresolvedAddressException，检查--name是否与Dockerfile里面的SPARK_MASTER_HOST一致
$ docker run \
    --name spark-master \
    --publish 8080:8080 \
    --publish 7077:7077 \
    --restart always \
    --network zxnet \
    --detach \
    spark-master
    
运行worker，启动多个worker需要运行多次，保证--name和--publish唯一即可
$ docker run \
    --name spark-worker1 \
    --publish 8081:8080 \
    --restart always \
    --link=spark-master:spark-master \
    --network zxnet \
    --detach \
    spark-worker
    
$ docker run \
    --name spark-worker2 \
    --publish 8082:8080 \
    --restart always \
    --link=spark-master:spark-master \
    --network zxnet \
    --detach \
    spark-worker
```

测试1
```
$ docker exec -it spark-master python3

把下面的代码复制进去测试：
from pyspark import SparkContext , SparkConf

conf = SparkConf()
conf.set("spark.master", "spark://spark-master:7077")

# 设置任务使用的核数
conf.set("spark.cores.max", 1)

sc = SparkContext(conf=conf)
ts = sc.parallelize([3, 1, 2, 5])

print(ts.count())
print(ts.collect())
```

测试2
```
把测试文件夹映射到容器内部
$ docker run \
    --name spark-master \
    --publish 8080:8080 \
    --publish 7077:7077 \
    --restart always \
    --network zxnet \
    -v /vagrant/mnet/deploy/test:/test \
    --detach \
    spark-master
    
运行
$ docker exec -it spark-master python3 /test/test1.py
```

# 网络收集
```
使用softflowd读取网络数据
$ sudo apt-get install git autoconf bison build-essential libtool libpcap-dev
$ git clone https://gitee.com/zhexiao/softflowd.git
$ cd softflowd
$ autoreconf -i | ./configure
$ make
$ sudo make install

抓取数据发送到vm1的端口
$ sudo softflowd -D -v 9 -i ens160 -n 192.168.71.148:4739 -T full

发送模拟数据
$ sudo apt install apache2-utils
$ ab -c 100 -n 1000 -t 30 http://sina.com.cn/
```

数据查看
```
进入192.168.71.148服务器
$ docker logs --tail 100 lg1

正常会输出
{
    "tags" => [
        [0] "netflow_input"
    ],
    "@version" => "1",
    "@timestamp" => 2019-08-30T03:55:00.000Z,
        "host" => "192.168.71.182",
        "netflow" => {
        "first_switched" => "2019-08-30T03:54:50.999Z",
        "last_switched" => "2019-08-30T03:54:51.999Z",
        "input_snmp" => 0,
        "l4_src_port" => 80,
        "in_bytes" => 52,
        "l4_dst_port" => 55474,
        "protocol" => 6,
        "src_tos" => 0,
        "in_src_mac" => "00:50:56:b6:00:ed",
        "output_snmp" => 0,
        "out_dst_mac" => "0c:da:41:ae:dd:b3",
        "version" => 9,
        "flowset_id" => 1024,
        "ipv4_src_addr" => "13.107.21.200",
        "ip_protocol_version" => 4,
        "flow_seq_num" => 3796,
        "in_pkts" => 1,
        "tcp_flags" => 18,
        "ipv4_dst_addr" => "192.168.71.182"
    }
}
```

# spark-client
```
$ docker build -t spark-client -f Dockerfile-spark-client .

$ docker run \
    --name spark-client1 \
    --restart always \
    --link=spark-master:spark-master \
    --network zxnet \
    --detach \
    spark-client
```