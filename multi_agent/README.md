# Start the server
1.  /home/luwei/kafka/kafka_2.11-1.0.0/bin/zookeeper-server-start.sh config/zookeeper.properties
2.  /home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-server-start.sh config/server.properties

# list topic
/home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-topics.sh --list --zookeeper localhost:2181

# delete topic
1.  /home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic cartpole-env-input
2.  /home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic cartpole-env-output

# view message
1.  /home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic cartpole-env-input --from-beginning
2.  /home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic cartpole-env-output --from-beginning
