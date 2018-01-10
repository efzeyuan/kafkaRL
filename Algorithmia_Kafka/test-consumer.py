# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 16:31:56 2018

@author: lenovo
"""

from pykafka import KafkaClient

client = KafkaClient("162.105.85.212:9092")
topic = client.topics['remote-python-test-output']
consumer = topic.get_simple_consumer()

for msg in consumer:
    if msg is not None:
        print(msg.value)
    