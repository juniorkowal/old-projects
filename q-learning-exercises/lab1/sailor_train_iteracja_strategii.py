import time
import os
import pdb
import numpy as np
import matplotlib.pyplot as plt
import sailor_funct as sf

num_of_episodes = 1000                   # number of training epizodes (multi-stage processes) 
gamma = 0.99                                 # discount factor


file_name = 'map_small.txt'
#file_name = 'map_easy.txt'
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
pi = np.ones((num_of_rows, num_of_columns), dtype=int)
pi_pom = np.zeros((num_of_rows, num_of_columns), dtype=int)
num_while = 0

while not np.array_equal(pi, pi_pom) and num_while < 50:
    pi_pom = np.copy(pi)
    
    for (i, j, k), _ in np.ndenumerate(Q):    # ITERACJA PO WSZYSTKICH PARACH (s,a)
        rewards = []
        for episode in range(num_of_episodes):
            # INICJOWANIE POCZĄTKOWEGO STANU I AKCJI
            state_s = (i, j)
            action_a = 1 + k
            # ZMIENNE ZATRZYMUJĄCE WEW. PĘTLĘ
            the_end = False
            steps = 0
            # LISTA DO PRZECHOWYWANIA NAGRÓD
            

            while not the_end:
                steps += 1
                
                # WYKONAJ  AKCJĘ A, OBSERWUJ I ZAPAMIĘTAJ R, S', A'
                state_prime, reward = sf.environment(state_s, action_a, reward_map)
                action_prime = pi[state_prime[0], state_prime[1]]
                
                # DODAJ NAGRODĘ ZA AKCJĘ DO LISTY NAGRÓD
                rewards.append(reward)
                
                state_s = state_prime   # S <- S'
                action_a = action_prime # A <- A'

                if (steps == num_of_steps_max) or (state_prime[1] >= num_of_columns - 1):
                    the_end = True

        # UZUPEŁNIANIE TABLICY WARTOŚCI AKCJI WEDŁUG WZORU
        rewards = np.array(rewards)
        discounts = np.power(gamma, np.arange(1, len(rewards) + 1))
        reward_sum = np.sum(rewards * discounts)
        Q[i, j, k] = reward_sum / num_of_episodes

    for (i, j, _), _ in np.ndenumerate(Q):
        pi[i, j] = 1 + np.argmax(Q[i, j, :])

    num_while += 1
    print(f"Numer iteracji: {num_while}")


sf.sailor_test(reward_map, Q, num_of_episodes)
sf.draw(reward_map, Q)
