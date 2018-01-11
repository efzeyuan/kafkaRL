# -*- coding: utf-8 -*-
"""
This file uses Algorithmia model to process data with Kafka.
There are 3 steps:
    1. consume data from input Kafka topic
    2. process data with Algorithmia model
    3. produce processed data to output Kafka topic
"""

from pykafka import KafkaClient
import Algorithmia
import sys,getopt
import time

KAFKA_SERVER_IP = "162.105.85.212"
KAFKA_SERVER_PORT = "9092"
INPUT_TOPIC = "test-input-topic"
OUTPUT_TOPIC = "test-output-topic"
ALGORITHMIA_USER_KEY = 'sim0p9Q80e7GOrE1/4Vb6MLeVMg1'
ALGORITHMIA_MODEL = 'efzeyuan/Hello/0.1.0'

'''
operate args, usage:
    -p                KAFKA_SERVER_PORT
    -k                ALGORITHMIA_USER_KEY
    -m                ALGORITHMIA_MODEL
    --input_topic     KAFKA_INPUT_TOPIC
    --output_topic    KAFKA_OUTPUT_TOPIC
    --ip              KAFKA_SERVER_IP
'''

opts, args = getopt.getopt(sys.argv[1:], "p:k:m:", ["ip", "input_topic", "output_topic"])
for op, value in opts:
    if op == "-p":
        KAFKA_SERVER_PORT = value
    elif op == "-k":
        ALGORITHMIA_USER_KEY = value
    elif op == "-m":
        ALGORITHMIA_MODEL = value
    elif op == "input_topic":
        INPUT_TOPIC = value
    elif op == "output_topic":
        OUTPUT_TOPIC = value
    elif op == "ip":
        KAFKA_SERVER_IP = value

#get full address of kafka server
kafka_server_address = KAFKA_SERVER_IP + ":" + KAFKA_SERVER_PORT

#connect to kafka server
print("Connecting Kafka server...address:%s" %(kafka_server_address) )
client = KafkaClient(kafka_server_address)
print("Connect successfully")

#get topics
print("getting topics...")
input_topic = client.topics[INPUT_TOPIC.encode('utf-8')]
print("INPUT_TOPIC:%s" %(INPUT_TOPIC))
output_topic = client.topics[OUTPUT_TOPIC.encode('utf-8')]
print("OUTPUT_TOPIC:%s" %(OUTPUT_TOPIC))

#get Algorithmia user client key
try:
    Algorithmia_client = Algorithmia.client(ALGORITHMIA_USER_KEY)
except Exception as Error:
    print(Error)

#get model from Algorithmia 
print("getting Algorithmia model: %s" %(ALGORITHMIA_MODEL))
try:
    algo = Algorithmia_client.algo(ALGORITHMIA_MODEL)
    print("Get model successfully")
except Exception as Error:
    print(Error)

#get consumer of input topic
input_comsumer = input_topic.get_simple_consumer()

#get producer of output topic
output_producer = output_topic.get_producer()
output_producer.start()

#start consuming input message and producing output message processed by model
print("Start processing data")
for message in input_comsumer:
    try:
        input = message.value.decode('utf-8')
        print("input data: %s" %(input))
        output = str(algo.pipe(input).result)
        print("output data: %s" %(output))
        output_producer.produce(output.encode('utf-8'))
        time.sleep(1)
    except Exception as Error:
        print(Error)