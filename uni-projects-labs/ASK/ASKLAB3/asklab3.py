import random
import sys
import unidecode
from main_window import Ui_mainWindow
from optic_window import OpticWindow
from optic2_window import OpticWindow2
from acoustic_window import AcousticWindow
from acoustic2_window import AcousticWindow2
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QElapsedTimer, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import matplotlib.pyplot as plt
import os

class OpticTest(QWidget,OpticWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.przycisk.clicked.connect(self.informacje)
        self.start.clicked.connect(self.start_testu)
        self.kolor.clicked.connect(self.reakcja)
        self.test.clicked.connect(self.testy)
        self.tryb=0
        self.time=QElapsedTimer()
        self.timer=None
        self.test.setEnabled(False)
        self.test.hide()
        self.start.setEnabled(False)
        self.start.hide()
        self.kolor.setEnabled(False)
        self.kolor.hide()

    def informacje(self):
        self.informacja.setText("")
        self.przycisk.setEnabled(False)
        self.przycisk.hide()
        self.tlo.setStyleSheet("background-color: gray;")
        self.test.setEnabled(True)
        self.test.show()
        self.start.setEnabled(True)
        self.start.show()
        self.kolor.show()
        self.typtestu.setText("Szkolenie")

    def start_testu(self):
        self.start.setEnabled(False)
        self.tlo.setStyleSheet("background-color: blue;")
        self.timer=QtCore.QTimer(self)
        self.timer.start(random.randrange(2000,10000))
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.zmiana_koloru)

    def zmiana_koloru(self):
        self.tlo.setStyleSheet("background-color: red;")
        self.kolor.setEnabled(True)
        if not self.time.isValid():
            self.time.start()

    def reakcja(self):
        self.kolor.setEnabled(False)
        interwal=self.timer.interval()
        self.tlo.setStyleSheet("background-color: blue;")
        self.timer.start(random.randrange(2000,10000))
        #self.timer.timeout.connect(self.zmiana_koloru)
        czas=self.time.restart()
        if interwal<czas:
            czas-=interwal
        self.szybkosc.setText("Twój czas reakcji wynosi: "+str(czas)+" ms")
        if self.tryb:
            with open('optic1.txt','a') as f:
                f.write(str(czas)+'\n')
                
    def testy(self):
        if self.tryb==0:
            self.typtestu.setText("Test")
            self.tryb=1
            self.test.setText("Szkolenie")
        elif self.tryb==1:
            self.typtestu.setText("Szkolenie")
            self.tryb=0
            self.test.setText("Test")

        self.tlo.setStyleSheet("background-color: gray;")
        self.szybkosc.setText("")
        if self.timer:
            self.timer.stop()
        self.time.invalidate()
        self.start.setEnabled(True)


