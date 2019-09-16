import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('testres', bootstrap_servers='192.168.33.50:9092')

for msg in consumer:
    val = msg.value.decode()

    print(msg.key.decode())
    print(json.loads(val).get('word'))
    print(json.loads(val).get('count'))
    print(json.loads(val).get('window'))
    print('='*30)
