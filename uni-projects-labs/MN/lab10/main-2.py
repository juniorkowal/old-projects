import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def analitycznie():
    # dy/dt = y(1-y)t
    # dy(1/y)-dy(1/y-1) = tdt
    # ln|y| - ln|y-1| +C = t^2/2
    # |y/y-1| *C = e ^(t^2/2)
    # C*y = (y-1)*e ^(t^2/2)
    # y(C-e ^(t^2/2)) = -e ^(t^2/2)
    # y = -e ^(t^2/2) / (C-e ^(t^2/2))
    # # z war pocz
    # y(0)=1/2
    # -1/(C-1) = 1/2
    # -2 = C-1
    # -1 = C
    # y = (e ^(t^2/2))/( e ^(t^2/2)+1)
    y_a = np.exp(np.power(t_range, 2)/2)/(np.exp(np.power(t_range, 2)/2)+1)
    return y_a

def Euler():
    y_e=np.zeros(n)
    y_e[0] = 1/2
    for i in range (n-1):
        dy_dt = y_e[i]*(1-y_e[i])*t_range[i]
        y_e[i+1]=y_e[i] + dy_dt *h
    return y_e

def Heun():
    y_h=np.zeros(n)
    y_h[0] = 1/2
    for i in range (n-1):
        dy_dt = y_h[i]*(1-y_h[i])*t_range[i]
        y_h[i+1]=y_h[i] + dy_dt *h
        dy_dt_1 = y_h[i+1]*(1-y_h[i+1])*t_range[i+1]
        y_h[i+1]=y_h[i] + (dy_dt+dy_dt_1)/2 *h
    return y_h

def pkt_sr():
    y_p=np.zeros(n)
    y_p[0] = 1/2
    for i in range (n-1):
        dy_dt = y_p[i]*(1-y_p[i])*t_range[i]
        y_1_2=y_p[i] + dy_dt *h/2
        dy_dt_1 = y_1_2 * (1 - y_1_2) * (t_range[i]+t_range[i+1])/2
        y_p[i + 1] = y_p[i] +  dy_dt_1 * h
    return y_p

if __name__ == '__main__':
    # -----------------
    t0, tk = 0, 10
    n = int(input("Podaj na ile części podzielić przedział od t=0 do t=10 (preferowane 100): "))
    #n = 100
    h = tk / n  # krok
    # -----------------
    t_range = np.linspace(t0, tk, n)        # zbior t
    y_analitycznie = analitycznie()
    y_euler = Euler()
    y_heun = Heun()
    y_pkt_sr = pkt_sr()

    gs = gridspec.GridSpec(3,1)
    fig = plt.figure()
    fig.set_size_inches(10.5, 7.5, forward=True)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t_range, y_analitycznie,'m', label='Analitycznie')
    ax1.plot(t_range, y_euler, 'g',label='Metoda Eulera')
    ax1.plot(t_range, y_heun, 'b', label='Metoda Heuna (bez iteracji)')
    ax1.plot(t_range, y_pkt_sr, 'r', label='Metoda punktu srodkowego')
    ax1.set_xlabel('t', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)

    ''' !!!  '''
    '''Poniższe wykresy dostosowane dla n =100'''
    ax2 = fig.add_subplot(gs[2, 0])
    ax2.set_xlim(3.45, 3.7)
    ax2.set_ylim(0.9975, 0.99950)
    ax2.plot(t_range, y_analitycznie, 'm')
    ax2.plot(t_range, y_euler, 'g')
    ax2.plot(t_range, y_heun, 'b')
    ax2.plot(t_range, y_pkt_sr, 'r')
    ax2.set_xlabel('t', fontsize=12)
    ax2.set_ylabel('y', fontsize=12)

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_xlim(0.9, 1.1)
    ax3.set_ylim(0.6, 0.625)
    ax3.plot(t_range, y_analitycznie)
    ax3.plot(t_range, y_euler)
    ax3.plot(t_range, y_heun)
    ax3.plot(t_range, y_pkt_sr)
    ax3.set_xlabel('t', fontsize=14)
    ax3.set_ylabel('y', fontsize=14)

    fig.legend(loc='upper left', mode='expand', ncol=4)
    fig.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()

