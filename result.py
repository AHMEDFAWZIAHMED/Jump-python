from PyQt5.QtWidgets import QFrame, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from pro import Pro

class Result(QFrame):

    def __init__(self, parent):
        QFrame.__init__(self, parent)

        self.setFixedSize(600, 700)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QImage("background2.jpg")))
        self.setPalette(palette)
        self.parent = parent

    def createOptions(self):
        msg = QLabel("Game over", self)
        msg.setStyleSheet(Pro.rMsgSty)
        msg.move(160, 50)

        self.gmRes = QLabel(self)
        self.gmRes.setFont(QFont("Arial", 20, QFont.Black, True))
        self.gmRes.move(190, 150)

        for i in range(1, 4):
            button = QPushButton(Pro.resButtons[i-1], self)
            button.setStyleSheet(Pro.reBttnSty)
            button.resize(300, 70)
            button.move(150, (i+1)*120)
            button.clicked.connect(lambda checked, i=i: self.userChoice(i-1))

    def userChoice(self, indx):
        if indx < 2:
            self.parent.changeFrames((-1+indx)*-1)
        else:
            self.parent.endGame()
