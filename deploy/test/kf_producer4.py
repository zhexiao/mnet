from kafka import KafkaProducer
import time
import json
import random

producer = KafkaProducer(bootstrap_servers='192.168.33.50:9092')

topic = 'test'
i = 0
while True:
    i += 1
    json_data = {
        "host": "192.168.71.182",
        "netflow": {
            "ipv4_src_addr": "122.204.161.{}".format(random.randint(240, 242)),
            "in_bytes": random.randint(10, 500),
            "in_pkts": random.randint(1, 10),
            "protocol": random.randint(6, 7),
            "ipv4_dst_addr": "192.168.71.{}".format(random.randint(180, 182)),
        },
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }

    post_data = json.dumps(json_data).encode()

    producer.send(topic, post_data)
    print('producer - {0}'.format(post_data))
    time.sleep(8)
