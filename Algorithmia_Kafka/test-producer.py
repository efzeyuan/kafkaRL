# -*- coding: utf-8 -*-
"""
This file is used to produce message continuously to a spicified topic.
"""

from pykafka import KafkaClient
import time
import sys,getopt

KAFKA_SERVER_IP = "162.105.85.212"
KAFKA_SERVER_PORT = "9092"
PRODUCER_TOPIC = "test-input-topic"

'''
operate args, usage:
    -p     KAFKA_SERVER_PORT
    -t     KAFKA_TOPIC
    --ip   KAFKA_SERVER_IP
'''

opts, args = getopt.getopt(sys.argv[1:], "p:t:", ["ip"])
for op, value in opts:
    if op == "-p":
        KAFKA_SERVER_PORT = value
    elif op == "-t":
        PRODUCER_TOPIC = value
    elif op == "ip":
        KAFKA_SERVER_IP = value

#get full address of kafka server
kafka_server_address = KAFKA_SERVER_IP + ":" + KAFKA_SERVER_PORT

#connect to kafka server
print("Connecting Kafka server...address:%s" %(kafka_server_address) )
client = KafkaClient(kafka_server_address)
print("Connect successfully")

#start a producer
print("Starting a producer of topic:%s" %(PRODUCER_TOPIC) )
topic = client.topics[PRODUCER_TOPIC]
producer = topic.get_producer()
producer.start()
print("The producer has started successfully")

#produce simple message
print("Start producing message")
i = 1
while True:
    try:
        producer.produce('remote message' + str(i))
        print("Produced a message to topic \"%s\" at %s" %(PRODUCER_TOPIC, time.asctime( time.localtime(time.time()) )))
        i = i + 1
        time.sleep(5)
    except Exception as Error:
        pass

