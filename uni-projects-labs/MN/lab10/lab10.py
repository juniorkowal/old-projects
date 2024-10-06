import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# rownanie rozniczkowe nr 3
def analytical():
    # met. zmiennych rozdzielonych
    # dy/dt = -2/3 * y * t + 3 * y, y(0) = 2
    # dy = (-2/3 * y * t + 3 * y) dt
    # dy/y = (-2/3 * t + 3) dt  y != 0
    # integral (1/y) dy = integral (-2/3 *  t + 3) dt
    # ln|y| = -1/3 * t^2 + 3 * t + C1
    # ln|y| = ln(e^(-1/3 * t^2)) + ln(e(^3 * t)) + ln(C1)
    # ln|y| = ln(C1 * e^(-1/3 * t^2) * e(^3 * t))
    # y = C * e^(-1/3 * t^2 + 3 * t)
    # podstawienie y(0) = 2 daje stala C = 2
    # rozwiazanie: y = 2 * e^(-1/3 * t^2 + 3 * t)
    y = 2 * np.exp(-1/3 * np.power(t_range, 2) + 3 * t_range)
    return y


def euler():
    y = [2]
    for i in range(1, n):
        y.append(y[i - 1] + function(t_range[i - 1], y[i - 1]) * h)
    return y


def heun():
    y = [2]
    for i in range(1, n):
        slope = y[i - 1] + function(t_range[i - 1], y[i - 1]) * h
        y.append(y[i - 1] + (function(t_range[i - 1], y[i - 1]) + function(t_range[i], slope)) / 2 * h)
    return y


def middle_point():
    y = [2]
    for i in range(1, n):
        y_half = y[i - 1] + function(t_range[i - 1], y[i - 1]) * h/2
        y_phalf = function(t_range[i - 1] + h/2, y_half)
        y.append(y[i - 1] + y_phalf * h)
    return y


def function(t, y):
    return - 2/3 * y * t + 3 * y


if __name__ == '__main__':
    # -----------------
    t0, tk = 0, 10
    n = 1000
    h = tk / n  # krok
    # -----------------
    t_range = np.linspace(t0, tk, n)
    y_analytic = analytical()
    y_euler = euler()
    y_heun = heun()
    y_middle = middle_point()

    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    fig.set_size_inches(10.5, 7.5, forward=True)
    fig.canvas.set_window_title('Metody numeryczne - lab. 10')

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t_range, y_analytic, label='Analitycznie')
    ax1.plot(t_range, y_euler, label='Metoda Eulera')
    ax1.plot(t_range, y_heun, label='Metoda Heuna (bez iteracji)')
    ax1.plot(t_range, y_middle, label='Metoda punktu srodkowego')
    ax1.set_xlabel('t', fontsize=14)
    ax1.set_ylabel('y', fontsize=14)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_xlim(3.75, 5)
    ax2.set_ylim(1500, 1720)
    ax2.plot(t_range, y_analytic)
    ax2.plot(t_range, y_euler)
    ax2.plot(t_range, y_heun)
    ax2.plot(t_range, y_middle)
    ax2.set_xlabel('t', fontsize=14)
    ax2.set_ylabel('y', fontsize=14)

    ax3 = fig.add_subplot(gs[:, 1])
    ax3.set_xlim(4.3, 4.7)
    ax3.set_ylim(1690, 1710)
    ax3.plot(t_range, y_analytic)
    ax3.plot(t_range, y_euler)
    ax3.plot(t_range, y_heun)
    ax3.plot(t_range, y_middle)
    ax3.set_xlabel('t', fontsize=14)
    ax3.set_ylabel('y', fontsize=14)

    fig.legend(loc='upper left', mode='expand', ncol=4)
    fig.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()
