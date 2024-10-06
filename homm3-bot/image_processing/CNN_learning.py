"""Script containing neural network classes that we use in obstacle/creature in queue recognition"""
import json
import os
import random

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models


class CNN:

    def __init__(self, size: tuple = (33, 33, 3), path: str = "./model/model/", num_of_classes: int = 69):
        """
        Class representing convolutional neural network that we use to recognize obstacles

        :param size: size of each image
        :param path: path to folder containing weight files
        :param num_of_classes: number of neural network outputs
        """
        self.test_loss = 0
        self.test_acc = 0
        self.size = size
        self.learning_images = []
        self.learning_labels = []
        self.test_labels = []
        self.test_images = []
        self.dictionary = dict()
        self.size = size
        self.checkpoint_path = path
        self.model = models.Sequential()
        self.model.add(layers.Rescaling(1. / 255, input_shape=(size)))
        #self.model.add(layers.Conv2D(64, (4,4), padding='same', activation='relu'))
        self.model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
        self.model.add(layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
        #self.model.add(layers.Dropout(0.1))
        #self.model.add(layers.Conv2D(64, (4,4), padding='same', activation='relu'))
        self.model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
        #self.model.add(layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
        #self.model.add(layers.Dropout(0.1))
        #self.model.add(layers.Conv2D(64, (4,4), padding='same', activation='relu'))
        #self.model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
        #self.model.add(layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
        #self.model.add(layers.Dropout(0.1))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(512, activation='relu'))
        self.model.add(layers.Dropout(0.4))
        self.model.add(layers.Dense(1024, activation='relu'))
        self.model.add(layers.Dropout(0.4))
        self.model.add(layers.Dense(256, activation='relu'))
        self.model.add(layers.Dense(num_of_classes, activation='softmax'))
        self.model.summary()

    def add_learning_images(self, path_to_directory: str = '../structures/'):
        """
        function adding learning dataset for neural network

        :param path_to_directory: path to directory containing dataset for function
        """
        temp2 = []
        temp3 = []
        i = 0
        for dirname in os.listdir(path_to_directory):
            temp2.append(dirname)
            temp3.append(i)
            i = i + 1
            for filename in os.listdir(os.path.join(path_to_directory,dirname)):
                img = cv2.imread(os.path.join(path_to_directory, dirname, filename))
                if img is not None:
                    # img2 = img.copy()
                    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    #
                    # img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
                    #
                    # edges = cv2.Canny(image=img_blur, threshold1=50, threshold2=200)
                    #
                    # erosion = cv2.erode(edges, (0.7, 0.7), iterations=1)
                    #
                    # img = cv2.dilate(erosion, (0.7, 0.7), iterations=10)
                    # img = cv2.bitwise_and(img2, img2, mask=img)
                    img = cv2.resize(img,(self.size[1],self.size[0]))
                    self.learning_images.append(img)
                self.learning_labels.append(dirname)
        temp = list(zip(self.learning_images,self.learning_labels))
        random.shuffle(temp)
        self.learning_images, self.learning_labels = zip(*temp)
        self.learning_images = list(self.learning_images)
        self.learning_labels = list(self.learning_labels)
        self.dictionary = dict(zip(temp2,temp3))
        self.learning_labels = [*map(self.dictionary.get, self.learning_labels)]

    def add_test_images(self, path_to_directory: str = './test/'):
        """
        function adding test dataset for neural network

        :param path_to_directory: path to directory containing dataset for function
        """
        for dirname in os.listdir(path_to_directory):
            for filename in os.listdir(os.path.join(path_to_directory,dirname)):
                img = cv2.imread(os.path.join(path_to_directory, dirname, filename))
                if img is not None:
                    # img2 = img.copy()
                    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    #
                    # img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
                    #
                    # edges = cv2.Canny(image=img_blur, threshold1=50, threshold2=200)
                    #
                    # erosion = cv2.erode(edges, (0.7, 0.7), iterations=1)
                    #
                    # img = cv2.dilate(erosion, (0.7, 0.7), iterations=10)
                    # img = cv2.bitwise_and(img2, img2, mask=img)
                    img = cv2.resize(img,(self.size[1],self.size[0]))
                    self.test_images.append(img)
                self.test_labels.append(dirname)
        self.test_images = list(self.test_images)
        self.test_labels = list(self.test_labels)
        self.test_labels = [*map(self.dictionary.get, self.test_labels)]

    def train_network(self):
        """
        function training and evaluating neural network, needs earlier 2 function to be called before being able to work
        """
        jsondict = json.dumps(self.dictionary)
        f = open(self.checkpoint_path + "dict.json", "w")
        f.write(jsondict)
        f.close
        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                           metrics=['accuracy'])
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./logs")
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path+"model", save_weights_only=True, verbose=1)
        self.model.fit(np.array(self.learning_images), np.array(self.learning_labels), epochs=120,
                       validation_split=0, shuffle=True,
                       callbacks=[cp_callback],batch_size=64)
        self.test_loss, self.test_acc = self.model.evaluate(np.array(self.test_images), np.array(self.test_labels),verbose=2)

    def test_network(self):
        """
        function evaluating neural network
        """
        self.test_loss,self.test_acc = self.model.evaluate(np.array(self.test_images), np.array(self.test_labels),verbose=2)

    def load_model(self):
        """
        function loading weightfiles from path specified in init
        """
        self.model.load_weights(self.checkpoint_path+"model").expect_partial()
        with open(self.checkpoint_path + "dict.json" ) as file:
            self.dictionary = json.load(file)
        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                           metrics=['accuracy'])


