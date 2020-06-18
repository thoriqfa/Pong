import random
import pygame
import numpy as np
from collections import deque
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam

'''
from numpy.random import seed
seed(42)                        # keras seed fixing
import tensorflow as tf
tf.random.set_seed(42)          # tensorflow seed fixing
'''
#pygame.init()

class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        self.available_action = [i for i in range(self.action_space)]

    def choose_action(self):
        '''Choosing action over discrete available actions'''
        action = random.choice(self.available_action)
        return action

class HumanAgent:
    def __init__(self):
        pass

    def choose_action(self):
        action = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            action = 1
        if keys[pygame.K_DOWN]:
            action = 2
        return action

class DQNAgent:
    def __init__(self, observation_space, action_space):
        self.gamma = 0.95
        self.learning_rate = 0.001
        self.memory_size = 1000000
        self.batch_size = 100
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_dec = 0.9995
        self.update_q_every = 5
        self.update_q_counter = 0

        self.observation_space = observation_space
        self.action_space = action_space
        self.available_action = [i for i in range(self.action_space)]
        self.memory = deque(maxlen=self.memory_size)

        self.q = self.build_model()
        self.q_target = self.build_model()
        self.q_target.set_weights(self.q.get_weights())

    def build_model(self):
        model = Sequential([
            Dense(32, input_shape = (self.observation_space,), activation="relu"),
            Dense(32, activation="relu"),
            Dense(32, activation="relu"),
            Dense(self.action_space, activation="linear")
        ])
        model.compile(optimizer= Adam(learning_rate=self.learning_rate), loss ="mse")
        return model

    def q_from_load_model(self, model):
        self.epsilon = self.epsilon_min
        self.q = load_model(model, compile=True)
        self.q_target.set_weights(self.q.get_weights())

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            #print("random action")
            action = np.random.choice(self.available_action)
        else:
            #print("greedy action")
            action_q_values = self.q.predict(observation.reshape(-1,5))
            action = np.argmax(action_q_values)
        return action

    def store_transition(self, state, action, reward, state_, done):
        self.memory.append((state, action, reward, state_, done))

    def learn(self):
        if len(self.memory) < self.batch_size:
            return

        #fetchs data from replay memory pool
        learning_batch = random.sample(self.memory, self.batch_size)
        
        states = np.array([transition[0] for transition in learning_batch])
        states_q = self.q.predict(states)

        next_states = np.array([transition[3] for transition in learning_batch])
        next_states_q = self.q_target.predict(next_states)

        for index, (state, action, reward, next_state, done) in enumerate(learning_batch):
        
            q_update = reward + self.gamma * np.max(next_states_q[index]) * (1 - int(done))
            states_q[index][action] = q_update

        X = np.array(states).reshape(self.batch_size, self.observation_space)
        Y = np.array(states_q).reshape(self.batch_size, self.action_space)
        self.q.fit(X, Y, verbose = 0, batch_size=self.batch_size)

        self.update_q_counter += 1
        if self.update_q_counter > self.update_q_every:
            self.epsilon = self.epsilon * self.epsilon_dec if self.epsilon > self.epsilon_min else self.epsilon_min
            self.q_target.set_weights(self.q.get_weights())
            self.update_q_counter = 0

class PolicyGradientAgent:
    def __init__(self, observation_space, action_space):
        self.gamma = 0.99
        self.alpha = 0.001
        self.learning_rate = 0.01

        self.observation_space = observation_space
        self.action_space = action_space

        #record transitions
        self.states = []
        self.gradients = []
        self.rewards = []
        self.probs = []
        self.discounted_rewards = []
        self.total_rewards = []

        self.model = self.build_model()

    def from_load_model(self, model):
        self.model = load_model(model, compile=True)

    def hot_encode_action(self, action):
        '''Convert action to one hot encoding'''
        action_encoded = np.zeros(self.action_space, np.float32)
        action_encoded[action] = 1
        return action_encoded

    def store_transition(self, state, action, action_prob, reward):
        '''Stores observations'''
        encoded_action = self.hot_encode_action(action)
        self.gradients.append(encoded_action - action_prob)
        self.states.append(state)
        self.rewards.append(reward)
        self.probs.append(action_prob)

    def build_model(self):
        model = Sequential([
            Dense(32, input_shape=(self.observation_space,), activation="relu"),
            Dense(32, activation="relu"),
            Dense(32, activation="relu"),
            Dense(self.action_space, activation="softmax")
        ])
        model.compile(loss="categorical_crossentropy", optimizer = Adam(lr=self.learning_rate))
        return model

    def choose_action(self, observation):
        observation = np.reshape(observation, [1, self.observation_space])
        #get action probability
        action_probability_dist = self.model.predict(observation)[0]
        #normalize
        action_probability_dist /= np.sum(action_probability_dist)

        #take action
        action = np.random.choice(self.action_space, 1, p = action_probability_dist)[0]
        return action, action_probability_dist

    def get_discounted_rewards(self, rewards):
        discounted_rewards = []
        cumulative_total_return = 0

        for reward in rewards[::-1]:
            cumulative_total_return = cumulative_total_return * self.gamma + reward
            discounted_rewards.insert(0, cumulative_total_return)

        #normalize discounted rewards
        mean_rewards = np.mean(discounted_rewards)
        std_rewards = np.std(discounted_rewards)
        norm_discounted_rewards = (discounted_rewards - mean_rewards)/(std_rewards+ 1e-7)

        return norm_discounted_rewards

    def learn(self):
        #if training is not enabled (False) then states list will be empty and learn function shouldn't be carried out
        if self.states == []:
            return

        states = np.vstack(self.states)

        #stacks vectors vertically so num[y element wise multiplication can be done
        gradients = np.vstack(self.gradients)
        discounted_rewards = np.vstack(self.get_discounted_rewards(self.rewards))

        #fitting the states to the desired action probability distribution based on the update rule
        updates = np.vstack(self.probs) + self.alpha * gradients * discounted_rewards
        self.model.train_on_batch(states, updates)

        #empty lists
        self.states, self.probs, self.gradients, self.rewards = [], [], [], []