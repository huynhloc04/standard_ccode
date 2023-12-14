import config
from kafka import KafkaProducer
import json

topic_name = 'nhac_vang'

p = KafkaProducer(
        bootstrap_servers=[config.kafka_ip]
        )

json_mess = json.dumps({ "name": "HuynhLoc",
                         "age": 22,
                         "car": "Mercedes"})

p.send(topic_name, json_mess.encode("utf-8"))
p.flush()

print("Sent successfully!!!")
