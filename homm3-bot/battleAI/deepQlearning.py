import os

import battleAI.reward as rw
import battleAI.reinforcmentLearningTest as rLT
import data.classes_const as cc
import numpy as np

from keras import backend as k_back
from keras import Sequential
from keras.layers import Dense, Flatten, Input, Conv2D, MaxPooling2D, Dropout, Softmax
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from data.BattleAI_environment_needs import Obstacle, CreatureBox
from image_processing.dictionaries import battle_dict
import copy
import time
import random
import matplotlib.pyplot as plt
import cv2

if __name__ == "__main__":
    os.chdir("../")


def normalize(x):

    return (x - np.min(x[x != -1e3])) / (np.max(x[x != -1e3]) - np.min(x[x != -1e3]))


def exclude_moat(probabilities, moat):
    """
    Sets low probabilities to actions including moat

    :param probabilities numpy array of action probabilities
    :param moat list of hexFields containing moat
    :return:    probabilities with filtered actions
    """

    return np.array([probabilities[i] if (i % 15, i // 15) not in moat else -1000 for i in range(len(probabilities))])


def policy(gameState, deepQAgent, possibleMoves, moat):
    """
    Function choosing action of creature

    :param gameState:   4D array - current state of our environment
    :param deepQAgent:  current agent
    :param possibleMoves:   2D array specifying on which tiles unit can or can't move
    :return:    chosen tile coordinates, chosen action index, indexes of possible actions,actions probabilities
    """
    statesNum = deepQAgent.actionsNum
    rng = np.random.uniform()
    if deepQAgent.training:
        epsilon = deepQAgent.epsilon
    else:
        epsilon = 0                    # epsilon set to 0 when not training
    # flatten possible moves

    not_possible = np.argwhere(possibleMoves.reshape(-1) == 0)
    # with probability = epsilon choose random action
    if rng < epsilon:
        actValues = np.random.random(statesNum[0])
        if moat is not None:
            actValues = exclude_moat(actValues, moat)
        actValues[not_possible] = -1e3

    # with probability = 1 - epsilon choose action based on agents model
    else:
        gameState = gameState.reshape((-1,) + gameState.shape)
        actValues = deepQAgent.mod.predict(gameState, verbose=0)[0]
        if moat is not None:
            actValues = exclude_moat(actValues, moat)
        actValues[not_possible] = -1e3

    # convert action to coordinates of a hex tile
    actIDX = np.argmax(actValues)
    actValues = actValues.reshape(15, 11)
    moveAction = np.unravel_index(actIDX, (15, 11), order='C')

    print("ACTION ", moveAction, "RANDOM: ", rng < epsilon)

    return moveAction, int(actIDX), not_possible, actValues, rng < epsilon


def createTeams(creaturesList, random_team=True):
    """
    Creates random teams

    :param creaturesList: list of instances of class Creature
    :return: list of instances of class CreatureBox
    """
    if random_team:
        creatures = []
        # randomly choose number of stacks for each player
        playerN = np.random.randint(1, 9)
        opponentN = np.random.randint(1, 9)
        # randomly choose initial positions of stacks
        posOpponent = random.sample(range(0, 11), opponentN)
        posPlayer = random.sample(range(0, 11), playerN)

        for idx in range(playerN):
            # randomly choose creature type
            typeIdx = np.random.randint(0, len(creaturesList))
            unitType = creaturesList[typeIdx]
            # randomly choose quantity of creatures in a stack
            quantity = np.random.randint(0, 50)
            creatures.append(rLT.CreatureBox(unitType, (unitType.size - 1, posPlayer[idx]), quantity))
        for idx in range(opponentN):
            # randomly choose creature type
            typeIdx = np.random.randint(0, len(creaturesList))
            unitType = creaturesList[typeIdx]
            # randomly choose quantity of creatures in a stack
            quantity = np.random.randint(0, 50)
            creatures.append(rLT.CreatureBox(unitType, (15 - unitType.size, posOpponent[idx]), quantity, allied=False))

    else:
        creatures = []
        creatures.append(rLT.CreatureBox(copy.deepcopy(battle_dict[5]), (14, 2), 7, allied=False))
        creatures.append(rLT.CreatureBox(copy.deepcopy(battle_dict[5]), (14, 5), 7, allied=False))
        creatures.append(rLT.CreatureBox(copy.deepcopy(battle_dict[5]), (14, 8), 6, allied=False))

        creatures.append(rLT.CreatureBox(copy.deepcopy(battle_dict[65]), (0, 2), 43, allied=True))
        creatures.append(rLT.CreatureBox(copy.deepcopy(battle_dict[140]), (0, 5), 13, allied=True))
        creatures.append(rLT.CreatureBox(copy.deepcopy(battle_dict[141]), (0, 8), 4, allied=True))
    return creatures


def createObstacle(random_obstacles=True):
    """
    Creates random obstacles

    :return: list of instances of class Obstacle
    """

    if random_obstacles:
        obstacles = []

        obstacleN = np.random.randint(0, 10)
        point = random.sample([[x, y] for x in range(2, 13) for y in range(11)], obstacleN)
        for idx in range(obstacleN):
            o = Obstacle(tuple(point[idx]))
            obstacles.append(o)

    else:
        obstacles = []
        # obstacles.append(Obstacle((3, 3)))
        # obstacles.append(Obstacle((4, 3)))
        # obstacles.append(Obstacle((5, 3)))
        # obstacles.append(Obstacle((6, 3)))
        # obstacles.append(Obstacle((6, 4)))
        # obstacles.append(Obstacle((7, 4)))
        # obstacles.append(Obstacle((8, 4)))
        # obstacles.append(Obstacle((9, 5)))
        # obstacles.append(Obstacle((9, 6)))
        # obstacles.append(Obstacle((10, 6)))
        # obstacles.append(Obstacle((11, 7)))
        # obstacles.append(Obstacle((2, 8)))
        # obstacles.append(Obstacle((3, 8)))
        # obstacles.append(Obstacle((8, 9)))

        obstacles.append(Obstacle((2, 4)))
        obstacles.append(Obstacle((3, 4)))
        obstacles.append(Obstacle((8, 2)))
        obstacles.append(Obstacle((9, 2)))
        obstacles.append(Obstacle((10, 2)))
        obstacles.append(Obstacle((10, 3)))
        obstacles.append(Obstacle((10, 4)))
        obstacles.append(Obstacle((8, 6)))
        obstacles.append(Obstacle((9, 6)))
        obstacles.append(Obstacle((10, 6)))



    return obstacles


def resetEnv(creatures, obstacles, training):
    """
    Reset environment

    :param creatures: list of instances of class CreatureBox
    :param obstacles: list of instances of class Obstacle
    :return:
    """
    environment = rLT.Environment(creatures, obstacles, training)
    return environment


class DQNAgent:

    def __init__(self, name, buffer_size=60000, batch_size=64, start_epsilon=.99, min_epsilon=.2, training=True):
        """
        Deep Q learning agent class

        :param name: str - name of the agent
        :param buffer_size: int - size of the buffer in which we remember states, rewards and such
        :param batch_size:  int - size of a batch on which we train the agent each time
        :param start_epsilon:   float - starting possibility of agent choosing random action
        :param min_epsilon: float - minimum value to which possibility of agent choosing random action can decrease
        """
        self.name = name
        self.training = training
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.bufferCounter = 0

        self.inputShape = (15, 11, 7)
        self.actionsNum = (165,)
        self.states = np.zeros(((self.buffer_size,) + self.inputShape))
        self.actions = np.zeros(self.buffer_size, dtype=int)
        self.terminal_states = np.ones(self.buffer_size, dtype=int)

        self.discount = .5
        self.rewards = np.zeros((self.buffer_size, 1))
        self.nextStates = np.zeros(((self.buffer_size,) + self.inputShape))
        self.possibleMovesBuffer = np.zeros(((self.buffer_size,) + self.actionsNum))

        self.epsilon = start_epsilon
        self.min_epsilon = min_epsilon

        self.mod = self.createModel()
        self.target = self.createModel()

        self.target.set_weights(self.mod.get_weights())

    def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond  = k_back.abs(error) <= clip_delta

        squared_loss = 0.5 * k_back.square(error)
        quadratic_loss = 0.5 * k_back.square(clip_delta) + clip_delta * (k_back.abs(error) - clip_delta)

        return k_back.mean(tf.where(cond, squared_loss, quadratic_loss))

    def save(self, observation):
        """
        Saves current move information to a buffer

        :param observation: list - [state, action, reward, nextState, possible moves, bool: is state terminal?]
        :return:
        """
        if self.bufferCounter >= self.buffer_size:
            self.bufferCounter = self.buffer_size
            self.states = np.delete(self.states, 0, axis=0)
            self.actions = np.delete(self.actions, 0, axis=0)
            self.rewards = np.delete(self.rewards, 0, axis=0)
            self.nextStates = np.delete(self.nextStates, 0, axis=0)
            self.possibleMovesBuffer = np.delete(self.possibleMovesBuffer, 0, axis=0)
            self.terminal_states = np.delete(self.terminal_states, 0, axis=0)

            idx = self.bufferCounter
            self.states = np.append(self.states, observation[0].reshape((1,)+observation[0].shape), axis=0)
            self.actions = np.append(self.actions, [observation[1]], axis=0)
            self.rewards = np.append(self.rewards, [[observation[2]]], axis=0)
            self.nextStates = np.append(self.nextStates, observation[3].reshape((1,)+observation[3].shape), axis=0)
            temp = np.zeros((1, self.possibleMovesBuffer.shape[1]))
            temp[0, observation[4]] = 1
            self.possibleMovesBuffer = np.append(self.possibleMovesBuffer, temp, axis=0)
            self.terminal_states = np.append(self.terminal_states, [int(not observation[5])], axis=0)

        else:
            idx = self.bufferCounter
            self.states[idx] = observation[0]
            self.actions[idx] = observation[1]
            self.rewards[idx] = observation[2]
            self.nextStates[idx] = observation[3]
            temp = np.zeros(self.possibleMovesBuffer.shape[1])
            temp[observation[4]] = 1
            self.possibleMovesBuffer[idx] = temp
            self.terminal_states[idx] = int(not observation[5])

        self.bufferCounter += 1

    def createModel(self):
        """
        creates the neural network model

        :return: neural network model
        """
        model = Sequential()

        model.add(Input(shape=self.inputShape))

        model.add(Conv2D(filters=64, kernel_size=2, strides=(2, 2), activation='relu'))
        model.add(Conv2D(filters=128, kernel_size=2, strides=(2, 2), activation='relu'))
        model.add(Conv2D(filters=256, kernel_size=2, strides=(2, 2), activation='relu'))
        model.add(Flatten())

        model.add(Dense(self.actionsNum[0], activation='linear'))
        # model.add(Conv2D(256, (3, 3), activation='relu'))
        # model.add(MaxPooling2D((2, 2)))
        #
        # model.add(Conv2D(512, (3, 3), activation='relu'))
        # model.add(MaxPooling2D((2, 2)))
        #
        # model.add(Flatten())

        # model.add(Dense(512))
        # model.add(Dense(256))
        # model.add(Dense(256))
        # model.add(Dense(512))
        # model.add(Dense(1024))
        # model.add(Dense(2048))
        # model.add(Dense(1024))
        # model.add(Dense(512))
        # model.add(Dense(256))
        # model.add(Dense(self.actionsNum[0], activation='linear'))
        model.compile(optimizer=Adam(learning_rate=0.001), loss=self._huber_loss, metrics=['accuracy'])
        model.summary()
        return model

    # update the agent
    def update(self, stateBatch, actionBatch, rewardBatch, nextStateBatch, possibleIdxsBatch, terminal_statesBatch):
        """
        updates the agent

        :param stateBatch: list - batch of states
        :param actionBatch: list - batch of actions
        :param rewardBatch: list - batch of rewards
        :param nextStateBatch: list - batch of next states
        :param possibleIdxsBatch: list - batch of possible moves
        :param terminal_statesBatch: list - batch of information whether the state is terminal
        """
        # get predicted Q values
        predictedQs = self.mod.predict(stateBatch, verbose=0)
        targetQs = np.copy(predictedQs)
        # get next Q values
        nextQs = self.target.predict(nextStateBatch, verbose=0)

        batchIdx = np.arange(self.batch_size, dtype=np.int32)
        # get target Q values:
        targetQs[batchIdx, actionBatch] = rewardBatch.reshape(-1) + terminal_statesBatch*self.discount * np.max(nextQs, axis=1)

        # train the model
        self.mod.fit(stateBatch, targetQs, batch_size=self.batch_size, epochs=1, verbose=1)

    def learn(self):
        """
        samples random batch of transitions and calls the update method of the agent
        """
        if self.bufferCounter < self.batch_size:
            return
        batchIndxes = np.random.choice(min(self.buffer_size,self.bufferCounter), self.batch_size)

        stateBatch = self.states[batchIndxes]
        actionBatch = self.actions[batchIndxes]
        rewardBatch = self.rewards[batchIndxes]
        nextStateBatch = self.nextStates[batchIndxes]
        possibleIdxsBatch = self.possibleMovesBuffer[batchIndxes]
        terminal_statesBatch = self.terminal_states[batchIndxes]

        self.update(stateBatch, actionBatch, rewardBatch, nextStateBatch, possibleIdxsBatch, terminal_statesBatch)


def saveBuffer(deepQAgent, path):
    """
    Saves the buffer to numpy files

    :param deepQAgent: DQNAgent class instance
    :param path: path to which the files should be saved
    """
    np.save(path + deepQAgent.name + "_states.npy", deepQAgent.states)
    np.save(path + deepQAgent.name + "_actions.npy", deepQAgent.actions)
    np.save(path + deepQAgent.name + "_rewards.npy", deepQAgent.rewards)
    np.save(path + deepQAgent.name + "_nextStates.npy", deepQAgent.nextStates)
    np.save(path + deepQAgent.name + "_buffercounter.npy", np.array([min(deepQAgent.bufferCounter, deepQAgent.buffer_size)]))
    print(f"save: {deepQAgent.name}")


def loadBuffer(deepQAgent, path):
    """
    Loads the buffer from the numpy files if they exist

    :param deepQAgent: DQNAgent class instance
    :param path: path from which the files should be loaded
    """
    try:
        deepQAgent.states = np.load(path + deepQAgent.name + "_states.npy")
        deepQAgent.actions = np.load(path + deepQAgent.name + "_actions.npy")
        deepQAgent.rewards = np.load(path + deepQAgent.name + "_rewards.npy")
        deepQAgent.nextStates = np.load(path + deepQAgent.name + "_nextStates.npy")

        deepQAgent.bufferCounter = np.load(path + deepQAgent.name + "_buffercounter.npy")[0]
        print(f"load: {deepQAgent.name}")
    except:
        print("Error while loading files")


def saveWeights(deepQAgent, path):
    """
    Saves the weights of the agent

    :param deepQAgent: DQNAgent class instance
    :param path: path to which the weights should be saved
    """
    deepQAgent.mod.save_weights(path + deepQAgent.name + "_weights.h5")
    print(f"save weight: {deepQAgent.name}")


def loadWeights(deepQAgent, path):
    """
    Loads the weights of the agent if they exist

    :param deepQAgent: DQNAgent class instance
    :param path: path from which the weights should be loaded
    """
    try:
        deepQAgent.mod.load_weights(path + deepQAgent.name + "_weights.h5")

        deepQAgent.target.set_weights(deepQAgent.mod.get_weights())
        print(f"load weight: {deepQAgent.name}")
    except:
        print("Error while loading files")


def learningProccess():
    """
    Starts the learning process of our agents
    """
    playerAgent = DQNAgent("player", buffer_size=5_000, start_epsilon=.4, min_epsilon=.3, training=True)
    opponentAgent = DQNAgent("opponent", buffer_size=1, start_epsilon=1.0, min_epsilon=1.0, training=True)

    folderPath = "./battleAI/battleModel"
    loadBuffer(playerAgent, folderPath)
    loadBuffer(opponentAgent, folderPath)

    loadWeights(playerAgent, folderPath)
    loadWeights(opponentAgent, folderPath)

    creaturesList = [getattr(cc, item) for item in dir(cc) if isinstance(getattr(cc, item), cc.Creature)]
    env = rLT.Environment(createTeams(creaturesList, False), [], playerAgent.training)

    tmp = 0
    checkpointVal = 200
    stepAlly = 0
    stepEnemy = 0
    rew = 0
    episode = 0

    printInfo = False
    # main loop
    while True:
        print("NEW EPISODE--------------------------------------------------------------------------------------")
        c = createTeams(creaturesList, False)
        o = createObstacle(False)
        env = resetEnv(c, o, True)
        reward = rw.Reward(env)
        episode += 1

        currUnit = env.queue.queue[-1]  # get current unit from queue
        _, posibleMoves = rLT.Environment.choosePossibleMoves(env, currUnit)
        # get state and prepare it to feed it into neural network
        state = env.prepareInputForNN(currUnit)
        fig, ax = plt.subplots(1, 2, figsize=(5, 2))
        game = ax[0].imshow(cv2.transpose(state[:, :, 0]))
        possible_plot = ax[1].imshow(cv2.transpose(state[:, :, 0]))
        reward.done = False
        observ = []
        waiting = False
        battle_result = 0
        cumulative_rew = [0, 0]
        one_more = True
        while not reward.done or one_more:
            if reward.done and one_more:
                one_more = False
            if printInfo:
                if rew != 0: env.printEnvironment()
            currUnit = env.queue.queue[-1]  # get current unit from queue
            _, posibleMoves = rLT.Environment.choosePossibleMoves(env, currUnit)
            state = env.prepareInputForNN(currUnit)
            prevHP = reward.getTeamHP(currUnit, False)
            reward.saveUnitHealth(currUnit)
            # choose agent according to unit side
            if (currUnit.ally and one_more) or (not currUnit.ally and not one_more):
                agent = playerAgent
                stepAlly += 1
                step = stepAlly
            else:
                agent = opponentAgent
                stepEnemy += 1
                step = stepEnemy

            # get action based on policy
            action, actIdx, possibleIdxs, possibilities, random_move = policy(state, agent, posibleMoves, env.moat)
            if printInfo: print("Current position: ", currUnit.field, "Destination: ", action)
            # perform an action

            game.set_data(cv2.transpose(state[:, :, 0]))
            if agent.name == 'player' and not random_move:
                possible_plot.set_data(cv2.transpose(normalize(possibilities)))
            fig.canvas.draw_idle()
            plt.pause(0.01)
            env.moveCreature(action)

            # get next state
            newState = env.prepareInputForNN(currUnit)
            # plt.draw()
            # calculate reward
            if battle_result == 0:
                rew, battle_result = reward.calcReward(currUnit, env)
            else:
                temp = [i.ally for i in env.queue.queue]
                allies_num = temp.count(True)
                enemies_num = temp.count(False)
                battle_result = 1 if allies_num > enemies_num else -1
                rew = battle_result * 10 if battle_result > 0 else 0
            cumulative_rew[0 if agent.name == 'player' else 1] += rew
            if printInfo: print("Estimated reward: ", rew)

            # save transition into agents memory

            # if next mob is enemy and current ally and its not over then store observation in list
            if not env.queue.queue[-1].ally and currUnit.ally and one_more:
                observ.append((state, actIdx, rew, newState, possibleIdxs, reward.done))
                waiting = True
                waiting_ally = currUnit

            # if current mob is ally and has observations in list or its over
            elif (currUnit.ally and waiting) or (not one_more and not currUnit.ally):
                for observation in observ:
                    if not one_more:
                        observation = list(observation)
                        observation[2] = rew
                        observation = tuple(observation)
                    else:
                        observation = list(observation)
                        observation[2] = 0 if waiting_ally.prevHP > waiting_ally.stackHP and waiting_ally.damage_dealt == 0 \
                            else observation[2] + 10
                        observation = tuple(observation)
                    playerAgent.save(observation)
                    playerAgent.learn()
                waiting_ally.prevHP = waiting_ally.stackHP
                observ = []
                if currUnit.ally and not env.queue.queue[-1].ally:
                    observ.append((state, actIdx, rew, newState, possibleIdxs, reward.done))
                    waiting_ally = currUnit
                elif one_more:
                    agent.save((state, actIdx, rew, newState, possibleIdxs, reward.done))
                    waiting = False
                    # update model
                    agent.learn()
            elif one_more:
                agent.save((state, actIdx, rew, newState, possibleIdxs, reward.done))
                # update model
                agent.learn()
            else:
                break

            # update state
            # state = newState
            time.sleep(tmp)

            if step % 100 == 0:
                agent.target.set_weights(agent.mod.get_weights())
            if step % checkpointVal == 0:
                saveBuffer(agent, folderPath)
                saveWeights(agent, folderPath)

            step += step
            # currUnit.prevHP = currUnit.stackHP
        if episode > 0:
            if playerAgent.epsilon > playerAgent.min_epsilon:
                playerAgent.epsilon *= .99
            else:
                playerAgent.epsilon = playerAgent.min_epsilon
        print("GAME REWARD = ", cumulative_rew)
        with open("rewards.txt", 'a') as f:
            f.write(f'Ally: {cumulative_rew[0]} Enemy: {cumulative_rew[1]}, result {"Ally" if battle_result == 1 else "Enemy"} won \n')
        plt.close(fig)

if __name__ == "__main__":
    learningProccess()
