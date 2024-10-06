import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.optimize


# ------ odp. skokowa i impulsowa ukladu 2 rzedu przy zalozeniu ze: 0 < zeta < 1 -----
def step(t, tau, zeta):
    return (1 - np.exp(-zeta * t / tau) / (np.sqrt(1 - zeta ** 2)) * np.sin(
        t * np.sqrt(1 - zeta * 2) / tau + math.acos(zeta)))     # theta = math.acos(zeta)


def impulse(t, tau, zeta):
    return (np.exp(-zeta * t / tau) / (tau * np.sqrt(1 - zeta ** 2)) * np.sin(
        t * np.sqrt(1 - zeta ** 2) / tau))
# ------------------------------------------------------------------------------------


# ------------------ odp. skokowa wynikowego ukladu ----------------------------------
def new_step(t, k, tau_z, tau, zeta):
    return k * (tau_z * impulse(t, tau, zeta) + step(t, tau, zeta))


# ================== KRYTERIUM NAJMNIEJSZYCH KWADRATOW ========================
# ----------- funkcja zwracajaca sume do minimalizacji dla fmin ---------------
def least_squares(param_opt):
    t = x
    add = 0
    new_y = new_step(t, param_opt[0], param_opt[1], param_opt[2], param_opt[3])
    for i in range(len(t)):
        add = add + np.power(y[i] - new_y[i], 2)
    return add
# =============================================================================


path = r'E:\AiR_semestr 6\Numeryczne_lab\lab_6_dane\data3.txt'
with open(path) as f:
    lines = f.readlines()
    x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]

x = np.array(x, dtype=np.float32)
y = np.array(y, dtype=np.float32)

# ------------- poszukiwanie minimum dla kryterium najmn. kwadratow ------------------------
k_opt, tau_z_opt, tau_opt, zeta_opt = scipy.optimize.fmin(least_squares, [0.1, 0.1, 0.1, 0.1])
# ------------------------------------------------------------------------------------------
opt_y = new_step(x, k_opt, tau_z_opt, tau_opt, zeta_opt)    # wartosci y nowej odp. skokowej
# ------------------------------------------------------------------------------------------
fig, ax = plt.subplots()
plt.xlim(np.min(x), np.max(x))
fig.set_size_inches(10.5, 7.5, forward=True)
fig.canvas.set_window_title('Metody numeryczne - lab. 6')
fig.suptitle('Wykresy odpowiedzi skokowych', fontsize=14)
ax.title.set_text(r'zidentyfikowane parametry: $\kappa$ = {}  $\tau_{}$ = {}  $\tau$ = {}  $\zeta$ = {}'.format(
    "%.6f" % k_opt, 'z', "%.6f" % tau_z_opt, "%.6f" % tau_opt, "%.6f" % zeta_opt))
ax.plot(x, y,  label='odp. skokowa z danych z pliku')
ax.plot(x, opt_y, label='odp. skokowa dla zidentyfikowanej transmitancji')
ax.set_yticks([0.0], minor=True)
ax.yaxis.grid(True, which='minor')
ax.set_xlabel('t', fontsize=14)
ax.set_ylabel('y(t)', fontsize=14)
ax.legend(loc="lower right", fontsize=12)
plt.show()
