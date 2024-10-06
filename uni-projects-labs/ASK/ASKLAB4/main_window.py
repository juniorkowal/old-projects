from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1280, 720)
        font = QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setCursor(QCursor(Qt.ArrowCursor))
        MainWindow.setIconSize(QSize(30, 30))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.the = QLabel(self.centralwidget)
        self.the.setObjectName(u"the")
        self.the.setGeometry(QRect(270, 120, 181, 121))
        font1 = QFont()
        font1.setPointSize(62)
        self.the.setFont(font1)
        self.symulator = QLabel(self.centralwidget)
        self.symulator.setObjectName(u"symulator")
        self.symulator.setGeometry(QRect(440, 150, 611, 141))
        font2 = QFont()
        font2.setFamily(u"Lucida Calligraphy")
        font2.setPointSize(62)
        font2.setItalic(True)
        self.symulator.setFont(font2)
        self.loginLabel = QLabel(self.centralwidget)
        self.loginLabel.setObjectName(u"loginLabel")
        self.loginLabel.setGeometry(QRect(500, 310, 301, 31))
        font3 = QFont()
        font3.setPointSize(15)
        self.loginLabel.setFont(font3)
        self.nick = QLineEdit(self.centralwidget)
        self.nick.setObjectName(u"nick")
        self.nick.setGeometry(QRect(500, 360, 211, 31))
        self.password = QLineEdit(self.centralwidget)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(500, 410, 211, 31))
        self.loginWarn = QLabel(self.centralwidget)
        self.loginWarn.setObjectName(u"loginWarn")
        self.loginWarn.setGeometry(QRect(720, 360, 201, 31))
        self.loginWarn.setFont(font)
        self.passWarn = QLabel(self.centralwidget)
        self.passWarn.setObjectName(u"passWarn")
        self.passWarn.setEnabled(True)
        self.passWarn.setGeometry(QRect(720, 410, 121, 31))
        self.passWarn.setFont(font)
        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setGeometry(QRect(580, 470, 211, 41))
        self.loginButton.setFont(font3)
        self.energy = QProgressBar(self.centralwidget)
        self.energy.setObjectName(u"energy")
        self.energy.setGeometry(QRect(380, 510, 61, 151))
        self.energy.setValue(90)
        self.energy.setTextVisible(False)
        self.energy.setOrientation(Qt.Vertical)
        self.energy.setTextDirection(QProgressBar.TopToBottom)
        self.energyLabel = QLabel(self.centralwidget)
        self.energyLabel.setObjectName(u"energyLabel")
        self.energyLabel.setGeometry(QRect(380, 670, 61, 21))
        font4 = QFont()
        font4.setPointSize(10)
        self.energyLabel.setFont(font4)
        self.energyLabel.setAlignment(Qt.AlignCenter)
        self.hunger = QProgressBar(self.centralwidget)
        self.hunger.setObjectName(u"hunger")
        self.hunger.setGeometry(QRect(510, 510, 61, 151))
        self.hunger.setValue(90)
        self.hunger.setTextVisible(False)
        self.hunger.setOrientation(Qt.Vertical)
        self.hunger.setTextDirection(QProgressBar.TopToBottom)
        self.higiene = QProgressBar(self.centralwidget)
        self.higiene.setObjectName(u"higiene")
        self.higiene.setGeometry(QRect(640, 510, 61, 151))
        self.higiene.setValue(90)
        self.higiene.setTextVisible(False)
        self.higiene.setOrientation(Qt.Vertical)
        self.higiene.setTextDirection(QProgressBar.TopToBottom)
        self.fun = QProgressBar(self.centralwidget)
        self.fun.setObjectName(u"fun")
        self.fun.setGeometry(QRect(770, 510, 61, 151))
        self.fun.setValue(90)
        self.fun.setTextVisible(False)
        self.fun.setOrientation(Qt.Vertical)
        self.fun.setTextDirection(QProgressBar.TopToBottom)
        self.comfort = QProgressBar(self.centralwidget)
        self.comfort.setObjectName(u"comfort")
        self.comfort.setGeometry(QRect(900, 510, 61, 151))
        self.comfort.setValue(0)
        self.comfort.setTextVisible(False)
        self.comfort.setOrientation(Qt.Vertical)
        self.comfort.setTextDirection(QProgressBar.TopToBottom)
        self.hungerLabel = QLabel(self.centralwidget)
        self.hungerLabel.setObjectName(u"hungerLabel")
        self.hungerLabel.setGeometry(QRect(510, 670, 61, 21))
        self.hungerLabel.setFont(font4)
        self.hungerLabel.setAlignment(Qt.AlignCenter)
        self.higieneLabel = QLabel(self.centralwidget)
        self.higieneLabel.setObjectName(u"higieneLabel")
        self.higieneLabel.setGeometry(QRect(640, 670, 61, 21))
        self.higieneLabel.setFont(font4)
        self.higieneLabel.setAlignment(Qt.AlignCenter)
        self.funLabel = QLabel(self.centralwidget)
        self.funLabel.setObjectName(u"funLabel")
        self.funLabel.setGeometry(QRect(770, 670, 61, 21))
        self.funLabel.setFont(font4)
        self.funLabel.setAlignment(Qt.AlignCenter)
        self.comfortLabel = QLabel(self.centralwidget)
        self.comfortLabel.setObjectName(u"comfortLabel")
        self.comfortLabel.setGeometry(QRect(900, 670, 61, 21))
        self.comfortLabel.setFont(font4)
        self.comfortLabel.setAlignment(Qt.AlignCenter)
        self.showerButton = QToolButton(self.centralwidget)
        self.showerButton.setObjectName(u"showerButton")
        self.showerButton.setGeometry(QRect(30, 70, 91, 91))
        font5 = QFont()
        font5.setPointSize(11)
        self.showerButton.setFont(font5)
        self.eatButton = QToolButton(self.centralwidget)
        self.eatButton.setObjectName(u"eatButton")
        self.eatButton.setGeometry(QRect(30, 180, 91, 91))
        self.eatButton.setFont(font5)
        self.workButton = QToolButton(self.centralwidget)
        self.workButton.setObjectName(u"workButton")
        self.workButton.setGeometry(QRect(30, 510, 91, 91))
        self.workButton.setFont(font5)
        self.tvButton = QToolButton(self.centralwidget)
        self.tvButton.setObjectName(u"tvButton")
        self.tvButton.setGeometry(QRect(30, 400, 91, 91))
        self.tvButton.setFont(font5)
        self.tvButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.drinkButton = QToolButton(self.centralwidget)
        self.drinkButton.setObjectName(u"drinkButton")
        self.drinkButton.setGeometry(QRect(140, 180, 91, 91))
        self.drinkButton.setFont(font5)
        self.sleepButton = QToolButton(self.centralwidget)
        self.sleepButton.setObjectName(u"sleepButton")
        self.sleepButton.setGeometry(QRect(30, 290, 91, 91))
        self.sleepButton.setFont(font5)
        self.brushButton = QToolButton(self.centralwidget)
        self.brushButton.setObjectName(u"brushButton")
        self.brushButton.setGeometry(QRect(140, 70, 91, 91))
        self.brushButton.setFont(font5)
        self.napButton = QToolButton(self.centralwidget)
        self.napButton.setObjectName(u"napButton")
        self.napButton.setGeometry(QRect(140, 290, 91, 91))
        self.napButton.setFont(font5)
        self.pcButton = QToolButton(self.centralwidget)
        self.pcButton.setObjectName(u"pcButton")
        self.pcButton.setGeometry(QRect(140, 400, 91, 91))
        self.pcButton.setFont(font5)
        self.pcButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.lotteryButton = QToolButton(self.centralwidget)
        self.lotteryButton.setObjectName(u"lotteryButton")
        self.lotteryButton.setGeometry(QRect(140, 510, 91, 91))
        self.lotteryButton.setFont(font5)
        self.lotteryButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.upgShower = QToolButton(self.centralwidget)
        self.upgShower.setObjectName(u"upgShower")
        self.upgShower.setGeometry(QRect(1050, 70, 91, 91))
        self.upgShower.setFont(font5)
        self.lifeLabel = QLabel(self.centralwidget)
        self.lifeLabel.setObjectName(u"lifeLabel")
        self.lifeLabel.setGeometry(QRect(60, 20, 141, 31))
        self.lifeLabel.setFont(font3)
        self.buyLabel = QLabel(self.centralwidget)
        self.buyLabel.setObjectName(u"buyLabel")
        self.buyLabel.setGeometry(QRect(1090, 20, 131, 31))
        self.buyLabel.setFont(font3)
        self.upgFridge = QToolButton(self.centralwidget)
        self.upgFridge.setObjectName(u"upgFridge")
        self.upgFridge.setGeometry(QRect(1160, 70, 91, 91))
        self.upgFridge.setFont(font5)
        self.upgBed = QToolButton(self.centralwidget)
        self.upgBed.setObjectName(u"upgBed")
        self.upgBed.setGeometry(QRect(1050, 200, 91, 91))
        self.upgBed.setFont(font5)
        self.upgTv = QToolButton(self.centralwidget)
        self.upgTv.setObjectName(u"upgTv")
        self.upgTv.setGeometry(QRect(1160, 200, 91, 91))
        self.upgTv.setFont(font5)
        self.upgWalls = QToolButton(self.centralwidget)
        self.upgWalls.setObjectName(u"upgWalls")
        self.upgWalls.setGeometry(QRect(1050, 330, 91, 91))
        self.upgWalls.setFont(font5)
        self.upgRoof = QToolButton(self.centralwidget)
        self.upgRoof.setObjectName(u"upgRoof")
        self.upgRoof.setGeometry(QRect(1160, 330, 91, 91))
        self.upgRoof.setFont(font5)
        self.moneyLabel = QLabel(self.centralwidget)
        self.moneyLabel.setObjectName(u"moneyLabel")
        self.moneyLabel.setGeometry(QRect(1050, 450, 201, 31))
        self.moneyLabel.setFont(font3)
        self.dayLabel = QLabel(self.centralwidget)
        self.dayLabel.setObjectName(u"dayLabel")
        self.dayLabel.setGeometry(QRect(30, 620, 341, 81))
        font6 = QFont()
        font6.setPointSize(28)
        self.dayLabel.setFont(font6)
        self.gifLabel = QLabel(self.centralwidget)
        self.gifLabel.setObjectName(u"gifLabel")
        self.gifLabel.setGeometry(QRect(260, 30, 761, 461))
        self.gifLabel.setFont(font6)
        self.roofLabel = QLabel(self.centralwidget)
        self.roofLabel.setObjectName(u"roofLabel")
        self.roofLabel.setGeometry(QRect(990, 510, 201, 31))
        self.roofLabel.setFont(font3)
        self.roofGraphics = QLabel(self.centralwidget)
        self.roofGraphics.setObjectName(u"roofGraphics")
        self.roofGraphics.setGeometry(QRect(990, 550, 261, 141))
        self.roofGraphics.setFont(font3)
        self.actionProgress = QProgressBar(self.centralwidget)
        self.actionProgress.setObjectName(u"actionProgress")
        self.actionProgress.setGeometry(QRect(510, 30, 321, 23))
        self.actionProgress.setValue(0)
        self.actionProgress.setTextVisible(False)
        self.showerGraphics = QLabel(self.centralwidget)
        self.showerGraphics.setObjectName(u"showerGraphics")
        self.showerGraphics.setGeometry(QRect(900,190,105,97))
        self.showerGraphics.setFont(font6)
        self.bedGraphics = QLabel(self.centralwidget)
        self.bedGraphics.setObjectName(u"bedGraphics")
        self.bedGraphics.setGeometry(QRect(330,240,328,263))
        self.bedGraphics.setFont(font6)
        self.fridgeGraphics = QLabel(self.centralwidget)
        self.fridgeGraphics.setObjectName(u"fridgeGraphics")
        self.fridgeGraphics.setGeometry(QRect(710,150,170,272))
        self.fridgeGraphics.setFont(font6)
        self.tvGraphics = QLabel(self.centralwidget)
        self.tvGraphics.setObjectName(u"tvGraphics")
        self.tvGraphics.setGeometry(QRect(350,80,189,189))
        self.tvGraphics.setFont(font6)
        self.wallsGraphics = QLabel(self.centralwidget)
        self.wallsGraphics.setObjectName(u"wallsGraphics")
        self.wallsGraphics.setGeometry(QRect(540, 60, 211, 121))
        self.wallsGraphics.setFont(font6)
        self.borders = QLabel(self.centralwidget)
        self.borders.setObjectName(u"borders")
        self.borders.setGeometry(QRect(384, 525, 581, 111))
        MainWindow.setCentralWidget(self.centralwidget)

        self.loginWarn.hide()
        self.passWarn.hide()
        self.energy.hide()
        self.energyLabel.hide()
        self.higiene.hide()
        self.higieneLabel.hide()
        self.hunger.hide()
        self.hungerLabel.hide()
        self.comfort.hide()
        self.comfortLabel.hide()
        self.fun.hide()
        self.funLabel.hide()
        
        self.gifLabel.hide()
        self.bedGraphics.hide()
        self.tvGraphics.hide()
        self.roofGraphics.hide()
        self.wallsGraphics.hide()
        self.showerGraphics.hide()
        self.fridgeGraphics.hide()
        self.actionProgress.hide()
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

        self.upgBed.hide()
        self.upgFridge.hide()
        self.upgRoof.hide()
        self.upgShower.hide()
        self.upgTv.hide()
        self.upgWalls.hide()
        
        self.borders.hide()
        bordersGraphic = QPixmap('assets/borders.png')
        self.borders.setPixmap(bordersGraphic)



        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"The Symulator", None))
        self.the.setText(QCoreApplication.translate("MainWindow", u"The", None))
        self.symulator.setText(QCoreApplication.translate("MainWindow", u"Symulator", None))
        self.loginLabel.setText(QCoreApplication.translate("MainWindow", u"Zaloguj si\u0119 i wejd\u017a do gry!", None))
        self.nick.setText("")
        self.nick.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nazwa u\u017cytkownika", None))
        self.password.setText("")
        self.password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Has\u0142o", None))
        self.loginWarn.setText(QCoreApplication.translate("MainWindow", u"Niepoprawna nazwa u\u017cytkownika!", None))
        self.passWarn.setText(QCoreApplication.translate("MainWindow", u"Niepoprawne has\u0142o!", None))
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"Zaloguj mnie!", None))
        self.energy.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.energyLabel.setText(QCoreApplication.translate("MainWindow", u"Energia", None))
        self.hunger.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.higiene.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.fun.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.comfort.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.hungerLabel.setText(QCoreApplication.translate("MainWindow", u"G\u0142\u00f3d", None))
        self.higieneLabel.setText(QCoreApplication.translate("MainWindow", u"Higiena", None))
        self.funLabel.setText(QCoreApplication.translate("MainWindow", u"Zabawa", None))
        self.comfortLabel.setText(QCoreApplication.translate("MainWindow", u"Komfort", None))
        self.showerButton.setText(QCoreApplication.translate("MainWindow", u"K\u0105piel", None))
        self.eatButton.setText(QCoreApplication.translate("MainWindow", u"Zjedz co\u015b", None))
        self.workButton.setText(QCoreApplication.translate("MainWindow", u"Pracuj", None))
        self.tvButton.setText(QCoreApplication.translate("MainWindow", u"Telewizja", None))
        self.drinkButton.setText(QCoreApplication.translate("MainWindow", u"Wypij co\u015b", None))
        self.sleepButton.setText(QCoreApplication.translate("MainWindow", u"Id\u017a spa\u0107", None))
        self.brushButton.setText(QCoreApplication.translate("MainWindow", u"Umyj z\u0119by", None))
        self.napButton.setText(QCoreApplication.translate("MainWindow", u"Drzemka", None))
        self.pcButton.setText(QCoreApplication.translate("MainWindow", u"Komputer", None))
        self.lotteryButton.setText(QCoreApplication.translate("MainWindow", u"Loteria", None))
        self.upgShower.setText(QCoreApplication.translate("MainWindow", u"Prysznic", None))
        self.lifeLabel.setText(QCoreApplication.translate("MainWindow", u"Akcje - \u017cycie", None))
        self.buyLabel.setText(QCoreApplication.translate("MainWindow", u"Kupowanie", None))
        self.upgFridge.setText(QCoreApplication.translate("MainWindow", u"Lod\u00f3wka", None))
        self.upgBed.setText(QCoreApplication.translate("MainWindow", u"\u0141\u00f3\u017cko", None))
        self.upgTv.setText(QCoreApplication.translate("MainWindow", u"TV", None))
        self.upgWalls.setText(QCoreApplication.translate("MainWindow", u"\u015aciany", None))
        self.upgRoof.setText(QCoreApplication.translate("MainWindow", u"Dach", None))
        self.moneyLabel.setText(QCoreApplication.translate("MainWindow", u"Pieni\u0105dze: 0", None))
        self.dayLabel.setText(QCoreApplication.translate("MainWindow", u"Dzie\u0144: 0", None))
        self.gifLabel.setText("")
        self.roofLabel.setText(QCoreApplication.translate("MainWindow", u"Podgl\u0105d dachu", None))
        self.roofGraphics.setText("")
        self.showerGraphics.setText("")
        self.bedGraphics.setText("")
        self.fridgeGraphics.setText("")
        self.tvGraphics.setText("")
        self.wallsGraphics.setText("")
        self.borders.setText("")
    # retranslateUi

