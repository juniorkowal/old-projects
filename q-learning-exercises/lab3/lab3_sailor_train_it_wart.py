import time
import os
import pdb
import numpy as np
import matplotlib.pyplot as plt
import sailor_funct as sf
import random

num_of_episodes = 1000                   # number of training epizodes (multi-stage processes) 
gamma = 0.9                                 # discount factor
epsilon = 1.0
epsilon_discount = 0.99
T = 1

#file_name = 'map_small.txt'
file_name = 'map_easy.txt'
#file_name = 'map_big.txt'
#file_name = 'map_spiral.txt'

reward_map = sf.load_data(file_name)
num_of_rows, num_of_columns = reward_map.shape

num_of_steps_max = int(5*(num_of_rows + num_of_columns))    # maximum number of steps in an episode
Q = np.zeros([num_of_rows, num_of_columns, 4], dtype=float)  # trained usability table of <state,action> pairs
sum_of_rewards = np.zeros([num_of_episodes], dtype=float)

# miejsce na algorytm uczenia - modelem jest tablica Q
# (symulację epizodu można wziąć z funkcji sailor_test())
# ............................

def epsilon_greedy(state):
    if random.random() < epsilon:
        return np.random.randint(1, 5)
    else:
        return 1 + np.argmax(Q[state[0], state[1], :])


def boltzman(state):
    action_prob = []
    for action in range(4):
        action_prob.append(np.exp(Q[state[0], state[1], action] / T))

    action_sum = sum(action_prob)
    action_prob = action_prob / action_sum
    return np.random.choice(np.arange(1, 5), p = action_prob)


# METODA MONTE CARLO - ITERACJA WARTOŚCI
for episode in range(num_of_episodes):
    alpha = np.exp(1 / (episode + 1)) / 10   # WSPÓŁCZYNNIK ALPHA ZALEŻNY OD EPIZODU

    state_s = np.zeros([2], dtype=int)  # initial state here [1 1] but rather random due to exploration
    state_s[0] = np.random.randint(0, num_of_rows)    

    the_end = False
    steps = 0


    while not the_end:
        steps += 1

        action = boltzman(state_s)

        state_prime, reward = sf.environment(state_s, action, reward_map)

        Q[state_s[0], state_s[1], action - 1] = Q[state_s[0], state_s[1], action - 1] + alpha * (reward + gamma * np.max(Q[state_prime[0], state_prime[1], :]) - Q[state_s[0], state_s[1], action - 1])
        
        state_s = state_prime   # S <- S'
        # action = action # A <- A'
        
        if (steps == num_of_steps_max) or (state_prime[1] >= num_of_columns - 1):
            the_end = True


    epsilon *= epsilon_discount
    # print(alpha)
    # print(epsilon)
    #print(f"Nr epizodu: {episode}")

sf.sailor_test(reward_map, Q, num_of_episodes)
sf.draw(reward_map, Q)
