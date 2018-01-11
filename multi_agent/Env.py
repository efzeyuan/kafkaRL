from pykafka import KafkaClient
import gym

env = gym.make('CartPole-v0')

client = KafkaClient("162.105.85.212:9092")

topic_input = client.topics['cartpole-env-output']
producer = topic_input.get_producer()
producer.start()
producer.produce(str(env.reset()))

topic_output = client.topics['cartpole-env-input']
consumer = topic_output.get_simple_consumer()
for msg in consumer:
    if msg is not None:
        action = int(msg.value)
	next_state, reward, done, _ = env.step(action)
	producer.produce(str(next_state)+'|'+str(reward)+'|'+str(done))
	if done is True:
	    producer.produce(str(env.reset()))

