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
FROM_THE_LATEST_START = True


'''
operate args, usage:
    -p     KAFKA_SERVER_PORT
    -t     KAFKA_TOPIC
    -l     only consume latest message if selected
    --ip   KAFKA_SERVER_IP
'''

opts, args = getopt.getopt(sys.argv[1:], "p:t:l", ["ip"])
for op, value in opts:
    if op == "-p":
        KAFKA_SERVER_PORT = value
    elif op == "-t":
        CONSUMER_TOPIC = value
    elif op == "-t":
        CONSUMER_TOPIC = value
    elif op == "-l":
        FROM_THE_LATEST_START = True
    elif op == "ip":
        KAFKA_SERVER_IP = value

#get full address of kafka server
kafka_server_address = KAFKA_SERVER_IP + ":" + KAFKA_SERVER_PORT

#connect to kafka server
print("Connecting Kafka server...address:%s" %(kafka_server_address) )
client = KafkaClient(kafka_server_address)
print("Connect successfully")

#start a consumer and get topic offsets
print("Starting a consumer of topic:%s" %(CONSUMER_TOPIC) )
topic = client.topics[CONSUMER_TOPIC.encode('utf-8')]
offsets = -1
if FROM_THE_LATEST_START:
    try:
        offsets = topic.fetch_offset_limits(time.time() * 1000)[0][0][0]
    except:
        pass
print("topic offsets: %d" %(offsets + 1))
consumer = topic.get_simple_consumer(reset_offset_on_start = False)

print("The consumer has started successfully")

#consume message from topic
print("Start consuming message")
while True:
    try:
        msg = consumer.consume()
        if msg.offset > offsets:
            print("recieve a message at %s" %(time.asctime( time.localtime(time.time()))) )
            print('message content: %s   offset:%s' %(msg.value.decode('utf-8'),msg.offset) )
        #time.sleep(1)
    except Exception as Error:
        pass
    
