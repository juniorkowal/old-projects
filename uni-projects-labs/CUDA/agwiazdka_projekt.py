import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue
import timeit
import matplotlib.animation as animation
from numba import cuda,int64

ILE=6

def plansza():
    wartosci_kolorow = np.random.choice([1, 0], size=(ILE, ILE), p=[0.8, 0.2])
    wartosci_kolorow[0, 0] = 1
    wartosci_kolorow[ILE-1, ILE-1] = 1
    return wartosci_kolorow


def h(komorka1,komorka2):
    x1,y1=komorka1
    x2,y2=komorka2
    return abs(x1-x2) + abs(y1-y2)


def sasiad(aktualna_komorka,koszt_g,koszt_f,open,ag_droga,d1,d2):
    potomek=(aktualna_komorka[0]+d1,aktualna_komorka[1]+d2)
    temp_koszt_g=koszt_g[aktualna_komorka[0]][aktualna_komorka[1]]+1
    temp_koszt_f=temp_koszt_g+h(potomek,(0,0))

    if temp_koszt_f < koszt_f[potomek[0]][potomek[1]]:
        koszt_g[potomek[0]][potomek[1]]= temp_koszt_g
        koszt_f[potomek[0]][potomek[1]]= temp_koszt_f
        open.put((temp_koszt_f,h(potomek,(0,0)),potomek))
        ag_droga[potomek]=aktualna_komorka


def agwiazdka(kolory):

    start=(ILE-1,ILE-1)

    koszt_g=np.full_like(kolory,214748364)
    koszt_g=koszt_g.tolist()


    koszt_g[start[0]][start[1]]=0

    koszt_f=np.full_like(kolory,214748364)
    koszt_f=koszt_f.tolist()


    koszt_f[start[0]][start[1]]=h(start,(0,0))

    open=PriorityQueue()
    open.put((h(start,(0,0)),h(start,(0,0)),start))

    ag_droga={}

    while not open.empty():
        aktualna_komorka=open.get()[2]

        if aktualna_komorka==(0,0):
            break

        if aktualna_komorka[1]>=1:

            if kolory[aktualna_komorka[0]][aktualna_komorka[1]-1]==1: #W
                sasiad(aktualna_komorka,koszt_g,koszt_f,open,ag_droga,d1=0,d2=-1)

        if aktualna_komorka[1]<=(ILE-2):
            if kolory[aktualna_komorka[0]][aktualna_komorka[1]+1]==1: #E
                sasiad(aktualna_komorka,koszt_g,koszt_f,open,ag_droga,d1=0,d2=1)

        if aktualna_komorka[0]<=(ILE-2):
            if kolory[aktualna_komorka[0]+1][aktualna_komorka[1]]==1: #S
                sasiad(aktualna_komorka,koszt_g,koszt_f,open,ag_droga,d1=1,d2=0)

        if aktualna_komorka[0]>=1:
            if kolory[aktualna_komorka[0]-1][aktualna_komorka[1]]==1: #N
                sasiad(aktualna_komorka,koszt_g,koszt_f,open,ag_droga,d1=-1,d2=0)

    droga_odwrocona={}
    cell=(0,0)
    try:
        while cell!=start:
            droga_odwrocona[ag_droga[cell]]=cell
            cell=ag_droga[cell]
    except:
        print('nie znaleziono drogi')
    droga_odwrocona = {y:x for x,y in droga_odwrocona.items()}
    data = list(droga_odwrocona.items())
    an_array = np.array(data)
    an_array=np.reshape(an_array,(an_array.shape[0]*2,2))
    an_array=np.unique(an_array,axis=0)
    an_array=an_array.tolist()

    return an_array

def update(i):
    kolory[droga_cpu[i][0]][droga_cpu[i][1]]=2
    im.set_data(kolory)

kolory = plansza()
kolory_gpu=kolory.copy()
kolory=kolory.tolist()

start_cpu = timeit.default_timer()
droga_cpu=agwiazdka(kolory)
stop_cpu = timeit.default_timer()

czas_cpu=stop_cpu-start_cpu
print(czas_cpu)

kolory_gpu=kolory_gpu.flatten()
wyjscie=np.empty_like(kolory_gpu)

#print(kolory)
#print(kolory_gpu)

kolory_gpu=cuda.to_device(kolory_gpu)
wyjscie=cuda.to_device(wyjscie)

