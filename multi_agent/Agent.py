import random
import gym
import math
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import pdb
import argparse
from pykafka import KafkaClient
import time


class DQNCartPoleSolver():
    def __init__(self, n_episodes=1000, n_win_ticks=195, max_env_steps=None, gamma=1.0, epsilon=1.0, epsilon_min=0.01,
                 epsilon_log_decay=0.995, alpha=0.01, alpha_decay=0.01, batch_size=64, monitor=False, quiet=False):
        self.memory = deque(maxlen=100000)
        self.env = gym.make('CartPole-v0')
        if monitor: self.env = gym.wrappers.Monitor(self.env, '../data/cartpole-1', force=True)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_log_decay
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.n_episodes = n_episodes
        self.n_win_ticks = n_win_ticks
        self.batch_size = batch_size
        self.quiet = quiet
        if max_env_steps is not None: self.env._max_episode_steps = max_env_steps

        # Init model
        self.model = Sequential()
        self.model.add(Dense(24, input_dim=4, activation='tanh'))
        self.model.add(Dense(48, activation='tanh'))
        self.model.add(Dense(2, activation='linear'))
        self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state, epsilon):
        return self.env.action_space.sample() if (np.random.random() <= epsilon) else np.argmax(
            self.model.predict(state))

    def get_epsilon(self, t):
        return max(self.epsilon_min, min(self.epsilon, 1.0 - math.log10((t + 1) * self.epsilon_decay)))

    def preprocess_state(self, state):
        return np.reshape(state, [1, 4])

    def replay(self, batch_size):
        x_batch, y_batch = [], []
        minibatch = random.sample(
            self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            y_target = self.model.predict(state)
            y_target[0][action] = reward if done else reward + self.gamma * np.max(self.model.predict(next_state)[0])
            x_batch.append(state[0])
            y_batch.append(y_target[0])

        self.model.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def run(self, producer, consumer):
        scores = deque(maxlen=100)

        for e in range(self.n_episodes):
            for msg in consumer:
                if msg is not None:
                    state = msg.value
                    break
            state = format_state(state)
            state = self.preprocess_state(state)
            done = False
            i = 0

            while not done:
                action = self.choose_action(state, self.get_epsilon(e))
                producer.produce(str(action))
                for msg in consumer:
                    if msg is not None:
                        feedback = msg.value
                        break
#                pdb.set_trace()
                next_state, reward, done = format_feedback(feedback)
                next_state = self.preprocess_state(next_state)
                self.remember(state, action, reward, next_state, done)
                state = next_state
                i += 1

            scores.append(i)
            mean_score = np.mean(scores)
            if mean_score >= self.n_win_ticks and e >= 100:
                if not self.quiet: print('Ran {} episodes. Solved after {} trials.'.format(e, e - 100))
                return e - 100
            if e % 100 == 0 and not self.quiet:
                print('[Episode {}] - Mean survival time over last 100 episodes was {} ticks.'.format(e, mean_score))

            self.replay(self.batch_size)

        if not self.quiet: print('Did not solve after {} episodes.'.format(e))
        return e


def format_state(state):
    return np.fromstring(state.strip('[').strip(']'), sep=' ')


def format_feedback(feedback):
    arr = feedback.split('|')
    next_state = format_state(arr[0])
    reward = int(float(arr[1]))
    done = bool(arr[2])
    return next_state, reward, done


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--kafka_server', type=str, default="162.105.85.66:9092")
    parser.add_argument('--read_topic', type=str, default='cartpole-env-output')
    parser.add_argument('--write_topic', type=str, default='cartpole-env-input')
    args = parser.parse_args()

    client = KafkaClient(args.kafka_server)
    # print(client.topics)
    topic_input = client.topics[args.write_topic]
    producer = topic_input.get_producer()
    producer.start()

    topic_output = client.topics[args.read_topic]
    #consumer = topic_output.get_simple_consumer(consumer_group='agent', auto_commit_enable=True)
    consumer = topic_output.get_simple_consumer()

    agent = DQNCartPoleSolver()
    agent.run(producer, consumer)

