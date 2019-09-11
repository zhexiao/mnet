from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='192.168.33.50:9092')

topic = 'test'
i = 0
while True:
    i += 1
    msg = "my kafka {}".format(i)
    producer.send(topic, msg.encode())
    print('producer - {0}'.format(msg))
    time.sleep(8)
