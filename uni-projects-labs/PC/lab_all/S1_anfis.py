import numpy as np
import matplotlib.pyplot as plt


def get_S1(path):
    x = []
    y = []
    nr = []
    with open(path, "r", encoding='utf-8') as f:
        data = f.readlines()
    for line in data:
        words = line.split()
        x.append(int(words[0]))
        y.append(int(words[1]))
        nr.append(int(words[2]))
    return x, y, nr


dane_testowe = np.array(get_S1("./S1_anfis.txt"))
dane_testowe = dane_testowe.T

kolor = ['#a74992', '#aa99c5', '#EaE4ef', '#2d73b9', '#49bdef', '#00a9a4', '#00a54e', '#aed673', '#faf519',
                    '#f38044', '#5c3e90', '#f9c7c2', '#959595', '#000000', '#ff33cc']

for dana in dane_testowe:
    try:
        plt.plot(dana[0], dana[1], "o", color=kolor[dana[2]-1])
    except:
        pass
plt.title("ANFIS")
plt.show()