class OpticTest2(QWidget,OpticWindow2):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.przycisk.clicked.connect(self.dalej)
        self.start.clicked.connect(self.start_testu)
        self.czerwony1.stateChanged.connect(self.testowanie)
        self.czerwony2.stateChanged.connect(self.testowanie)
        self.czerwony3.stateChanged.connect(self.testowanie)
        self.niebieski1.stateChanged.connect(self.testowanie)
        self.niebieski2.stateChanged.connect(self.testowanie)
        self.niebieski3.stateChanged.connect(self.testowanie)
        self.zolty1.stateChanged.connect(self.testowanie)
        self.zolty2.stateChanged.connect(self.testowanie)
        self.zolty3.stateChanged.connect(self.testowanie)
        self.time=QElapsedTimer()
        self.sprawdzenie_kolorow=''
        self.tryb=0
        self.test.clicked.connect(self.zmiana_na_test)

    def dalej(self):
        self.informacja.hide()
        self.przycisk.setEnabled(False)
        self.przycisk.hide()
        self.start.show()
        self.start.setEnabled(True)
        self.typtestu.show()
        self.test.show()
        self.test.setEnabled(True)
        self.tlo.setStyleSheet('background-color: lightgray;')
        self.tlo2.setStyleSheet("background-color: gray;")
        self.tlo3.setStyleSheet("background-color: lightgray;")

        for i in range(3):
            czerwony1='self.czerwony'+str(i+1)+'.show()'
            niebieski1='self.niebieski'+str(i+1)+'.show()'
            zolty1='self.zolty'+str(i+1)+'.show()'
            exec(czerwony1)
            exec(niebieski1)
            exec(zolty1)

    def start_testu(self):
        self.start.setEnabled(False)

        self.time.start()

        for i in range(3):
            czerwony2='self.czerwony'+str(i+1)+'.setEnabled(True)'
            niebieski2='self.niebieski'+str(i+1)+'.setEnabled(True)'
            zolty2='self.zolty'+str(i+1)+'.setEnabled(True)'
            exec(czerwony2)
            exec(niebieski2)
            exec(zolty2)

        self.tlo.setStyleSheet(random.choice(['background-color: blue;','background-color: red;','background-color: yellow;']))
        self.tlo2.setStyleSheet(random.choice(['background-color: blue;','background-color: red;','background-color: yellow;']))
        self.tlo3.setStyleSheet(random.choice(['background-color: blue;','background-color: red;','background-color: yellow;']))

    def testowanie(self):
        kolor1=''
        kolor2=''
        kolor3=''

        if 'yellow' in self.tlo.styleSheet():
            kolor1='zolty'
        elif 'red' in self.tlo.styleSheet():
            kolor1='czerwony'
        elif 'blue' in self.tlo.styleSheet():
            kolor1='niebieski'

        if 'yellow' in self.tlo2.styleSheet():
            kolor2='zolty'
        elif 'red' in self.tlo2.styleSheet():
            kolor2='czerwony'
        elif 'blue' in self.tlo2.styleSheet():
            kolor2='niebieski'
            
        if 'yellow' in self.tlo3.styleSheet():
            kolor3='zolty'
        elif 'red' in self.tlo3.styleSheet():
            kolor3='czerwony'
        elif 'blue' in self.tlo3.styleSheet():
            kolor3='niebieski'

        self.sprawdzenie_kolorow=''
        
        if kolor1 in unidecode.unidecode(self.czerwony1.text().lower()):

            if self.czerwony1.isChecked() and not self.niebieski1.isChecked() and not self.zolty1.isChecked():

                if kolor2 in unidecode.unidecode(self.czerwony2.text().lower()):
                    if self.czerwony2.isChecked() and not self.niebieski2.isChecked() and not self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyczerwonyczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyczerwonyniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyczerwonyzolty'

                elif kolor2 in unidecode.unidecode(self.niebieski2.text().lower()):
                    if not self.czerwony2.isChecked() and self.niebieski2.isChecked() and not self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyniebieskiczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyniebieskiniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyniebieskizolty'

                elif kolor2 in unidecode.unidecode(self.zolty2.text().lower()):
                    if not self.czerwony2.isChecked() and not self.niebieski2.isChecked() and self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyzoltyczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyzoltyniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='czerwonyzoltyzolty'

        elif kolor1 in unidecode.unidecode(self.niebieski1.text().lower()):
            if not self.czerwony1.isChecked() and self.niebieski1.isChecked() and not self.zolty1.isChecked():

                if kolor2 in unidecode.unidecode(self.czerwony2.text().lower()):
                    if self.czerwony2.isChecked() and not self.niebieski2.isChecked() and not self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskiczerwonyczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskiczerwonyniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskiczerwonyzolty'

                elif kolor2 in unidecode.unidecode(self.niebieski2.text().lower()):
                    if not self.czerwony2.isChecked() and self.niebieski2.isChecked() and not self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskiniebieskiczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskiniebieskiniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskiniebieskizolty'

                elif kolor2 in unidecode.unidecode(self.zolty2.text().lower()):
                    if not self.czerwony2.isChecked() and not self.niebieski2.isChecked() and self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskizoltyczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskizoltyniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='niebieskizoltyzolty'

        elif kolor1 in unidecode.unidecode(self.zolty1.text().lower()):
            if not self.czerwony1.isChecked() and not self.niebieski1.isChecked() and self.zolty1.isChecked():

                if kolor2 in unidecode.unidecode(self.czerwony2.text().lower()):
                    if self.czerwony2.isChecked() and not self.niebieski2.isChecked() and not self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyczerwonyczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyczerwonyniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyczerwonyzolty'

                elif kolor2 in unidecode.unidecode(self.niebieski2.text().lower()):
                    if not self.czerwony2.isChecked() and self.niebieski2.isChecked() and not self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyniebieskiczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyniebieskiniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyniebieskizolty'

                elif kolor2 in unidecode.unidecode(self.zolty2.text().lower()):
                    if not self.czerwony2.isChecked() and not self.niebieski2.isChecked() and self.zolty2.isChecked():

                        if kolor3 in unidecode.unidecode(self.czerwony3.text().lower()):
                            if self.czerwony3.isChecked() and not self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyzoltyczerwony'

                        elif kolor3 in unidecode.unidecode(self.niebieski3.text().lower()):
                            if not self.czerwony3.isChecked() and self.niebieski3.isChecked() and not self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyzoltyniebieski'

                        elif kolor3 in unidecode.unidecode(self.zolty3.text().lower()):
                            if not self.czerwony3.isChecked() and not self.niebieski3.isChecked() and self.zolty3.isChecked():
                                self.sprawdzenie_kolorow='zoltyzoltyzolty'

        if self.sprawdzenie_kolorow==(kolor1+kolor2+kolor3):
            czas=self.time.restart()
            self.szybkosc.setText('Twój czas to: '+str(czas)+' ms')
            self.tlo.setStyleSheet(random.choice(['background-color: blue;','background-color: red;','background-color: yellow;']))
            self.tlo2.setStyleSheet(random.choice(['background-color: blue;','background-color: red;','background-color: yellow;']))
            self.tlo3.setStyleSheet(random.choice(['background-color: blue;','background-color: red;','background-color: yellow;']))
            
            if self.tryb:
                with open('optic2.txt','a') as f:
                    f.write(str(czas)+'\n')

            for i in range(3):
                czerwony='self.czerwony'+str(i+1)+'.setChecked(False)'
                niebieski='self.niebieski'+str(i+1)+'.setChecked(False)'
                zolty='self.zolty'+str(i+1)+'.setChecked(False)'
                exec(czerwony)
                exec(niebieski)
                exec(zolty)
            kolor1=''
            kolor2=''
            kolor3=''
            self.sprawdzenie_kolorow=''

    def zmiana_na_test(self):
        self.tlo.setStyleSheet('background-color: lightgray;')
        self.tlo2.setStyleSheet("background-color: gray;")
        self.tlo3.setStyleSheet("background-color: lightgray;")
        self.szybkosc.setText('')
        self.start.setEnabled(True)

        for i in range(3):
            czerwony2='self.czerwony'+str(i+1)+'.setEnabled(False)'
            niebieski2='self.niebieski'+str(i+1)+'.setEnabled(False)'
            zolty2='self.zolty'+str(i+1)+'.setEnabled(False)'
            exec(czerwony2)
            exec(niebieski2)
            exec(zolty2)

        if self.tryb==0:
            self.typtestu.setText('Test')
            self.tryb=1
            self.test.setText('Szkolenie')
        else:
            self.typtestu.setText('Szkolenie')
            self.tryb=0
            self.test.setText('Test')