class DumbNN:
    def __init__(self, size: tuple = (33, 33, 3), path: str = "./models/model/", num_of_classes: int = 165):
        """
        Class representing neural network that we use to recognise creatures in the queue

        :param size: size of each image
        :param path: path to folder containing weight files
        :param num_of_classes: number of neural network outputs
        """
        self.test_loss = 0
        self.test_acc = 0
        self.size = size
        self.learning_images = []
        self.learning_labels = []
        self.test_labels = []
        self.test_images = []
        self.dictionary = dict()
        self.checkpoint_path = path
        self.model = models.Sequential()
        self.model.add(layers.Rescaling(1. / 255, input_shape=size))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(num_of_classes, activation='softmax'))
        self.model.summary()

    def add_learning_images(self, path_to_directory: str = '../unit_portraits/'):
        """
        function adding learning dataset for neural network

        :param path_to_directory: path to directory containing dataset for function
        """
        temp2 = []
        temp3 = []
        i = 0
        for filename in os.listdir(path_to_directory):
            temp2.append(filename[:-4])
            temp3.append(i)
            i = i + 1
            img = cv2.imread(os.path.join(path_to_directory, filename))
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img,(self.size[1],self.size[0]))
                self.learning_images.append(img)
            self.learning_labels.append(filename[:-4])
        temp = list(zip(self.learning_images,self.learning_labels))
        random.shuffle(temp)
        self.learning_images, self.learning_labels = zip(*temp)
        self.learning_images = list(self.learning_images)
        self.learning_labels = list(self.learning_labels)
        self.dictionary = dict(zip(temp2,temp3))
        self.learning_labels = [*map(self.dictionary.get, self.learning_labels)]

    def add_test_images(self, path_to_directory: str = '../queue_test/'):
        """
        function adding test dataset for neural network

        :param path_to_directory: path to directory containing dataset for function
        """
        for filename in os.listdir(path_to_directory):
            img = cv2.imread(os.path.join(path_to_directory, filename))
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
                img = cv2.resize(img, (self.size[1], self.size[0]))
                self.test_images.append(img)
            self.test_labels.append(filename[:-4])
        self.test_images = list(self.test_images)
        self.test_labels = list(self.test_labels)
        self.test_labels = [*map(self.dictionary.get, self.test_labels)]

    def train_network(self):
        """
        function training and evaluating neural network, needs earlier 2 function to be called before being able to work
        """
        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                           metrics=['accuracy'])
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./logs")
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path+"model", save_weights_only=True, verbose=1)
        self.model.fit(np.array(self.learning_images), np.array(self.learning_labels), epochs=600,
                       validation_split=0, shuffle=True,
                       callbacks=[cp_callback], batch_size=64)
        self.test_loss, self.test_acc = self.model.evaluate(np.array(self.test_images), np.array(self.test_labels),verbose=2)
        jsondict = json.dumps(self.dictionary)
        f = open(self.checkpoint_path + "dict.json", "w")
        f.write(jsondict)
        f.close

    def test_network(self):
        """
        function evaluating neural network
        """
        self.test_loss,self.test_acc = self.model.evaluate(np.array(self.test_images), np.array(self.test_labels),verbose=2)

    def load_model(self):
        """
        function loading weightfiles from path specified in init
        """
        self.model.load_weights(self.checkpoint_path+"model").expect_partial()
        with open(self.checkpoint_path + "dict.json" ) as file:
            self.dictionary = json.load(file)
        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                           metrics=['accuracy'])


def train_queue_NN():
    """
    helper function for creating and training of specyfic neural network
    """
    queueNN = DumbNN((38,36,1),"./model/queue/", 166)
    queueNN.add_learning_images('../unit_portraits/')
    queueNN.add_test_images('../queue_test/')
    queueNN.train_network()


def try_queue_NN():
    """
    helper function for loading and testing of specyfic neural network
    """
    queueNN = DumbNN((38, 36, 1), "./model/queue/", 166)
    queueNN.load_model()
    queueNN.add_test_images('../queue_test/')
    queueNN.test_network()

def train_unit_NN():
    """
    helper function for creating and training of specyfic neural network
    """
    queueNN = DumbNN((53,59,1),"./model/unit/", 166)
    queueNN.add_learning_images('./unit_portraits/')
    queueNN.add_test_images('./queue_test/')
    queueNN.train_network()


def try_unit_NN():
    """
    helper function for loading and testing of specyfic neural network
    """
    queueNN = DumbNN((53, 59, 1), "./model/unit/", 166)
    queueNN.load_model()
    queueNN.add_test_images('./queue_test/')
    queueNN.test_network()
