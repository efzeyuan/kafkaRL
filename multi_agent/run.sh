/home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic cartpole-env-input
/home/luwei/kafka/kafka_2.11-1.0.0/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic cartpole-env-output
python Env.py &
python Agent.py
