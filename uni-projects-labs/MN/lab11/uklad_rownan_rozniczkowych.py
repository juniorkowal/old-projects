import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np


def f(v, x, y, z):
    if v == 0:
        return -10 * x + 10 * y
    elif v == 1:
        return 28 * x - y - x * z
    elif v == 2:
        return -8 / 3 * z + x * y


def algorithm(steps):
    x, y, z = np.zeros(steps, dtype=float), np.zeros(steps, dtype=float), np.zeros(steps, dtype=float)
    x[0], y[0], z[0] = 5, 5, 5

    for i in range(steps - 1):
        k1_x = f(0, x[i], y[i], z[i])
        k1_y = f(1, x[i], y[i], z[i])
        k1_z = f(2, x[i], y[i], z[i])
        k2_x = f(0, x[i] + k1_x * h / 2, y[i] + k1_y * h / 2, z[i] + k1_z * h / 2)
        k2_y = f(1, x[i] + k1_x * h / 2, y[i] + k1_y * h / 2, z[i] + k1_z * h / 2)
        k2_z = f(2, x[i] + k1_x * h / 2, y[i] + k1_y * h / 2, z[i] + k1_z * h / 2)
        k3_x = f(0, x[i] + k2_x * h / 2, y[i] + k2_y * h / 2, z[i] + k2_z * h / 2)
        k3_y = f(1, x[i] + k2_x * h / 2, y[i] + k2_y * h / 2, z[i] + k2_z * h / 2)
        k3_z = f(2, x[i] + k2_x * h / 2, y[i] + k2_y * h / 2, z[i] + k2_z * h / 2)
        k4_x = f(0, x[i] + k3_x * h, y[i] + k3_y * h, z[i] + k3_z * h)
        k4_y = f(1, x[i] + k3_x * h, y[i] + k3_y * h, z[i] + k3_z * h)
        k4_z = f(2, x[i] + k3_x * h, y[i] + k3_y * h, z[i] + k3_z * h)
        x[i + 1] = x[i] + (k1_x + 2 * k2_x + 2 * k3_x + k4_x) * h / 6
        y[i + 1] = y[i] + (k1_y + 2 * k2_y + 2 * k3_y + k4_y) * h / 6
        z[i + 1] = z[i] + (k1_z + 2 * k2_z + 2 * k3_z + k4_z) * h / 6
    return x, y, z


if __name__ == "__main__":
    t_0 = 0
    t_k = 25
    h = 0.03125
    n_steps = int(t_k / h)
    t = np.linspace(t_0, t_k, n_steps)
    x, y, z = algorithm(n_steps)

    g = gridspec.GridSpec(2, 2)
    fig = plt.figure('Układy równań różniczkowych')

    ax = fig.add_subplot(g[0, 0])
    ax.title.set_text("Zmienna x")
    ax.plot(t, x, 'cyan')
    ax.set_xlabel('t')
    ax.set_ylabel('x')

    ax2 = fig.add_subplot(g[0, 1])
    ax2.title.set_text("Zmienna y")
    ax2.plot(t, y, 'magenta')
    ax2.set_xlabel('t')
    ax2.set_ylabel('y')

    ax3 = fig.add_subplot(g[1, 0])
    ax3.title.set_text("Zmienna z")
    ax3.plot(t, z, 'violet')
    ax3.set_xlabel('t')
    ax3.set_ylabel('z')

    ax4 = fig.add_subplot(g[1, 1], projection='3d')
    ax4.title.set_text("Trajektoria fazowa")
    ax4.plot3D(x, y, z, '')
    ax4.set_xlabel('x')
    ax4.set_ylabel('y')
    ax4.set_zlabel('z')

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
