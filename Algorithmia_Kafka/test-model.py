# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 16:26:27 2018

@author: lenovo
"""

from pykafka import KafkaClient
import Algorithmia

client = KafkaClient("162.105.85.212:9092")
input_topic = client.topics['remote-python-test-input']
output_topic = client.topics['remote-python-test-output']
Algorithmia_client = Algorithmia.client('sim0p9Q80e7GOrE1/4Vb6MLeVMg1')
algo = Algorithmia_client.algo('efzeyuan/Hello/0.1.0')
producer = output_topic.get_producer()
producer.start()
comsumer = input_topic.get_simple_consumer()
for message in comsumer:
    input = message.value
    output = str(algo.pipe(input).result)
    print(output)
    producer.produce(output)