class AcousticTest(QWidget,AcousticWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.przycisk.clicked.connect(self.informacje)
        self.start.clicked.connect(self.starttestu)
        self.reakcja.clicked.connect(self.reakcja_uzytkownika)
        self.test.clicked.connect(self.zmiana)

        cwd=os.getcwd()
        akustyczne1=cwd+'/data/akustyczne1.jpg'
        akustyczne2=cwd+'/data/akustyczne1_reakcja.jpg'

        self.pixmap1=QPixmap(akustyczne1)
        self.pixmap2=QPixmap(akustyczne2)

        self.czas_reakcji=QElapsedTimer()

        self.tryb=0
        self.licznik=3

        self.odliczanie_czas=QtCore.QTimer(self)
        self.odliczanie_czas.setSingleShot(True)
        self.odliczanie_czas.timeout.connect(self.odliczanie_funk)

        self.timer_pomocniczy=QtCore.QTimer(self)
        self.timer_pomocniczy.setSingleShot(True)
        self.timer_pomocniczy.timeout.connect(self.przygotuj_test)

        self.glowny_timer=QtCore.QTimer(self)
        self.glowny_timer.setSingleShot(True)
        self.glowny_timer.timeout.connect(self.tluczenie_szklanki)

        self.dzwiek=QMediaPlayer()
        self.szklanka=QMediaPlayer()
        self.zdziwienie=QMediaPlayer()

        url=QUrl.fromLocalFile(cwd+'/data/ludzie.mp3')
        content=QMediaContent(url)
        self.dzwiek.setMedia(content)

        url1=QUrl.fromLocalFile(cwd+'/data/szklanka.mp3')
        content1=QMediaContent(url1)
        self.szklanka.setMedia(content1)
        self.szklanka.setVolume(20)

        url2=QUrl.fromLocalFile(cwd+'/data/zdziwienie.mp3')
        content2=QMediaContent(url2)
        self.zdziwienie.setMedia(content2)

    def informacje(self):
        self.start.show()
        self.reakcja.show()
        self.test.show()
        self.przycisk.hide()
        self.informacja.hide()
        self.tlo.setStyleSheet("background-color: gray;")
        self.typtestu.setText('Szkolenie')

    def starttestu(self):
        self.odliczanie_czas.start()
        self.start.setEnabled(False)
        self.reakcja.setEnabled(False)

    def odliczanie_funk(self):
        self.tlo.clear()
        if self.licznik>=1:
            self.odliczanie.setText(str(self.licznik))
            self.odliczanie_czas.start(1000)
            self.licznik-=1
        else:                        
            self.odliczanie.setText('Start!')
            self.timer_pomocniczy.start(1000)

    def przygotuj_test(self):
        self.tlo.setPixmap(self.pixmap1)
        self.dzwiek.play()
        self.odliczanie.setText('')
        self.glowny_timer.start(random.randrange(2000,10000))

    def tluczenie_szklanki(self):
        self.szklanka.play()
        self.reakcja.setEnabled(True)
        if not self.czas_reakcji.isValid():
            self.czas_reakcji.start()

    def reakcja_uzytkownika(self):
        self.reakcja.setEnabled(False)
        self.tlo.setPixmap(self.pixmap2)
        self.zdziwienie.play()
        self.dzwiek.stop()

        czas=self.czas_reakcji.restart()
        interwal=self.glowny_timer.interval()

        if czas>interwal:
            if (czas-interwal+6000)<0:
                pass
            else:
                czas-=(interwal+6000)

        self.szybkosc.setText('Twój czas reakcji to: '+str(czas)+' ms')
        self.licznik=3
        self.odliczanie_czas.start(2000)
        if self.tryb:
            with open('acoustic1.txt','a') as f:
                f.write(str(czas)+'\n')

    def zmiana(self):
        self.tlo.clear()
        self.czas_reakcji.invalidate()

        if self.dzwiek:
            self.dzwiek.stop()

        if self.zdziwienie:
            self.zdziwienie.stop()

        if self.szklanka:
            self.szklanka.stop()

        self.timer_pomocniczy.stop()
        self.odliczanie_czas.stop()
        self.odliczanie.setText('')
        self.szybkosc.setText('')
        self.start.setEnabled(True)
        self.licznik=3

        if self.tryb:
            self.typtestu.setText('Szkolenie')
            self.test.setText('Test')
            self.tryb=0
        else:
            self.typtestu.setText('Test')
            self.test.setText('Szkolenie')
            self.tryb=1

    def closeEvent(self, event):
        self.timer_pomocniczy.stop()
        self.odliczanie_czas.stop()
        self.glowny_timer.stop()
        self.dzwiek.stop()
        self.zdziwienie.stop()
        self.szklanka.stop()
        event.accept()

class AcousticTest2(QWidget,AcousticWindow2):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.przycisk.clicked.connect(self.informacje)
        self.start.clicked.connect(self.odliczanie_funk)
        self.kon.clicked.connect(self.wybor_kon)
        self.malpa.clicked.connect(self.wybor_malpa)
        self.lew.clicked.connect(self.wybor_lew)
        self.test.clicked.connect(self.zmiana_na_test)

        self.czas_reakcji=QElapsedTimer()
        self.licznik=3
        self.tryb=0
        self.wybrany_zwierzaczek=''

        cwd=os.getcwd()

        self.malpa_obrazek=QPixmap(cwd+'/data/malpa.jpg')
        self.kon_obrazek=QPixmap(cwd+'/data/kon.jpg')
        self.lew_obrazek=QPixmap(cwd+'/data/lew.jpg')

        self.pikanie1=QMediaPlayer()
        self.pikanie2=QMediaPlayer()

        self.kon_dzwiek=QMediaPlayer()
        self.malpa_dzwiek=QMediaPlayer()
        self.lew_dzwiek=QMediaPlayer()

        self.odliczanie_czas=QtCore.QTimer(self)
        self.odliczanie_czas.setSingleShot(True)
        self.odliczanie_czas.timeout.connect(self.odliczanie_funk)

        self.timer_pomocniczy=QtCore.QTimer(self)
        self.timer_pomocniczy.setSingleShot(True)
        self.timer_pomocniczy.timeout.connect(self.przygotuj_test)

        url1=QUrl.fromLocalFile(cwd+'/data/pikanie1.mp3')
        content1=QMediaContent(url1)
        self.pikanie1.setMedia(content1)

        url2=QUrl.fromLocalFile(cwd+'/data/pikanie2.mp3')
        content2=QMediaContent(url2)
        self.pikanie2.setMedia(content2)

        url3=QUrl.fromLocalFile(cwd+'/data/malpa.mp3')
        content3=QMediaContent(url3)
        self.malpa_dzwiek.setMedia(content3)

        url4=QUrl.fromLocalFile(cwd+'/data/lew.mp3')
        content4=QMediaContent(url4)
        self.lew_dzwiek.setMedia(content4)

        url5=QUrl.fromLocalFile(cwd+'/data/kon.mp3')
        content5=QMediaContent(url5)
        self.kon_dzwiek.setMedia(content5)

    def informacje(self):
        self.informacja.hide()
        self.przycisk.hide()

        self.kon.show()
        self.malpa.show()
        self.lew.show()
        self.start.show()
        self.test.show()
        self.typtestu.show()

        self.zwierzaczek1.setPixmap(self.malpa_obrazek)
        self.zwierzaczek2.setPixmap(self.kon_obrazek)
        self.zwierzaczek3.setPixmap(self.lew_obrazek)

        self.start.setEnabled(True)
        self.test.setEnabled(True)

    def odliczanie_funk(self):
        self.start.setEnabled(False)
        if self.licznik>=1:
            self.pikanie1.play()
            self.odliczanie_czas.start(1000)
            self.licznik-=1
        else:                        
            self.pikanie2.play()
            self.timer_pomocniczy.start(random.randrange(2000,10000))

    def przygotuj_test(self):
        self.wybrany_zwierzaczek=random.choice(['lew','kon','malpa'])
        self.licznik=3
        if self.wybrany_zwierzaczek=='lew':
            self.lew_dzwiek.play()
        elif self.wybrany_zwierzaczek=='kon':
            self.kon_dzwiek.play()
        elif self.wybrany_zwierzaczek=='malpa':
            self.malpa_dzwiek.play()

        self.kon.setEnabled(True)
        self.malpa.setEnabled(True)
        self.lew.setEnabled(True)

        if not self.czas_reakcji.isValid():
            self.czas_reakcji.start()

    def wybor_kon(self):
        if self.wybrany_zwierzaczek == unidecode.unidecode(self.kon.text().lower()):
            self.pokaz_czas()
        else:
            self.szybkosc.setText('Zły wybór!')

    def wybor_malpa(self):
        if self.wybrany_zwierzaczek == unidecode.unidecode(self.malpa.text().lower()):
            self.pokaz_czas()  
        else:
            self.szybkosc.setText('Zły wybór!')

    def wybor_lew(self):
        if self.wybrany_zwierzaczek == unidecode.unidecode(self.lew.text().lower()):
           self.pokaz_czas()
        else:
            self.szybkosc.setText('Zły wybór!')

    def pokaz_czas(self):
        czas=self.czas_reakcji.restart()

        interwal=self.timer_pomocniczy.interval()

        if czas>interwal:
            if (czas-interwal+4000)<0:
                pass
            else:
                czas-=(interwal+4000)

        self.szybkosc.setText('Twój czas reakcji: '+str(czas)+' ms')
        self.odliczanie_czas.start(1000)
        self.kon.setEnabled(False)
        self.malpa.setEnabled(False)
        self.lew.setEnabled(False) 

        if self.tryb:
            with open('acoustic2.txt','a') as f:
                f.write(str(czas)+'\n')

    def zmiana_na_test(self):
        self.malpa.setEnabled(False)
        self.kon.setEnabled(False)
        self.lew.setEnabled(False)

        self.start.setEnabled(True)

        self.timer_pomocniczy.stop()
        self.odliczanie_czas.stop()
        self.czas_reakcji.invalidate()

        self.kon_dzwiek.stop()
        self.malpa_dzwiek.stop()
        self.lew_dzwiek.stop()
        self.pikanie1.stop()
        self.pikanie2.stop()

        self.szybkosc.setText('')
        self.licznik=3

        if self.tryb:
            self.typtestu.setText('Szkolenie')
            self.test.setText('Test')
            self.tryb=0
        else:
            self.typtestu.setText('Test')
            self.test.setText('Szkolenie')
            self.tryb=1

    def closeEvent(self, event):
        self.timer_pomocniczy.stop()
        self.odliczanie_czas.stop()
        self.kon_dzwiek.stop()
        self.malpa_dzwiek.stop()
        self.lew_dzwiek.stop()
        self.pikanie1.stop()
        self.pikanie2.stop()
        event.accept()

class Window(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.testOptyczny.clicked.connect(self.test_optyczny)
        self.testOptycznyAdv.clicked.connect(self.test_optyczny2)
        self.testAkustyczny.clicked.connect(self.test_akustyczny)
        self.testAkustycznyAdv.clicked.connect(self.test_akustyczny2)
        self.wyswietlanieWynikow.clicked.connect(self.wyniki)

        self.msg= QMessageBox()
        self.msg.setWindowTitle('Brak danych!')
        self.msg.setText('Proszę najpierw wykonać wszystkie badania w trybie testowym!')

        open('optic1.txt', 'a').close()
        open('optic2.txt', 'a').close()
        open('acoustic1.txt', 'a').close()
        open('acoustic2.txt', 'a').close()

    def wyniki(self):
        lista_reakcji1=lista_reakcji_pliki('optic1.txt')
        lista_reakcji2=lista_reakcji_pliki('optic2.txt')
        lista_reakcji3=lista_reakcji_pliki('acoustic1.txt')
        lista_reakcji4=lista_reakcji_pliki('acoustic2.txt')

        if not lista_reakcji1 or not lista_reakcji2 or not lista_reakcji3 or not lista_reakcji4:
            self.msg.exec_()
        else:
            fig, axs = plt.subplots(2, 2)
            axs[0, 0].plot(lista_reakcji1)
            axs[0, 0].set_title('Optyczny 1, czas reakcji: \n'+str(round(sum(lista_reakcji1)/len(lista_reakcji1),2))+' ms')
            axs[0, 1].plot(lista_reakcji2, 'tab:orange')
            axs[0, 1].set_title('Optyczny 2, czas reakcji: \n'+str(round(sum(lista_reakcji2)/len(lista_reakcji2),2))+' ms')
            axs[1, 0].plot(lista_reakcji3, 'tab:green')
            axs[1, 0].set_title('Akustyczny 1, czas reakcji: \n'+str(round(sum(lista_reakcji3)/len(lista_reakcji3),2))+' ms')
            axs[1, 1].plot(lista_reakcji4, 'tab:red')
            axs[1, 1].set_title('Akustyczny 2, czas reakcji: \n'+str(round(sum(lista_reakcji4)/len(lista_reakcji4),2))+' ms')

            axs[0, 0].set_xticks(range(0,len(lista_reakcji1)+1, 1))
            axs[0, 1].set_xticks(range(0,len(lista_reakcji2)+1, 1))
            axs[1, 0].set_xticks(range(0,len(lista_reakcji3)+1, 1))
            axs[1, 1].set_xticks(range(0,len(lista_reakcji4)+1, 1))
            for ax in axs.flat:
                ax.set(xlabel='podejście', ylabel='wynik (ms)')
            fig.tight_layout()
            plt.show()

    def test_optyczny(self):
        self.optic = OpticTest()
        self.optic.show()

    def test_optyczny2(self):
        self.optic2 = OpticTest2()
        self.optic2.show()

    def test_akustyczny(self):
        self.acoustic = AcousticTest()
        self.acoustic.show()

    def test_akustyczny2(self):
        self.acoustic2 = AcousticTest2()
        self.acoustic2.show()


def lista_reakcji_pliki(plik):
    test = open(plik, "r")

    lista_reakcji=[]
    for czas in test:
        czas=czas.strip()
        lista_reakcji.append(int(czas))

    test.close()
    return lista_reakcji


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())