# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:00:03 2017

@author: lenovo
"""

from pykafka import KafkaClient
import time

client = KafkaClient("162.105.85.212:9092")
#print(client.topics)
topic = client.topics['remote-python-test-input']
producer = topic.get_producer()
producer.start()
i = 1
while True:
    producer.produce('remote message' + str(i))
    print(i)
    i = i + 1
    time.sleep(5)