import cv2
import numpy as np
import matplotlib.pyplot as plt


#Program na początku dokonuje prostych operacji typu odejmowanie od siebie dwóch obrazów, zwiększanie kontrastu, konwersja na binarne,
#redukcja szumu. Z tego otrzymujemy maskę dla wyciętych kevinów, z maski wyciągamy kontury i ich współrzędne do otoczenia kevinów bounding
#boxami, które są zapisywane do listy. Następnie są tworzone maski dla wycinania bounding boxów za pomocą wstawiania zer i jedynek według
#współrzędnych za pomocą numpy. Nie byłem pewny w jaki sposób je wyciąć, dlatego wyciąłem je na dwa sposoby. Na koniec wyświetlam wszystkie
#obrazy w jednym fig za pomocą subplotów dla estetyki.

def podstawowe_operacje(kevin, no_kevin):
    roznica = cv2.absdiff(kevin,no_kevin)
    kontrast = cv2.convertScaleAbs(roznica, alpha=5, beta=0)
    kontrast_szary = cv2.cvtColor(kontrast, cv2.COLOR_BGR2GRAY)
    _,binarny = cv2.threshold(kontrast_szary,50,255,cv2.THRESH_BINARY)
    szum_redukcja = cv2.morphologyEx(binarny, cv2.MORPH_OPEN, kernel(2))
    zamkniecie = cv2.morphologyEx(szum_redukcja, cv2.MORPH_CLOSE, kernel(6))
    wyciete_keviny = cv2.bitwise_and(kevin,kevin,mask = zamkniecie)
    return wyciete_keviny, zamkniecie

def kernel(liczba):
    kernel_zmienny = np.ones((liczba,liczba),np.uint8)
    return kernel_zmienny

def prostokaty(bw_maska, kevin_boxy, kevin_org):
    kontury,_ = cv2.findContours(bw_maska, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maska = np.zeros_like(kevin_boxy, np.uint8)
    lista_wspolrzednych=[]

    for kontur in kontury:
        (x,y,w,h) = cv2.boundingRect(kontur)
        cv2.rectangle(kevin_boxy, (x,y), (x+w,y+h), (0,255,0), 2)
        wsp=(x,y,w,h)
        lista_wspolrzednych.append(wsp)

    for wsp in lista_wspolrzednych:
        maska[wsp[1]:wsp[1]+wsp[3], wsp[0]:wsp[0]+wsp[2]] = np.ones((wsp[3],wsp[2],3),np.uint8)

    maska*=255
    maska = cv2.cvtColor(maska, cv2.COLOR_BGR2GRAY)
    maska_inv =cv2.bitwise_not(maska)
    wyciete_boxy = cv2.bitwise_and(kevin_org,kevin_org,mask = maska)
    wyciete_boxy_inv = cv2.bitwise_and(kevin_org,kevin_org,mask = maska_inv)
    return wyciete_boxy, wyciete_boxy_inv, kevin_boxy

dublin = cv2.imread('dublin.jpg')
dublin_ed = cv2.imread('dublin_edited.jpg')
dublin_ed_copy = dublin_ed.copy()

bez_tla, binarna_maska = podstawowe_operacje(dublin_ed, dublin)
wyciecie_1, wyciecie_2, bounding_boxy = prostokaty(binarna_maska, dublin_ed, dublin_ed_copy)

fig = plt.figure(figsize=(15, 10))

wiersze = 2
kolumny = 2

fig.add_subplot(wiersze, kolumny, 1)
plt.imshow(cv2.cvtColor(bounding_boxy,cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title("1. Otoczenie obiektu bounding boxem")
  
fig.add_subplot(wiersze, kolumny, 2)
plt.imshow(cv2.cvtColor(wyciecie_1,cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title("2. Wyciecie bounding boxow")
  
fig.add_subplot(wiersze, kolumny, 3)
plt.imshow(cv2.cvtColor(wyciecie_2,cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title("3. Rowniez wyciecie bounding boxow, ale w inny sposob")
  
fig.add_subplot(wiersze, kolumny, 4)
plt.imshow(cv2.cvtColor(bez_tla,cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title("4. Obiekty bez tla")
plt.subplots_adjust(0,0,1,0.96,0,0.09)

plt.show()