import numpy as np
from scipy import linalg
#otrzymane równania to:
#   Ws+Qa*ca-Qa*c1+E12(c2-c1) = 0
#   Qb*cb+E12(c1-c2)+E23(c3-c2)-Qb*c2+Qa*c1-Qa*c2 = 0
#   (Qa+Qb)*c2-(Qd+Qc)*c3+E23*(c2-c3)+E34(c4-c3)+E35(c5-c3) = 0
#   Qc*c3-Qc*c4+E34(c3-c4) = 0
#   Qd*c3-Qd*c5+wg+E35(c3-c5) = 0

#dane wejsciowe
Wg = 2500.
Ws = 1500.
Qa = 200.
ca =2.
Qb = 300.
cb = 2.
Qc = 150.
Qd= 350.
E12 = 25.
E23 = 50.
E34 = 50.
E35 = 25.
#funkcja potrzebna do obracania macierzy A
def wyznacz_wiersz_AinvT(L_inv, U_inv, b):
    bt=b.T
    d =L_inv@bt
    x = U_inv@d
    return x.flatten()
#wyznaczanie macierzy C - stężenie CO w poszczególnych pokojach
def stezenie_CO(Wg,Ws, Qa, ca, Qb, cb, A_inv):
    print("\nWyniki dla wartości Wg =",Wg, "Ws =", Ws)
    B_poziome = np.array([-Ws - Qa * ca, -Qb * cb, 0, 0, -Wg])[np.newaxis]
    B = B_poziome.T
    print("Macierz B:\n", B)
    # wyznaczenie wektora c
    C = A_inv @ B
    print("Stężenie CO  w poszczególnych pomieszczeniach [mg/m3]:\n", C.flatten())
    return C.flatten()

#tworzenie macierzy A i B
A = np.array(  [[-Qa-E12, +E12, 0, 0, 0],
                [+E12+Qa, -E12-E23-Qb-Qa, E23, 0, 0],
                [0, Qa+Qb+E23, -Qd-Qc-E23-E34-E35, E34, E35],
                [0,0,Qc+E34, -Qc-E34, 0],
                [0,0, Qd+E35, 0, -Qd-E35]])
print("\nMacierz A:\n", A)

#rozkład LU
P, L, U = linalg.lu(A)
print ("\nMacierz L:\n",L)
print ("\nMacierz U:\n",U)
L_inv = linalg.inv(L)
U_inv = linalg.inv(U)

#wyznaczenie macierzy A.inv
b1=np.array([1, 0, 0, 0, 0])[np.newaxis]
b2=np.array([0, 1, 0, 0, 0])[np.newaxis]
b3=np.array([0, 0, 1, 0, 0])[np.newaxis]
b4=np.array([0, 0, 0, 1, 0])[np.newaxis]
b5=np.array([0, 0, 0, 0, 1])[np.newaxis]
a1=wyznacz_wiersz_AinvT(L_inv, U_inv, b1)
a2=wyznacz_wiersz_AinvT(L_inv, U_inv, b2)
a3=wyznacz_wiersz_AinvT(L_inv, U_inv, b3)
a4=wyznacz_wiersz_AinvT(L_inv, U_inv, b4)
a5=wyznacz_wiersz_AinvT(L_inv, U_inv, b5)
A_inv=np.round(np.array([a1,a2,a3,a4,a5]).T, decimals =8)
print("\nOdwrotnosc macierzy A:\n", A_inv)

#wyznaczenie CO
C=stezenie_CO(Wg,Ws,Qa, ca, Qb,cb,A_inv)
C1=stezenie_CO(1200.,800.,Qa, ca, Qb,cb,A_inv)
print("\nStężenie CO w pomieszczeniach zmieniło się następująco (C-C1) [mg/m3]:\n", C-C1)

# wpływ procentowy na pokój dla dzieci
stezenie_dzieci = C[3]
# grilla
dd=np.abs(A_inv[3][4])
grill = np.round(np.absolute(A_inv[3][4]) *Wg/ stezenie_dzieci * 100, decimals=3)
# palaczy
palacze = np.round(np.absolute(A_inv[3][0]) * Ws / stezenie_dzieci * 100, decimals=3)
# ulicy
ulica = np.round((np.absolute(A_inv[3][0]) * Qa * ca + np.abs(A_inv[3][1]) * Qb * cb) / stezenie_dzieci * 100, decimals=3)
print("\nWpływ procentowy CO na pokój dla dzieci pochodzący od:\n"
      "- grilla: ", grill, "%\n"
      "- palaczy: ", palacze, "%\n"
      "- ulicy: ", ulica, "%\n"
      "dla Wg =",Wg," i Ws =",Ws)