def train_artifact_NN():
    """
    helper function for creating and training of specyfic neural network
    """
    artifactNN = DumbNN((40,40,3),"./model/artifact/", 156)
    artifactNN.add_learning_images('../artifacts/')
    artifactNN.add_test_images('../artifact_test/')
    artifactNN.train_network()


def try_artifact_NN():
    """
    helper function for loading and testing of specyfic neural network
    """
    artifactNN = CNN((40, 40, 3), "./model/artifact/", 156)
    artifactNN.load_model()
    artifactNN.add_test_images('../artifact_test/')
    artifactNN.test_network()


def train_creatures_NN():
    """
    helper function for creating and training of specyfic neural network
    """
    CreatureNN = CNN((17,9,3),"./model/creatures/", 167)
    CreatureNN.add_learning_images('../ds/')
    CreatureNN.add_test_images('../ds_test/')
    CreatureNN.train_network()


def try_creatures_NN():
    """
    helper function for loading and testing of specyfic neural network
    """
    CreatureNN = CNN((17,9,3),"./model/creatures/", 167)
    CreatureNN.load_model()
    CreatureNN.add_test_images('../ds_test/')
    CreatureNN.test_network()

def abomination(): #dont look at that, only for checking what errors from network we are receving
    """
    just dont
    function created for finding which classes of output is giving most errors in first iteration of neural network based image recognition

    :return: list containing each pair of bad predictions of network
    """
    # CreatureNN = CNN((17, 9, 3), "./model/creatures/", 167)
    # CreatureNN.load_model()
    # CreatureNN.add_test_images('../ds_test/')
    # CreatureNN = DumbNN((38, 36, 1), "./model/queue/", 166)
    # CreatureNN.load_model()
    # CreatureNN.add_test_images('../queue_test/')
    CreatureNN = CNN((17, 9, 3), "./model/battle1/", 2)
    CreatureNN.load_model()
    CreatureNN.add_test_images('../battle1_test/')

    inv_map = {v: k for k, v in CreatureNN.dictionary.items()}
    data = list()
    for i in range(154):
        data.append(CreatureNN.test_images[i])
    data = np.array(data)
    result = CreatureNN.model.predict(data)
    result2 = []
    for i in range(154):
        result2.append(np.where(result[i] == np.amax(result[i])))
    result3 = []
    for i in range(154):
        x = result2[i]
        result3.append(int(x[0]))
    result2 = [*map(inv_map.get, result3)]
    real = [*map(inv_map.get, CreatureNN.test_labels)]
    errors = [[], []]
    for i in range(154):
        if result2[i] != real[i]:
            errors[0].append(result2[i])
            errors[1].append(real[i])
    a = np.array(errors)
    return a


def train_map_NN():
    """
    helper function for creating and training of specyfic neural network
    """
    mapNN = CNN((11,11,3),"./model/map/", 519)
    mapNN.add_learning_images('../structures/')
    mapNN.add_test_images('../structures_test/')
    mapNN.train_network()


def try_map_NN():
    """
    helper function for loading and testing of specyfic neural network
    """
    mapNN = CNN((11,11,3),"./model/map/", 519)
    mapNN.load_model()
    mapNN.add_test_images('../structures_test/')
    mapNN.test_network()

def train_battle1_NN():
    """
    helper function for creating and training of specyfic neural network
    """
    CreatureNN = CNN((17,9,3),"./model/battle1/", 2)
    CreatureNN.add_learning_images('../battle1/')
    CreatureNN.add_test_images('../battle1_test/')
    CreatureNN.train_network()

def train_spells_NN():
    """
    helper function for creating and training of specyfic neural network
    """
    CreatureNN = DumbNN((35, 47, 1), "image_processing/model/spells/", 79)
    CreatureNN.add_learning_images('./spells/')
    CreatureNN.add_test_images('./spells_test/')
    CreatureNN.train_network()

def try_spells_NN():
    """
    helper function for loading and testing of specyfic neural network
    """
    CreatureNN = DumbNN((35, 47, 1), "image_processing/model/spells/", 79)
    CreatureNN.load_model()
    CreatureNN.add_test_images('./spells_test/')
    CreatureNN.test_network()

def try_battle1_NN():
    """
    helper function for loading and testing of specyfic neural network
    """
    CreatureNN = CNN((17,9,3),"./model/battle1/", 3)
    CreatureNN.load_model()
    CreatureNN.add_test_images('../battle1_test/')
    CreatureNN.test_network()

# train_creatures_NN()
# train_map_NN()
# test = abomination()
# print(1)
# for dirname in os.listdir("../ds/"):
#     for filename in os.listdir(os.path.join("../ds/", dirname)):
#         img = cv2.imread(os.path.join("../ds/", dirname, filename))
#         if img is not None:
#             cv2.imwrite(os.path.join("../battle1/creature/", filename),img)
# train_battle1_NN()
# a = abomination()
# print(1)

#train_spells_NN()