# -*- coding: utf-8 -*-
"""
This file is used to consume message from a spicified topic.
"""


from pykafka import KafkaClient
import sys,getopt
import time

KAFKA_SERVER_IP = "162.105.85.212"
KAFKA_SERVER_PORT = "9092"
CONSUMER_TOPIC = "test-output-topic"

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
        CONSUMER_TOPIC = value
    elif op == "ip":
        KAFKA_SERVER_IP = value

#get full address of kafka server
kafka_server_address = KAFKA_SERVER_IP + ":" + KAFKA_SERVER_PORT

#connect to kafka server
print("Connecting Kafka server...address:%s" %(kafka_server_address) )
client = KafkaClient(kafka_server_address)
print("Connect successfully")

#start a consumer
print("Starting a consumer of topic:%s" %(CONSUMER_TOPIC) )
topic = client.topics[CONSUMER_TOPIC.encode('utf-8')]
consumer = topic.get_simple_consumer()
print("The consumer has started successfully")

#consume message from topic
print("Start consuming message")
for msg in consumer:
    try:
        
        print('message content: %s   offset:%s' %(msg.value.decode('utf-8'),msg.offset) )
        time.sleep(1)
    except Exception as Error:
        pass
    
