import sys
from main_window import Ui_MainWindow
from progress_bars import Pbar,SignalBar
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMainWindow, QProgressBar, QMessageBox
from PySide2.QtCore import QTimer
from PySide2.QtCore import QPropertyAnimation, QThread, Signal
import time
from PySide2.QtGui import QPixmap
import random

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.username=''
        self.loginButton.clicked.connect(self.login)
        self.tvButton.clicked.connect(self.watchTv)
        self.pcButton.clicked.connect(self.playGames)
        self.napButton.clicked.connect(self.sleepCouch)
        self.sleepButton.clicked.connect(self.sleepBed)
        self.eatButton.clicked.connect(self.eatBig)
        self.drinkButton.clicked.connect(self.eatSmall)
        self.showerButton.clicked.connect(self.shower)
        self.brushButton.clicked.connect(self.brushTeeth)
        self.workButton.clicked.connect(self.work)
        self.lotteryButton.clicked.connect(self.lotteryTicket)
        self.daysTimer=QTimer()
        self.daysTimer.timeout.connect(self.updateDays)

        self.actionTimer=QTimer()
        self.actionTimer.setSingleShot(True)

        self.upgShower.clicked.connect(self.upgradeShower)
        self.upgBed.clicked.connect(self.upgradeBed)
        self.upgTv.clicked.connect(self.upgradeTv)
        self.upgWalls.clicked.connect(self.upgradeWalls)
        self.upgFridge.clicked.connect(self.upgradeFridge)
        self.upgRoof.clicked.connect(self.upgradeRoof)

        self.actionBarTimer=QTimer()
        
        self.tvWatchingGraphic=QPixmap('assets/tvWatching.png')
        self.playingGames=QPixmap('assets/gaming.png')
        self.sleepingInBed=QPixmap('assets/sleeping.png')
        self.sleepingOnCouch=QPixmap('assets/napping.png')
        self.eatingSmall=QPixmap('assets/drinking.png')
        self.eatingBig=QPixmap('assets/eating.png')
        self.showering=QPixmap('assets/shower.png')
        self.brushing=QPixmap('assets/teeth.png')
        self.working=QPixmap('assets/working.png')
        self.lottery=QPixmap('assets/lottery.png')

        self.wallsPng1=QPixmap('assets/walls1.png')
        self.wallsPng2=QPixmap('assets/walls2.png')
        self.showerPng1=QPixmap('assets/shower1.png')
        self.showerPng2=QPixmap('assets/shower2.png')
        self.tvPng1=QPixmap('assets/tv1.png')
        self.tvPng2=QPixmap('assets/tv2.png')
        self.fridgePng1=QPixmap('assets/fridge1.png')
        self.fridgePng2=QPixmap('assets/fridge2.png')
        self.roofPng1=QPixmap('assets/roof1.png')
        self.roofPng2=QPixmap('assets/roof2.png')
        self.bedPng1=QPixmap('assets/bed1.png')
        self.bedPng2=QPixmap('assets/bed2.png')

        self.funFlag=True
        self.higieneFlag=True
        self.hungerFlag=True
        self.energyFlag=True
        self.deathFlag=True
        self.money=0

        self.tier=0
        self.amount=0
        self.day=0
        
        self.bedLvl=0
        self.showerLvl=0
        self.wallsLvl=0
        self.roofLvl=0
        self.tvLvl=0
        self.fridgeLvl=0

        self.energyModifier=0
        self.higieneModifier=0
        self.funModifier=0
        self.hungerModifier=0

        self.burglarsTimer=QTimer()
        self.burglarsTimer.timeout.connect(self.burglars)

        self.showHouse()


    def login(self):
        if not self.nick.text():
            self.loginWarn.show()
        else:
            self.loginWarn.hide()

        if not self.password.text():
            self.passWarn.show()
        else:
            self.passWarn.hide()

        if self.nick.text() and self.password.text():
            self.username=self.nick.text()

            self.hideLoginScreen()
            self.showGameScreen()

            self.funDeplete = Pbar()
            self.funDeplete.speed=0.5
            self.funDeplete.valueChanged.connect(self.funBarDeplete)
            self.funDeplete.start()
            
            self.daysTimer.start(3000)
            self.burglarsTimer.start(random.randint(15000,20000))

            self.energyDeplete=Pbar()
            self.energyDeplete.speed=2
            self.energyDeplete.valueChanged.connect(self.energyBarDeplete)
            self.energyDeplete.start()

            self.hungerDeplete=Pbar()
            self.hungerDeplete.speed=0.75
            self.hungerDeplete.valueChanged.connect(self.hungerBarDeplete)
            self.hungerDeplete.start()

            self.higieneDeplete=Pbar()
            self.higieneDeplete.speed=0.9
            self.higieneDeplete.valueChanged.connect(self.higieneBarDeplete)
            self.higieneDeplete.start()

            self.comfortSignal=SignalBar()
            self.comfortSignal.valueChanged.connect(self.recalculateComfort)
            self.comfortSignal.start()


    def burglars(self):
        event=random.choice(['flood','burglars'])

        if event=='flood':
            self.floodAlert()
        if event=='burglars':
            self.burglarsAlert()

    def floodAlert(self):
        alert = QMessageBox()
        alert.setText('Mieszkanie na Żuławach Wiślanych nie było dobrym pomysłem! Trochę popadało i dom w ruinie! Ściany zniszczone! Telewizor do naprawy!')
        alert.setWindowTitle('Powódź!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        if self.wallsLvl:
            self.wallsLvl=0
        if self.tvLvl:
            self.tvLvl=0
        self.showHouse()
        alert.exec_()

    def burglarsAlert(self):
        alert = QMessageBox()
        if self.money>=500:
            self.money-=500
            alert.setText(f'{self.username} został okradziony! To niebezpieczna dzielnica!')
        else:
            alert.setText(f'Złodzieje przyszli do domu {self.username}, jednak zauważyli jak bardzo bieda tutaj piszczy i sami zostawili trochę pieniędzy!')
            self.money+=500
        alert.setWindowTitle('Złodzieje!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        self.moneyLabelUpdate()
        alert.exec_()

    def recalculateComfort(self):
        self.comfort.setValue(self.energyModifier+self.hungerModifier+self.higieneModifier+self.funModifier+10*(self.bedLvl
        +self.tvLvl+self.fridgeLvl+self.roofLvl+self.wallsLvl+self.showerLvl))

        if self.comfort.value()<=40:
            self.funDeplete.speed=0.5
            self.energyDeplete.speed=2
            self.hungerDeplete.speed=0.75
            self.higieneDeplete.speed=0.9

        if self.comfort.value()>40:
            self.funDeplete.speed=0.85
            self.energyDeplete.speed=2.3
            self.hungerDeplete.speed=1
            self.higieneDeplete.speed=1.1

        if self.comfort.value()>80:
            self.funDeplete.speed=1.2
            self.energyDeplete.speed=2.5
            self.hungerDeplete.speed=1.1
            self.higieneDeplete.speed=1.2

        if self.hunger.value()<=1 and self.deathFlag:
            self.deathAlert()

    def updateDays(self):
        self.day+=1
        self.dayLabel.setText('Dzień: '+str(self.day))

        if self.day%30==0:
            self.billsAlert()

    def billsAlert(self):
        alert = QMessageBox()
        alert.setText('Czas zapłacić rachunki, jeśli nie masz pieniędzy to koniec gry!')
        alert.setWindowTitle('Rachunki!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        if self.money>=2000:
            self.money-=2000
        else:
            self.logout()
        self.moneyLabelUpdate()
        alert.exec_()

    def watchTv(self):
        self.tier=1
        self.amount=25
        self.actionTimer.timeout.connect(self.enableFun)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.funDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.tvWatchingGraphic)
        self.hideHouse()
        self.actionTimer.start(4005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def playGames(self):
        self.tier=0
        self.amount=50
        self.actionTimer.timeout.connect(self.enableFun)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.funDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.playingGames)
        self.hideHouse()
        self.actionTimer.start(2005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def enableFun(self):
        self.funDeplete.waiting=0
        self.enableButtons()
        self.gifLabel.clear()
        self.funAdd(self.tier)
        self.actionTimer.stop()
        self.actionBarTimer.stop()
        self.actionBarTimer.timeout.disconnect(self.actionBarUpdate)
        self.actionProgress.hide()
        self.actionProgress.setValue(0)
        self.showHouse()
        self.actionTimer.timeout.disconnect(self.enableFun)

    def sleepBed(self):
        self.tier=1
        self.amount=25
        self.actionTimer.timeout.connect(self.enableEnergy)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.energyDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.sleepingInBed)
        self.hideHouse()
        self.actionTimer.start(4005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def sleepCouch(self):
        self.tier=0
        self.amount=50
        self.actionTimer.timeout.connect(self.enableEnergy)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.energyDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.sleepingOnCouch)
        self.hideHouse()
        self.actionTimer.start(2005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def enableEnergy(self):
        self.energyDeplete.waiting=0
        self.enableButtons()
        self.gifLabel.clear()
        self.energyAdd(self.tier)
        self.actionTimer.stop()
        self.actionBarTimer.stop()
        self.actionBarTimer.timeout.disconnect(self.actionBarUpdate)
        self.actionProgress.hide()
        self.actionProgress.setValue(0)
        self.showHouse()
        self.actionTimer.timeout.disconnect(self.enableEnergy)

    def eatBig(self):
        self.tier=1
        self.amount=25
        self.actionTimer.timeout.connect(self.enableHunger)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.hungerDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.eatingBig)
        self.hideHouse()
        self.actionTimer.start(4005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()
    
    def eatSmall(self):
        self.tier=0
        self.amount=50
        self.actionTimer.timeout.connect(self.enableHunger)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.hungerDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.eatingSmall)
        self.hideHouse()
        self.actionTimer.start(2005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def enableHunger(self):
        self.hungerDeplete.waiting=0
        self.enableButtons()
        self.gifLabel.clear()
        self.hungerAdd(self.tier)
        self.actionTimer.stop()
        self.actionBarTimer.stop()
        self.actionBarTimer.timeout.disconnect(self.actionBarUpdate)
        self.actionProgress.hide()
        self.actionProgress.setValue(0)
        self.showHouse()
        self.actionTimer.timeout.disconnect(self.enableHunger)

    def shower(self):
        self.tier=1
        self.amount=25
        self.actionTimer.timeout.connect(self.enableHigiene)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.higieneDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.showering)
        self.hideHouse()
        self.actionTimer.start(4005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def brushTeeth(self):
        self.tier=0
        self.amount=50
        self.actionTimer.timeout.connect(self.enableHigiene)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.higieneDeplete.waiting=1
        self.disableButtons()
        self.gifLabel.setPixmap(self.brushing)
        self.hideHouse()
        self.actionTimer.start(2005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def enableHigiene(self):
        self.higieneDeplete.waiting=0
        self.enableButtons()
        self.gifLabel.clear()
        self.higieneAdd(self.tier)
        self.actionTimer.stop()
        self.actionBarTimer.stop()
        self.actionBarTimer.timeout.disconnect(self.actionBarUpdate)
        self.actionProgress.hide()
        self.actionProgress.setValue(0)
        self.showHouse()
        self.actionTimer.timeout.disconnect(self.enableHigiene)

    def work(self):
        self.tier=1
        self.amount=25
        self.actionTimer.timeout.connect(self.enableWork)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.disableButtons()
        self.gifLabel.setPixmap(self.working)
        self.hideHouse()
        self.actionTimer.start(4005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def lotteryTicket(self):
        self.tier=0
        self.amount=50
        self.actionTimer.timeout.connect(self.enableWork)
        self.actionBarTimer.timeout.connect(self.actionBarUpdate)
        self.disableButtons()
        self.gifLabel.setPixmap(self.lottery)
        self.hideHouse()
        self.actionTimer.start(2005)
        self.actionBarTimer.start(1000)
        self.actionProgress.show()

    def enableWork(self):
        self.enableButtons()
        self.gifLabel.clear()
        self.moneyAdd(self.tier)
        self.actionTimer.stop()
        self.actionBarTimer.stop()
        self.actionBarTimer.timeout.disconnect(self.actionBarUpdate)
        self.actionProgress.hide()
        self.actionProgress.setValue(0)
        self.showHouse()
        self.actionTimer.timeout.disconnect(self.enableWork)

    def moneyAdd(self,tier):
        if tier:
            self.money+=2500
        else:
            self.money+=500
        self.moneyLabelUpdate()

    def funAdd(self,tier):
        if tier:
            self.funDeplete.value+=25
        else:
            self.funDeplete.value+=10

        if self.funDeplete.value>100:
            self.funDeplete.value=99
        if self.funDeplete.isFinished() and self.funDeplete.value:
            self.funDeplete.start()

        self.actionProgress.setValue(0)

    def energyAdd(self,tier):
        if tier:
            self.energyDeplete.value+=25
        else:
            self.energyDeplete.value+=10

        if self.energyDeplete.value>100:
            self.energyDeplete.value=99
        if self.energyDeplete.isFinished() and self.energyDeplete.value:
            self.energyDeplete.start()  

    def higieneAdd(self,tier):
        if tier:
            self.higieneDeplete.value+=25
        else:
            self.higieneDeplete.value+=10

        if self.higieneDeplete.value>100:
            self.higieneDeplete.value=99
        if self.higieneDeplete.isFinished() and self.higieneDeplete.value:
            self.higieneDeplete.start()  

    def hungerAdd(self,tier):
        if tier:
            self.hungerDeplete.value+=25
        else:
            self.hungerDeplete.value+=10

        if self.hungerDeplete.value>100:
            self.hungerDeplete.value=99
        if self.hungerDeplete.isFinished() and self.hungerDeplete.value:
            self.hungerDeplete.start()  


    def funBarDeplete(self, emittedValue):
        if emittedValue<=20 and self.funFlag:
            self.funAlert()
            self.funModifier=0
        if emittedValue>20:
            self.funFlag=True
            self.funModifier=10
        self.fun.setValue(emittedValue)

    def higieneBarDeplete(self, emittedValue):
        if emittedValue<=20 and self.higieneFlag:
            self.higieneAlert()
            self.higieneModifier=0
        if emittedValue>20:
            self.higieneFlag=True
            self.higieneModifier=10
        self.higiene.setValue(emittedValue)

    def hungerBarDeplete(self, emittedValue):
        if emittedValue<=20 and self.hungerFlag:
            self.hungerAlert()
            self.hungerModifier=0
        if emittedValue>20:
            self.hungerFlag=True
            self.hungerModifier=10
        self.hunger.setValue(emittedValue)

    def energyBarDeplete(self, emittedValue):
        if emittedValue<=20 and self.energyFlag:
            self.energyAlert()
            self.energyModifier=0
        if emittedValue>20:
            self.energyModifier=10
            self.energyFlag=True
        self.energy.setValue(emittedValue)

    def actionBarUpdate(self):
        self.actionProgress.setValue(self.actionProgress.value()+self.amount)

    def funAlert(self):
        alert = QMessageBox()
        alert.setText(f'{self.username} jest niesamowicie zestresowany!')
        alert.setWindowTitle('Niski poziom zabawy!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        self.funFlag=False
        alert.exec_()

    def higieneAlert(self):
        alert = QMessageBox()
        alert.setText(f'{self.username} jest brudasem!')
        alert.setWindowTitle('Niski poziom higieny!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        self.higieneFlag=False
        alert.exec_()

    def energyAlert(self):
        alert = QMessageBox()
        alert.setText(f'{self.username} chyba siedzi do późna w nocy, ponieważ jest strasznie przemęczony!')
        alert.setWindowTitle('Niski poziom energii!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        self.energyFlag=False
        alert.exec_()

    def hungerAlert(self):
        alert = QMessageBox()
        alert.setText(f'{self.username} jest chyba na diecie! Niech lepiej coś zje zanim zginie!')
        alert.setWindowTitle('Głód!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        self.hungerFlag=False
        alert.exec_()

    def deathAlert(self):
        alert = QMessageBox()
        alert.setText(f'{self.username} umarł z głodu! Czasami nowomodne diety nie popłacają!')
        alert.setWindowTitle('R.I.P!')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        self.deathFlag=False
        alert.exec_()
        #sys.exit()
        self.logout()

    def hideLoginScreen(self):
        self.the.hide()
        self.symulator.hide()
        self.loginButton.hide()
        self.passWarn.hide()
        self.password.hide()
        self.nick.hide()
        self.loginLabel.hide()
        self.loginWarn.hide()

    def showGameScreen(self):
        self.energy.show()
        self.energyLabel.show()
        self.fun.show()
        self.funLabel.show()
        self.hunger.show()
        self.hungerLabel.show()
        self.higiene.show()
        self.higieneLabel.show()
        self.comfort.show()
        self.comfortLabel.show()

        self.upgBed.show()
        self.upgFridge.show()
        self.upgRoof.show()
        self.upgShower.show()
        self.upgTv.show()
        self.upgWalls.show()  

        self.gifLabel.show()
        self.bedGraphics.show()
        self.tvGraphics.show()
        self.roofGraphics.show()
        self.wallsGraphics.show()
        self.showerGraphics.show()
        self.fridgeGraphics.show()

        self.dayLabel.show()
        self.moneyLabel.show()
        self.roofLabel.show()
        self.lifeLabel.show()
        self.buyLabel.show()
        self.pcButton.show()
        self.tvButton.show()
        self.eatButton.show()
        self.napButton.show()
        self.workButton.show()
        self.lotteryButton.show()
        self.drinkButton.show()
        self.sleepButton.show()
        self.brushButton.show()
        self.showerButton.show()

        self.borders.show()

    def disableButtons(self):
        self.pcButton.setDisabled(True)
        self.tvButton.setDisabled(True)
        self.eatButton.setDisabled(True)
        self.napButton.setDisabled(True)
        self.workButton.setDisabled(True)
        self.lotteryButton.setDisabled(True)
        self.drinkButton.setDisabled(True)
        self.sleepButton.setDisabled(True)
        self.brushButton.setDisabled(True)
        self.showerButton.setDisabled(True)

        self.upgBed.setDisabled(True)
        self.upgFridge.setDisabled(True)
        self.upgRoof.setDisabled(True)
        self.upgShower.setDisabled(True)
        self.upgTv.setDisabled(True)
        self.upgWalls.setDisabled(True)

    def enableButtons(self):
        self.pcButton.setEnabled(True)
        self.tvButton.setEnabled(True)
        self.eatButton.setEnabled(True)
        self.napButton.setEnabled(True)
        self.workButton.setEnabled(True)
        self.lotteryButton.setEnabled(True)
        self.drinkButton.setEnabled(True)
        self.sleepButton.setEnabled(True)
        self.brushButton.setEnabled(True)
        self.showerButton.setEnabled(True)

        if not self.bedLvl:
            self.upgBed.setEnabled(True)
        if not self.fridgeLvl:    
            self.upgFridge.setEnabled(True)
        if not self.roofLvl:    
            self.upgRoof.setEnabled(True)
        if not self.showerLvl:
            self.upgShower.setEnabled(True)
        if not self.tvLvl:
            self.upgTv.setEnabled(True)
        if not self.wallsLvl:    
            self.upgWalls.setEnabled(True)

    def moneyLabelUpdate(self):
        self.moneyLabel.setText('Pieniądze: '+str(self.money))

    def upgradeRoof(self):
        if self.money>=5000 and not self.roofLvl:
            self.roofLvl=1
            self.money-=5000
            self.moneyLabelUpdate()
            self.upgRoof.setEnabled(False)
        self.showHouse()

    def upgradeFridge(self):
        if self.money>=2500 and not self.fridgeLvl:
            self.fridgeLvl=1
            self.money-=2500
            self.moneyLabelUpdate()
            self.upgFridge.setEnabled(False)
        self.showHouse()

    def upgradeWalls(self):
        if self.money>=1000 and not self.wallsLvl:
            self.wallsLvl=1
            self.money-=1000
            self.moneyLabelUpdate()
            self.upgWalls.setEnabled(False)
        self.showHouse()

    def upgradeTv(self):
        if self.money>=6000 and not self.tvLvl:
            self.tvLvl=1
            self.money-=6000
            self.moneyLabelUpdate()
            self.upgTv.setEnabled(False)
        self.showHouse()

    def upgradeShower(self):
        if self.money>=4000 and not self.showerLvl:
            self.showerLvl=1
            self.money-=4000
            self.moneyLabelUpdate()
            self.upgShower.setEnabled(False)
        self.showHouse()

    def upgradeBed(self):
        if self.money>=10000 and not self.bedLvl:
            self.bedLvl=1
            self.money-=10000
            self.moneyLabelUpdate()
            self.upgBed.setEnabled(False)
        self.showHouse()

    def showHouse(self):
        if self.roofLvl:
            self.roofGraphics.setPixmap(self.roofPng2)
        else:
            self.roofGraphics.setPixmap(self.roofPng1)

        if self.bedLvl:
            self.bedGraphics.setPixmap(self.bedPng2)
        else:
            self.bedGraphics.setPixmap(self.bedPng1)

        if self.showerLvl:
            self.showerGraphics.setPixmap(self.showerPng2)
        else:
            self.showerGraphics.setPixmap(self.showerPng1)

        if self.tvLvl:
            self.tvGraphics.setPixmap(self.tvPng2)
        else:
            self.tvGraphics.setPixmap(self.tvPng1)

        if self.wallsLvl:
            self.gifLabel.setPixmap(self.wallsPng2)
        else:
            self.gifLabel.setPixmap(self.wallsPng1)

        if self.fridgeLvl:
            self.fridgeGraphics.setPixmap(self.fridgePng2)
        else:
            self.fridgeGraphics.setPixmap(self.fridgePng1)

    def hideHouse(self):
        self.fridgeGraphics.clear()
        self.tvGraphics.clear()
        self.bedGraphics.clear()
        self.showerGraphics.clear()

    def logout(self):
        self.energy.hide()
        self.energyLabel.hide()
        self.fun.hide()
        self.funLabel.hide()
        self.hunger.hide()
        self.hungerLabel.hide()
        self.higiene.hide()
        self.higieneLabel.hide()
        self.comfort.hide()
        self.comfortLabel.hide()

        self.upgBed.hide()
        self.upgFridge.hide()
        self.upgRoof.hide()
        self.upgShower.hide()
        self.upgTv.hide()
        self.upgWalls.hide()  

        self.gifLabel.hide()
        self.bedGraphics.hide()
        self.tvGraphics.hide()
        self.roofGraphics.hide()
        self.wallsGraphics.hide()
        self.showerGraphics.hide()
        self.fridgeGraphics.hide()

        self.dayLabel.hide()
        self.moneyLabel.hide()
        self.roofLabel.hide()
        self.lifeLabel.hide()
        self.buyLabel.hide()
        self.pcButton.hide()
        self.tvButton.hide()
        self.eatButton.hide()
        self.napButton.hide()
        self.workButton.hide()
        self.lotteryButton.hide()
        self.drinkButton.hide()
        self.sleepButton.hide()
        self.brushButton.hide()
        self.showerButton.hide()

        self.borders.hide()

        self.the.show()
        self.symulator.show()
        self.loginButton.show()
        self.passWarn.show()
        self.password.show()
        self.nick.show()
        self.loginLabel.show()
        self.loginWarn.show()

        self.funFlag=True
        self.higieneFlag=True
        self.hungerFlag=True
        self.energyFlag=True
        self.deathFlag=True
        self.money=0

        self.tier=0
        self.amount=0
        self.day=0
        self.dayLabel.setText('Dzień: 0')
        
        self.bedLvl=0
        self.showerLvl=0
        self.wallsLvl=0
        self.roofLvl=0
        self.tvLvl=0
        self.fridgeLvl=0

        self.energyModifier=0
        self.higieneModifier=0
        self.funModifier=0
        self.hungerModifier=0

        self.loginButton.show()

        self.daysTimer.stop()
        self.burglarsTimer.stop()

        self.funDeplete.waiting=True
        self.fun.setValue(90)
        self.energyDeplete.waiting=True
        self.energy.setValue(90)
        self.hungerDeplete.waiting=True
        self.hunger.setValue(90)
        self.higieneDeplete.waiting=True
        self.higiene.setValue(90)

        self.hungerDeplete.value=90
        self.higieneDeplete.value=90
        self.energyDeplete.value=90
        self.funDeplete.value=90



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())