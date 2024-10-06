import time
import os
import pdb
import numpy as np
import matplotlib.pyplot as plt
import sailor_funct as sf
import random

def q_learning(epsilon, num_of_episodes, map):
    # num_of_episodes = 1000                   # number of training epizodes (multi-stage processes) 
    gamma = 0.9                                 # discount factor
    alpha = 0.1
    # epsilon = 1.0

    # file_name = 'map_small.txt'
    # # file_name = 'map_easy.txt'
    # # file_name = 'map_big.txt'
    # # file_name = 'map_spiral.txt'

    reward_map = sf.load_data(map)
    num_of_rows, num_of_columns = reward_map.shape

    num_of_steps_max = int(5*(num_of_rows + num_of_columns))    # maximum number of steps in an episode
    Q = np.zeros([num_of_rows, num_of_columns, 4], dtype=float)  # trained usability table of <state,action> pairs
    sum_of_rewards = np.zeros([num_of_episodes], dtype=float)

    # miejsce na algorytm uczenia - modelem jest tablica Q
    # (symulację epizodu można wziąć z funkcji sailor_test())
    # ............................

    def epsilon_greedy(state):
        if random.uniform(0,1) < epsilon:
            # print("epsilon")
            return random.randint(1,4)
        else:
            # print("max")
            return (np.argmax(Q[state[0], state[1], :])+1)

    # METODA MONTE CARLO - ITERACJA WARTOŚCI
    for episode in range(num_of_episodes):
        # ZAINICJUJ STAN POCZATKOWY S
        state_s = np.zeros([2],dtype=int)
        state_s[0] = np.random.randint(0,num_of_rows)

        # ZMIENNE ZATRZYMUJĄCE WEW. PĘTLĘ
        the_end = False
        steps = 0
        # LISTA DO PRZECHOWYWANIA NAGRÓD
        # rewards = []

        while not the_end:
            steps += 1
            action = epsilon_greedy(state_s)
            # WYKONAJ  AKCJĘ A, OBSERWUJ I ZAPAMIĘTAJ R, S', A'
            state_prime, reward = sf.environment(state_s, action, reward_map)

            Q[state_s[0], state_s[1], action -1] = Q[state_s[0], state_s[1], action -1] + alpha * (reward + gamma * np.max(Q[state_prime[0], state_prime[1], :]) - Q[state_s[0], state_s[1], action - 1])

            
            state_s = state_prime   # S <- S'
            # action_a = action # A <- A'

            if (steps == num_of_steps_max) or (state_prime[1] >= num_of_columns - 1):
                the_end = True

        # print(f"Nr epizodu: {episode}")
    rewards_for_q = sf.sailor_test(reward_map, Q, num_of_episodes)

    # sf.draw(reward_map, Q)
    return rewards_for_q


file_name = 'map_small.txt'
# file_name = 'map_easy.txt'
# file_name = 'map_big.txt'
# file_name = 'map_spiral.txt'
maps = ['map_small.txt', 'map_easy.txt', 'map_big.txt', 'map_spiral.txt']
episodes_num = 10000
epsilones = np.linspace(0.1,1.0,10)
# print(epsilon)


for map in maps:
    rewardsy = []
    for e in epsilones:
        rewardsy.append(q_learning(e, episodes_num, map))
    plt.scatter(epsilones, rewardsy)
    plt.xlabel("Epsilon")
    plt.ylabel("Rewards")
    plt.suptitle(f"{map}")
    plt.title("gamma = 0.9, alpha = 0.1")
    plt.show()

