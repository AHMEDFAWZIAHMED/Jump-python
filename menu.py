from PyQt5.QtWidgets import QFrame, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QTimer
from pro import Pro

class Menu(QFrame):

    def __init__(self, parent):
        QFrame.__init__(self, parent)

        self.setFixedSize(600, 700)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QImage("background1.jpg")))
        self.setPalette(palette)
        self.parent = parent

    def startMenu(self):
        def showName():
            gameName = QLabel("نط الكلب", self)
            gameName.setStyleSheet(Pro.gNameSty)
            gameName.move(200, 50)
            gameName.show()

        QTimer.singleShot(400, lambda: showName())

        def showPaw():
            self.paw = QLabel(self)
            self.paw.setPixmap(QPixmap("paw.png"))
            self.paw.move(50, 150)
            self.paw.show()

            self.firstMenu()

        QTimer.singleShot(800, lambda: showPaw())

    def firstMenu(self):
        def showFButtons(indx):
            button = QPushButton(Pro.fMenuBttns[indx], self.paw)
            button.move(105, (indx+1)*110)
            button.setStyleSheet(Pro.menuBttnSty)
            button.resize(300, 70)
            button.clicked.connect(lambda checked, indx=indx: self.userChoice(indx))
            button.show()
        for i in range(3):
            QTimer.singleShot((i+1)*400, lambda i=i: showFButtons(i))

    def secondMenu(self):
        def showSButtons(indx):
            button = QPushButton(Pro.sMenuBttns[indx], self.paw)
            button.move(100, (indx+1)*87)
            button.setStyleSheet(Pro.menuBttnSty)
            button.resize(300, 70)
            button.clicked.connect(lambda checked, indx=indx: self.userChoice(indx+3))
            button.show()
        for i in range(4):
            QTimer.singleShot((i+1)*400, lambda i=i: showSButtons(i))

    def userChoice(self, num):
        for child in self.paw.children():
            child.deleteLater()
        self.paw.children().clear()
        choices = {
            0: self.secondMenu,
            1: self.parent.changeFrames,
            2: self.parent.endGame,
            3: self.parent.changeFrames,
            4: self.parent.changeFrames,
            5: self.parent.changeFrames,
            6: self.firstMenu
        }
        if num == 0 or num == 2 or num == 6:
            choices[num]()
        else:
            newValue = {
                1: [2, 0],
                3: [1, 0],
                4: [1, 1],
                5: [1, 2]
            }
            Pro.menuResult = newValue[num]
            for child in self.children():
                child.deleteLater()
            self.children().clear()
            choices[num](1)