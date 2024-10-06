from numba import cuda
import numpy as np
import matplotlib.pyplot as plt
import timeit

def generowanie_punktow(ilosc):
    losowe_pkt = np.random.uniform(0, 100000, size=(ilosc, 2))
    return losowe_pkt


def sortowanie_babelkowe_cpu(punkty):
    n = len(punkty)-1
    for i in range(n):
        for j in range(0, n-i):
            if punkty[j, 0] > punkty[j+1, 0]:
                punkty[j, 0], punkty[j+1, 0] = punkty[j+1, 0], punkty[j, 0]
                punkty[j, 1], punkty[j+1, 1] = punkty[j+1, 1], punkty[j, 1]
    return punkty


def interpolacja_cpu(punkty):
    x = []
    y = []
    for i in range(len(punkty)-1):
        x_inter = []
        for j in range(10):
            x_inter.append(punkty[i, 0]+j*((punkty[i+1, 0]-punkty[i, 0])/10))
        y_inter = punkty[i, 1]+((punkty[i+1, 1]-punkty[i, 1]) * (x_inter-punkty[i, 0]))/(punkty[i+1, 0]-punkty[i, 0])
        x.extend(x_inter)
        y.extend(y_inter)
    return x, y


def usuwanie_duplikatow_cpu(lista_x, lista_y):
    out_x = []
    out_y = []
    bufor = set()
    for i in range(len(lista_x)):
        if not lista_x[i] in bufor:
            out_x.append(lista_x[i])
            bufor.add(lista_x[i])
            out_y.append(lista_y[i])
    return out_x, out_y


def calkowanie_cpu(wsp_x, wsp_y):
    suma_calek = 0
    for i in range(len(wsp_x)-1):
        calka = (wsp_x[i+1]-wsp_x[i])*((wsp_y[i+1]+wsp_y[i])/2)
        suma_calek += calka
    return suma_calek


@cuda.jit
def sortowanie_babelkowe_gpu(pkt_x, pkt_y, petla, n):

    idx = cuda.grid(1)

    if(petla==0 and ((idx*2+1)< n)):
        if(pkt_x[idx*2]>pkt_x[idx*2+1]):
            pkt_x[idx*2+1],pkt_x[idx*2]=pkt_x[idx*2],pkt_x[idx*2+1]
            pkt_y[idx*2+1],pkt_y[idx*2]=pkt_y[idx*2],pkt_y[idx*2+1]
    
    if(petla==1 and ((idx*2+2)< n)):
        if(pkt_x[idx*2+1]>pkt_x[idx*2+2]):
            pkt_x[idx*2+2],pkt_x[idx*2+1]=pkt_x[idx*2+1],pkt_x[idx*2+2]
            pkt_y[idx*2+2],pkt_y[idx*2+1]=pkt_y[idx*2+1],pkt_y[idx*2+2]


@cuda.jit
def biedna_interpolacja(pkt_x,pkt_y,out_x,out_y):
    pos=cuda.grid(1)

    if pos < pkt_x.size:
        for i in range(10):
            out_x[i+10*pos]=(pkt_x[pos]+i*((pkt_x[pos+1]-pkt_x[pos])/10))
            out_y[i+10*pos]=pkt_y[pos]+((pkt_y[pos+1]-pkt_y[pos]) * (out_x[i+10*pos]-pkt_x[pos]))/(pkt_x[pos+1]-pkt_x[pos])


@cuda.jit
def calkowanie_gpu(pkt_x,pkt_y,wyjscie):
    pos=cuda.grid(1)
    if pos < pkt_x.size:
        wyjscie[pos]=(pkt_x[pos+1]-pkt_x[pos])*(pkt_y[pos+1]+pkt_y[pos])/2


@cuda.jit
def dodawanie_calki(calka,lista_calek):
    start=cuda.grid(1)
    stride=cuda.gridsize(1)
    for i in range(start,lista_calek.shape[0]-1,stride):
        cuda.atomic.add(calka,0,lista_calek[i])

ile=1000

xy_cpu = generowanie_punktow(ile)
xy_gpu=xy_cpu.copy()
start_cpu = timeit.default_timer()
sorted = sortowanie_babelkowe_cpu(xy_cpu)
inter_x, inter_y = interpolacja_cpu(sorted)
org_x, org_y = usuwanie_duplikatow_cpu(inter_x, inter_y)
calkowane_pole = calkowanie_cpu(org_x, org_y)
stop_cpu = timeit.default_timer()

x_gpu=xy_gpu[:,0]
y_gpu=xy_gpu[:,1]
x_gpu=x_gpu.tolist()
y_gpu=y_gpu.tolist()

puste = np.arange(10*(ile-1)).astype(np.float32)

x_out=np.empty_like(puste)
y_out=np.empty_like(puste)
lista_calek=np.empty_like(puste)

wartosc_calki_gpu=np.array([0], dtype='float32')

x_gpu=cuda.to_device(x_gpu)
y_gpu=cuda.to_device(y_gpu)
x_out=cuda.to_device(x_out)
y_out=cuda.to_device(y_out)
lista_calek=cuda.to_device(lista_calek)
wartosc_calki_gpu=cuda.to_device(wartosc_calki_gpu)

n=len(x_gpu)


for i in range(n):
    sortowanie_babelkowe_gpu[n//2,32](x_gpu,y_gpu,i%2,n)
biedna_interpolacja[n//2,32](x_gpu,y_gpu,x_out,y_out)
start_gpu = timeit.default_timer()
calkowanie_gpu[(ile//10)+1,1024](x_out,y_out,lista_calek)
dodawanie_calki[(ile//10)+1,1024](wartosc_calki_gpu,lista_calek)
stop_gpu = timeit.default_timer()

wartosc_calki_gpu=wartosc_calki_gpu.copy_to_host()

print('Calkowane pole na CPU: '+str(calkowane_pole))
print('Czas na CPU: '+str(stop_cpu-start_cpu))
print('Calkowanie pole na GPU: '+str(wartosc_calki_gpu))
print('Czas na GPU: '+str(stop_gpu-start_gpu))

# plt.plot(x_out,y_out,'+',c='red')
# plt.plot(org_x,org_y,'.',c='blue')
# # #plt.plot(xy_cpu[:,0],xy_cpu[:,1],'.',c='Red')
# plt.xlabel('Całka CPU: '+str(calkowane_pole)+' Calka GPU: '+str(wartosc_calki_gpu))
# plt.show()
