import os
import matplotlib.pyplot as plt
import numpy as np


def predykcja(it):
    T = 1
    F = np.array([[1, 0, T, 0], [0, 1, 0, T], [0, 0, 1, 0], [0, 0, 0, 1]])
    predicted_s = [[predicted_x[- 1]], [predicted_y[- 1]], [trajectory[0][2][-1]], [trajectory[0][3][-1]]]
    predicted = []
    for i in range(it):
        predicted.append(np.matmul(F, predicted_s))
        predicted_s = predicted[i]
    predicted = np.transpose(predicted)
    p_x = predicted[0][0][:]
    p_y = predicted[0][1][:]
    p_x, p_y = np.insert(p_x, 0, predicted_x[-1]), np.insert(p_y, 0, predicted_y[-1])
    return p_x, p_y


def filtr_kalmana(x0, y0, t):
    T = 1
    F = np.array([[1, 0, T, 0], [0, 1, 0, T], [0, 0, 1, 0], [0, 0, 0, 1]])
    G = np.array([[0, 0], [0, 0], [1, 0], [0, 1]])
    H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
    Q = np.array([[0.25, 0], [0, 0.25]])
    R = np.array([[2.0, 0], [0, 2.0]])

    s = np.array([[x0[0]], [y0[0]], [0], [0]])
    s_predicted = []
    s_n1_n = np.matmul(F, s)
    p_n1_n1 = np.array([[5, 0, 0, 0],[0, 5, 0, 0],[0, 0, 5, 0],[0, 0, 0, 5]])

    for i in range(t):
        p_n1_n = np.matmul(np.matmul(F, p_n1_n1), np.transpose(F)) + np.matmul(np.matmul(G, Q), np.transpose(G))
        z_n1_n = np.matmul(H, s_n1_n)
        e_n1 = np.transpose(np.atleast_2d([x0[i + 1], y0[i + 1]])) - z_n1_n
        s_n_n = np.matmul(np.matmul(H, p_n1_n), np.transpose(H)) + R
        k_n1 = np.matmul(np.matmul(p_n1_n, np.transpose(H)), np.linalg.inv(s_n_n))
        s_predicted.append(s_n1_n + np.matmul(k_n1, e_n1))
        p_n1_n1 = np.matmul((np.identity(len(np.matmul(k_n1, H))) - np.matmul(k_n1, H)), p_n1_n)
        s_n1_n = np.matmul(F, s_predicted[i])
    return s_predicted


if __name__ == '__main__':
    with open('measurements9.txt') as f:
        lines = f.readlines()
        x = [line.split()[0] for line in lines]
        y = [line.split()[1] for line in lines]
    x = np.array(x, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    trajectory = filtr_kalmana(x, y, (len(x) - 1))
    trajectory = np.transpose(trajectory)
    predicted_x = trajectory[0][0][:]
    predicted_y = trajectory[0][1][:]
    predicted_x, predicted_y = np.insert(predicted_x, 0, x[0]), np.insert(predicted_y, 0, y[0])
    pre_trajectory_x, pre_trajectory_y = predykcja(5)

    fig, ax = plt.subplots()
    ax.set_xlabel('Współrzedna x')
    ax.set_ylabel('Współrzedna y')
    ax.plot(predicted_x, predicted_y, 'black', label='Wyznaczona trajektoria')
    ax.plot(x, y, 'bx', label='Zmierzona trajektoria')
    ax.plot(pre_trajectory_x, pre_trajectory_y, 'r--', label='Przewidziana trajektoria')
    ax.plot(pre_trajectory_x[- 1], pre_trajectory_y[- 1], 'ro')
    ax.legend(loc="upper right")
    plt.show()
