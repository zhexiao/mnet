from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(bootstrap_servers='192.168.33.50:9092')

topic = 'test'
i = 0
while True:
    i += 1
    json_data = {
        "msg": "my kafka {}".format(i),
        "count": i,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    post_data = json.dumps(json_data).encode()

    producer.send(topic, post_data)
    print('producer - {0}'.format(post_data))
    time.sleep(8)