@cuda.jit
def agwiazdka_gpu(grid,dim,k,result):

    tx = cuda.threadIdx.x

    poprzedni_punkt=cuda.shared.array(shape=(36),dtype=int64)
    najnizszy_koszt=cuda.shared.array(shape=(36),dtype=int64)
    array=cuda.shared.array(shape=(30),dtype=int64)
    heuristics=cuda.shared.array(shape=(30),dtype=int64)
    sizes=cuda.shared.array(shape=(5),dtype=int64)
    flag=cuda.shared.array(shape=(1),dtype=int64)
    odkryte_pkt=cuda.shared.array(shape=(20),dtype=int64)

    flag=0
    najnizszy_koszt[(dim*dim)-1]=0
    poprzedni_punkt[(dim*dim)-1]=-5

    if tx==0:
        for i in range(dim*k):
            array[i]=-1
        for i in range(dim*dim):
            najnizszy_koszt[i]=2136
        for i in range(k):
            sizes[i]=0
        for i in range(4*k):
            odkryte_pkt[i]=-1

    cuda.syncthreads()

    array[0]=0
    sizes[0]=1
    najnizszy_koszt[0]=0

    while(czypustakolejka(array,dim,k)!=0):
        cuda.syncthreads()
        if flag==1:
            break
        
        if array[dim*tx]!=-1:
            extracted=array[dim*tx]
            zmianakolejki(array,dim,tx)
            sizes[tx]-=1

            if extracted==((dim*dim)-1) or flag==1:
                flag=1
                continue

            top=extracted-dim
            bottom=extracted+dim
            left=extracted-1
            right=extracted+1

            if (extracted%dim)==0:
                left=-1
            if extracted%dim==dim-1:
                right=-1

            odkryte_pkt[tx*4+0]=top
            odkryte_pkt[tx*4+1]=bottom
            odkryte_pkt[tx*4+2]=left
            odkryte_pkt[tx*4+3]=right

            for i in range(4):
                aktualny_numer=odkryte_pkt[tx*4+i]

                if(aktualny_numer<0 or aktualny_numer>dim*dim or grid[aktualny_numer]==0 or najnizszy_koszt[extracted]+1>najnizszy_koszt[aktualny_numer]):
                    odkryte_pkt[tx*4+i]=-1
                    continue

                if(odkryte_pkt[tx*4+i]!=-1):
                    najnizszy_koszt[aktualny_numer]=najnizszy_koszt[extracted]+1
                    poprzedni_punkt[aktualny_numer]=extracted

            for i in range(4):
                r=duplikaty(odkryte_pkt,odkryte_pkt[tx*4+i],k,tx*4+i)
                if r!=-1:
                    cuda.atomic.exch(odkryte_pkt,r,-1)
                if(odkryte_pkt[tx*4+i]!=-1):
                    h=najnizszy_koszt[odkryte_pkt[tx*4+i]]+heuristic(dim,odkryte_pkt[tx*4+i],(dim*dim)-1)
                    check=0
                    # while(check==0):
                    #     targetLocation=znajdznastepnypunkt(sizes,k)
                    #     if(cuda.atomic.compare_and_swap(array[targetLocation*dim+sizes[targetLocation]],-1,odkryte_pkt[tx*4+i])==-1):
                    #         heuristics[targetLocation*dim+sizes[targetLocation]]=h
                    #         sizes[targetLocation]+=1
                    #         ustawkolejke(array,targetLocation,heuristics,h,sizes[targetLocation],dim)
                    #         check=1

    if tx==0:
        aktualny=dim*dim-1
        while(aktualny!=0):
            if poprzedni_punkt[aktualny]==-5:
                break
            grid[aktualny]=-1
            aktualny=poprzedni_punkt[aktualny]
            if aktualny==0:
                grid[aktualny]=-1
            else:
                print('brak drogi')
n=1
m=1
@cuda.jit(device=True)
def ustawkolejke(queue,targetLocation,heuristics,h,which,dim):
    for i in range(which-1,0,-1):
        if i<0:
            break
        if heuristics[dim*targetLocation+i]>h:
            temp1=heuristics[dim*targetLocation+i]
            temp2=queue[dim*targetLocation+i]
            heuristics[dim*targetLocation+i]=h
            queue[dim*targetLocation+i]=queue[dim*targetLocation+which]
            queue[dim*targetLocation+which]=temp2
            heuristics[dim*targetLocation+which]=temp1
            which-=1

@cuda.jit(device=True)
def duplikaty(adjacents,a,k,obecna_pozycja):
    for i in range(4*k):
        if adjacents[i]==a and i !=obecna_pozycja:
            return i
    return -1

@cuda.jit(device=True)
def znajdznastepnypunkt(sizes,k):
    smallestQueue=-100
    cursmallest=5000
    for i in range(k):
        if sizes[i]<cursmallest:
            smallestQueue=i
            cursmallest=sizes[i]
    return smallestQueue

@cuda.jit(device=True)
def heuristic(dim,aktualny,end):
    curX=aktualny%dim
    curY=aktualny/dim
    endX=end%dim
    endY=end/dim
    return int(abs(curX-endX)+abs(curY-endY))

@cuda.jit(device=True)
def zmianakolejki(array_sh,dim,k):
    for i in range(dim):
        if i==dim-1:
            array_sh[dim*k+i]=-1
        else:
            array_sh[dim*k+i]=array_sh[dim*k+i+1]

@cuda.jit(device=True)
def czypustakolejka(array_sh,dim,k):
    check=0
    for i in range(k):
        if array_sh[dim*i]!=-1:
            check=1
            break
    return check


j=np.zeros(shape=(5),dtype=int)
#print(j)

z=timeit.default_timer()
agwiazdka_gpu[1*n,5*m](kolory_gpu,ILE,5,wyjscie)
j=timeit.default_timer()
print('CZAS GPU: '+str(j-z))
wyjscie=wyjscie.copy_to_host()
#print(wyjscie)
kolory_gpu=kolory_gpu.copy_to_host()
#print(kolory_gpu)
cuda.synchronize()



cmap = colors.ListedColormap(["black", "white", "blue"])
boundaries = [0,1,2,3]
norm = colors.BoundaryNorm(boundaries, cmap.N, clip=True)
mpl.rcParams['toolbar'] = 'None'

fig = plt.figure()
im=plt.imshow(kolory,interpolation="nearest",origin="upper", cmap=cmap, norm=norm)

ani = animation.FuncAnimation(fig, func=update, frames=len(droga_cpu), repeat=False,interval=czas_cpu/len(droga_cpu))

plt.show()