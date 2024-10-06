import time
import os
import pdb
import numpy as np
import matplotlib.pyplot as plt
import sailor_funct as sf

number_of_episodes = 1000                   # number of training epizodes (multi-stage processes) 
gamma = 1.0                                 # discount factor


file_name = 'map_small.txt'
# file_name = 'map_easy.txt'
# file_name = 'map_big.txt'
# file_name = 'map_spiral.txt'
# file_name = 'map_middle.txt'

reward_map = sf.load_data(file_name)
num_of_rows, num_of_columns = reward_map.shape

num_of_steps_max = int(5*(num_of_rows + num_of_columns))    # maximum number of steps in an episode
Q = np.zeros([num_of_rows, num_of_columns, 4], dtype=float)  # trained usability table of <state,action> pairs
sum_of_rewards = np.zeros([number_of_episodes], dtype=float)

# miejsce na algorytm uczenia - modelem jest tablica Q
# (symulację epizodu można wziąć z funkcji sailor_test())
# ............................


def state_prob(state, action, next_state):
    a = action - 1
    left_state = [state[0], max(0, state[1] - 1)]
    right_state = [state[0], min(num_of_columns - 1, state[1] + 1)]
    up_state = [max(0, state[0] - 1), state[1]]
    down_state = [min(num_of_rows - 1, state[0] + 1), state[1]]

    probability_table = [
        [0.02, 0.78, 0.1, 0.1],
        [0.1, 0.1, 0.78, 0.02],
        [0.78, 0.02, 0.1, 0.1],
        [0.1, 0.1, 0.02, 0.78]
    ]
    
    probability = 0
    states = [left_state, right_state, up_state, down_state]
    for i, state in enumerate(states):
        if next_state == state:
            probability += probability_table[a][i]

    return probability

def state_reward(state, next_state):
    if next_state[0] == state[0] and next_state[1] == state[1]:
        return -2
    elif next_state[0] < 0 or next_state[0] >= num_of_rows:
        return -2
    elif next_state[1] < 0 or next_state[1] >= num_of_columns:
        return -2
    else:
        return reward_map[next_state[0], next_state[1]]

def next_states(state):
    x, y = state
    potential_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    states = []

    states.append([x, y])
    for dx, dy in potential_moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < num_of_rows and 0 <= new_y < num_of_columns:
            states.append([new_x, new_y])

    return states

IT_LIMIT = number_of_episodes
ERROR = 0.000001
gamma = 0.9
err = ERROR

limit=0
# TABLICA WARTOŚCI STANÓW WYPEŁNIONA ZERAMI
V=np.zeros([num_of_rows, num_of_columns], dtype=float)
while limit < IT_LIMIT and err >= ERROR:
    # TABLICA DO WIZUALIZACJI WYNIKÓW
    Q = np.zeros([num_of_rows, num_of_columns, 4], dtype=float)
    # VPOM <- V
    v_pom = np.copy(V)
    # ERROR <- 0
    err=0
    # ITERACJA PO STANACH
    for (i,j), _ in np.ndenumerate(V[:,:-1]):
        # STAN POCZATKOWY
        state = (i, j)
        # SPRAWDZENIE MOZLIWYCH RUCHOW DLA DANEGO STATE
        possible_states = next_states(state)
        # PUSTA TABLICA VS
        Vs = []

        for action in range(1,5):
            avg_reward = 0
            avg_v = 0
            for next_state in possible_states:
                p = state_prob(state, action, next_state)
                r = state_reward(state, next_state)
                v = v_pom[next_state[0], next_state[1]]
                avg_reward += p * r
                avg_v += p * v

            result = avg_reward + gamma * avg_v
            Vs.append(result)
            Q[state[0], state[1], action - 1] = result
        V[state[0], state[1]]= max(Vs)
        err = max(err, abs(V[state[0], state[1]] - v_pom[state[0], state[1]]))
    limit += 1
    print(f"Iteracja {limit}: {err}")

result_reward = sf.sailor_test(reward_map, Q, 1000)
sf.draw(reward_map, Q, file_name, result_reward, limit, err)
