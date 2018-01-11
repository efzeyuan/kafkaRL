from pykafka import KafkaClient
import gym
import argparse, time


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--kafka_server', type=str, default="162.105.85.66:9092")
    parser.add_argument('--read_topic', type=str, default='cartpole-env-input')
    parser.add_argument('--write_topic', type=str, default='cartpole-env-output')
    args = parser.parse_args()

    env = gym.make('CartPole-v0')

    client = KafkaClient(args.kafka_server)

    topic_input = client.topics[args.write_topic]
    producer = topic_input.get_producer()
    producer.start()
    producer.produce(str(env.reset()))

    topic_output = client.topics[args.read_topic]
    consumer = topic_output.get_simple_consumer()

    offsets = topic_output.fetch_offset_limits(time.time() * 1000)[0][0][0]
    while True:
        try:
            msg = consumer.consume()
            action = int(msg.value)
            next_state, reward, done, _ = env.step(action)
            producer.produce(str(next_state) + '|' + str(reward) + '|' + str(done))
            if done is True:
                producer.produce(str(env.reset()))
        except Exception as Error:
            pass



