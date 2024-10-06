import time
import os
import pdb
import numpy as np
import matplotlib.pyplot as plt
import sailor_funct as sf

number_of_episodes = 1000                   # number of training epizodes (multi-stage processes) 
gamma = 1.0                                 # discount factor


file_name = 'map_small.txt'
#file_name = 'map_easy.txt'
#file_name = 'map_big.txt'
#file_name = 'map_spiral.txt'

reward_map = sf.load_data(file_name)
num_of_rows, num_of_columns = reward_map.shape

num_of_steps_max = int(5*(num_of_rows + num_of_columns))    # maximum number of steps in an episode
Q = np.zeros([num_of_rows, num_of_columns, 4], dtype=float)  # trained usability table of <state,action> pairs
sum_of_rewards = np.zeros([number_of_episodes], dtype=float)

# miejsce na algorytm uczenia - modelem jest tablica Q
# (symulację epizodu można wziąć z funkcji sailor_test())
# ............................


def state_prob(state, action, next_state):
    left_state = [0, 0]
    left_state[0] = state[0]
    left_state[1] = state[1] - 1
    if left_state[1] < 0 or left_state[1] >= num_of_columns:
        left_state[0] = state[0]
        left_state[1] = state[1]

    right_state = [0, 0]
    right_state[0] = state[0]
    right_state[1] = state[1] + 1
    if right_state[1] < 0 or right_state[1] >= num_of_columns:
        right_state[0] = state[0]
        right_state[1] = state[1]

    up_state = [0, 0]
    up_state[0] = state[0] - 1
    up_state[1] = state[1]
    if up_state[0] < 0 or up_state[0] >= num_of_rows:
        up_state[0] = state[0]
        up_state[1] = state[1]

    down_state = [0, 0]
    down_state[0] = state[0] + 1
    down_state[1] = state[1]
    if down_state[0] < 0 or down_state[0] >= num_of_rows:
        down_state[0] = state[0]
        down_state[1] = state[1]

    probs = [
        [0.02, 0.78, 0.1, 0.1],
        [0.1, 0.1, 0.78, 0.02],
        [0.78, 0.02, 0.1, 0.1],
        [0.1, 0.1, 0.02, 0.78]
    ]
    p = 0
    if next_state[0] == left_state[0] and next_state[1] == left_state[1]:
        p += probs[action - 1][0]
    if next_state[0] == right_state[0] and next_state[1] == right_state[1]:
        p += probs[action - 1][1]
    if next_state[0] == up_state[0] and next_state[1] == up_state[1]:
        p += probs[action - 1][2]
    if next_state[0] == down_state[0] and next_state[1] == down_state[1]:
        p += probs[action - 1][3]

    return p

def state_reward(state, next_state):
    if next_state[0] == state[0] and next_state[1] == state[1]:
        return -10
    else:
        return reward_map[next_state[0], next_state[1]]

def next_states(state):
    states = []

    states.append([state[0], state[1]])
    if state[0] + 1 < num_of_rows:
        states.append([state[0] + 1, state[1]])
    if state[0] - 1 >= 0:
        states.append([state[0] - 1, state[1]])
    if state[1] + 1 < num_of_columns:
        states.append([state[0], state[1] + 1])
    if state[1] - 1 >= 0:
        states.append([state[0], state[1] - 1])

    return states

IT_LIMIT = number_of_episodes
ERROR = 0.000001
gamma = 0.8
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
                avg_reward+=p*r
                avg_v += p*v

            Vs.append(avg_reward + gamma * avg_v)
            Q[state[0], state[1], action - 1] = avg_reward + gamma * avg_v
        V[state[0], state[1]]= max(Vs)
        err = max(err, abs(V[state[0],state[1]]-v_pom[state[0],state[1]]))
    limit+=1
    print(limit, err)


sf.sailor_test(reward_map, Q, 1000)
sf.draw(reward_map,Q)
