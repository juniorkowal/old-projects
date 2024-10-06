import numpy as np
import pdb
import animat_fun as afun

# # from lecture
# type_of_map = -1          
# obs_size = 3
# if_cross = True

# # middle:
# type_of_map = 3          
# obs_size = 3
# if_cross = False

# hard:
type_of_map = 3          
obs_size = 7
if_cross = False

def animat_train(type_of_map, obs_size = 3, if_cross = False):
    gamma = 0.97   # can be changed in training and test for the same value
    # alpha = ...
    # epsilon = ...
    number_of_episodes = 100
    strategy = []

    for epi in range(number_of_episodes):
        map = afun.generate_map(type_of_map)  # can be generated for more than one episode
        num_of_rows, num_of_columns = np.shape(map)
        position = afun.start_position(map)
        max_num_of_steps = 4*(num_of_rows + num_of_columns)
        
        if_end = False 
        step_number = 0
        sum_of_discounted_rewards = 0
        cumulated_gamma = 1

        while (if_end == False):                           # episode steps loop
            step_number += 1
            
            # square region observed by agent:
            observation = afun.observable_region(map, obs_size, position, if_cross)
           

            # action based on observation: (from current strategy with exploration)
            # .....................................
            # ...... set your code here! ..........
            # .....................................
            # action = my_action(strategy, observation) 
            action = np.random.randint(4)     # temporarily random action

            new_position, reward = afun.transition_and_reward(map,position,action)

            # strategy modification or pushing experience into replay memory:
            # .....................................
            # ...... set your code here! ..........
            # .....................................
            # strategy = ......
            # replay memory <- ....

            if (reward > 0)|(step_number > max_num_of_steps):
                if_end = True

            position = new_position
            sum_of_discounted_rewards += reward*cumulated_gamma
            cumulated_gamma *= gamma

        # optional strategy modification based on replay memory:
        # .....................................
        # ...... set your code here! ..........
        # .....................................
        # strategy = ......
    
    return strategy   # approximator of strategy or pair of approximators if actor-critic

def animat_test(strategy, type_of_map, obs_size = 3, if_cross = False):
    gamma = 0.97 # can be changed in training and test for the same value
    number_of_episodes = 100

    mean_sum_of_discounted_rewards = 0

    for epi in range(number_of_episodes):
        map = afun.generate_map(type_of_map)  # can be generate for more than one episode
        num_of_rows, num_of_columns = np.shape(map)
        position = afun.start_position(map)
        max_num_of_steps = 4*(num_of_rows + num_of_columns)
        
        if_end = False 
        step_number = 0
        sum_of_discounted_rewards = 0
        cumulated_gamma = 1
        path = []

        while (if_end == False):                           # episode steps loop
            step_number += 1
            
            # square region observed by agent:
            observation = afun.observable_region(map, obs_size, position, if_cross)
            #print(str(observation))

            # action based on observation: (from given strategy)
            # .....................................
            # ...... set your code here! ..........
            # .....................................
            # e.g.
            # action = my_action(strategy, observation) 
            action = np.random.randint(4)     # temporarily random action

            new_position, reward = afun.transition_and_reward(map,position,action)

            path.append([*position, action, *new_position, reward])

            if (reward > 0)|(step_number > max_num_of_steps):
                if_end = True

            position = new_position
            sum_of_discounted_rewards += reward*cumulated_gamma
            cumulated_gamma *= gamma

        mean_sum_of_discounted_rewards += sum_of_discounted_rewards/number_of_episodes

        print("episode " + str(epi) + ": steps = " + str(step_number) + " sum_of_rewards = " + str(sum_of_discounted_rewards))

        if epi < 5:
            afun.save_map_and_path(map, path, epi)
            afun.save_text_animation(map, path, epi)

    print("after " + str(number_of_episodes) + " episodes:")
    print("mean sum of discounted rewards = " + str(mean_sum_of_discounted_rewards))
    
strategy = animat_train(type_of_map, obs_size, if_cross)
animat_test(strategy, type_of_map, obs_size, if_cross)


