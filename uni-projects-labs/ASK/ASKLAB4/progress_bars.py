import time
from PySide2.QtCore import QThread, Signal

class Pbar(QThread):

    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.value=90
        self.speed=1
        self.waiting=0

    def run(self):

        while self.value >0 and not self.waiting:
            self.value -=1
            time.sleep(self.speed)
            self.valueChanged.emit(self.value)


class SignalBar(QThread):

    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.value=40

    def run(self):

        while True:
            time.sleep(0.2)
            self.valueChanged.emit(self.value)
