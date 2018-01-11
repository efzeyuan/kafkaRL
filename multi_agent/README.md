# Start the server
1. bin/zookeeper-server-start.sh config/zookeeper.properties
2. bin/kafka-server-start.sh config/server.properties

# list topic
bin/kafka-topics.sh --list --zookeeper localhost:2181

# delete topic
bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic test
