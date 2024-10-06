from encodings import utf_8
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.GuzikWyslij = QtWidgets.QPushButton(self.centralwidget)
        self.GuzikWyslij.setGeometry(QtCore.QRect(20, 510, 101, 31))
        self.GuzikWyslij.setObjectName("GuzikWyslij")
        self.GuzikWyslij.clicked.connect(self.wyslij)

        self.GuzikOdbierz = QtWidgets.QPushButton(self.centralwidget)
        self.GuzikOdbierz.setGeometry(QtCore.QRect(520, 510, 101, 31))
        self.GuzikOdbierz.setObjectName("GuzikOdbierz")
        self.GuzikOdbierz.clicked.connect(self.odbierz)

        self.GuzikUsun = QtWidgets.QPushButton(self.centralwidget)
        self.GuzikUsun.setGeometry(QtCore.QRect(140, 510, 101, 31))
        self.GuzikUsun.setObjectName("GuzikUsun")
        self.GuzikUsun.clicked.connect(self.usun)

        self.Label1 = QtWidgets.QLabel(self.centralwidget)
        self.Label1.setGeometry(QtCore.QRect(30, 10, 161, 31))
        self.Label1.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.Label1.setObjectName("Label1")

        self.Label2 = QtWidgets.QLabel(self.centralwidget)
        self.Label2.setGeometry(QtCore.QRect(320, 20, 161, 16))
        self.Label2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.Label2.setObjectName("Label2")

        self.Label3 = QtWidgets.QLabel(self.centralwidget)
        self.Label3.setGeometry(QtCore.QRect(550, 20, 171, 16))
        self.Label3.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.Label3.setObjectName("Label3")

        self.TekstWysylany = QtWidgets.QTextEdit(self.centralwidget)
        self.TekstWysylany.setGeometry(QtCore.QRect(20, 50, 221, 441))
        self.TekstWysylany.setAutoFillBackground(False)
        self.TekstWysylany.setObjectName("TekstWysylany")

        self.TekstZnaki = QtWidgets.QTextEdit(self.centralwidget)
        self.TekstZnaki.setGeometry(QtCore.QRect(270, 50, 221, 441))
        self.TekstZnaki.setAutoFillBackground(False)
        self.TekstZnaki.setReadOnly(True)
        self.TekstZnaki.setPlaceholderText("")
        self.TekstZnaki.setObjectName("TekstZnaki")

        self.TekstOdebrany = QtWidgets.QTextEdit(self.centralwidget)
        self.TekstOdebrany.setGeometry(QtCore.QRect(520, 50, 221, 441))
        self.TekstOdebrany.setAutoFillBackground(False)
        self.TekstOdebrany.setReadOnly(True)
        self.TekstOdebrany.setPlaceholderText("")
        self.TekstOdebrany.setObjectName("TekstOdebrany")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASK LAB2"))
        self.GuzikWyslij.setText(_translate("MainWindow", "Wyślij"))
        self.GuzikOdbierz.setText(_translate("MainWindow", "Odbierz"))
        self.GuzikUsun.setText(_translate("MainWindow", "Usuń"))
        self.Label1.setText(_translate("MainWindow", "Wiadomość do wysłania:"))
        self.Label2.setText(_translate("MainWindow", "Ciąg znaków:"))
        self.Label3.setText(_translate("MainWindow", "Odebrana wiadomość:"))
        self.TekstWysylany.setPlaceholderText(_translate("MainWindow", "Wpisz wiadomość ..."))

    def wyslij(self):
        wysylanyTekst=self.TekstWysylany.toPlainText()
        kodowane=''
        for i in range(len(wysylanyTekst)):
            literka=wysylanyTekst[i]
            bajt1,bajt2=tekst_na_bity(literka)
            kodowane=kodowane+bajt1+'\n'+bajt2+'\n'
            self.TekstZnaki.setPlainText(kodowane)

        with open('wiadomosc.txt', 'w') as f:
            f.write(self.TekstZnaki.toPlainText())

    def odbierz(self):
        odbieranyTekst=[]
        with open('wiadomosc.txt', 'r') as f:
            for line in f.readlines():
                for w in line.split():
                    odbieranyTekst.append(w)
        tekst=''
        for i in range(0,len(odbieranyTekst),2):
            tekst=tekst+tekst_z_bitow(odbieranyTekst[i],odbieranyTekst[i+1])

        tekst=cenzura(tekst)

        self.TekstOdebrany.setText(tekst)

    def usun(self):
        self.TekstWysylany.setText('')
        self.TekstZnaki.setText('')
        self.TekstOdebrany.setText('')


def cenzura(do_cenzury):

    slownik=[]
    with open('cenzura.txt', 'r') as f:
        for line in f.readlines():
            for w in line.split():
                slownik.append(w)

    lista_slow=do_cenzury.split()

    for i in range(len(lista_slow)):
        for j in range(len(slownik)):
            slowo=lista_slow[i]
            znalezione=slowo.find(slownik[j])
            gwiazdki='*'*len(slownik[j])
            if znalezione!=-1:
                lista_slow[i]=slowo[:znalezione]+gwiazdki+slowo[(znalezione+len(slownik[j])):]
    slowa=''
    for i in range(len(lista_slow)):
        slowa=slowa+lista_slow[i]+' '

    return slowa
    

def tekst_na_bity(tekst, encoding='utf-8', errors='surrogatepass'):

    bity = bin(int.from_bytes(tekst.encode(encoding, errors), 'big'))[2:]
    bity=bity.zfill(8 * ((len(bity) + 7) // 8))

    bajt1=bity[-8:]
    bajt1=bajt1[::-1]
    bajt1='0'+bajt1+'11'

    if len(bity)>8:
        bajt2=bity[:(len(bity)-8)]
    else:
        bajt2='00000000'

    bajt2=bajt2[::-1]
    bajt2='0'+bajt2+'11'

    return bajt1,bajt2

def tekst_z_bitow(bajt1,bajt2, encoding='utf-8', errors='surrogatepass'):

    bajt1=bajt1[1:]
    bajt1=bajt1[:-2]
    bajt1=bajt1[::-1]

    bajt2=bajt2[1:]
    bajt2=bajt2[:-2]
    bajt2=bajt2[::-1]

    bity=bajt2+bajt1

    n = int(bity, 2)
    odkodowane=n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

    return odkodowane


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
