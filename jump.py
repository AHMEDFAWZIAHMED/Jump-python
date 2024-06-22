from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout
from menu import Menu
from play import Play
from result import Result
import sys

class Jump(QWidget):

  def __init__(self, *args, **kwargs):
      QWidget.__init__(self, *args, **kwargs)

      self.setWindowTitle("Jump")
      self.setFixedSize(600, 700)
      self.move(400, 100)

      self.mainMenu = Menu(self)
      self.startGame = Play(self)
      self.showResult = Result(self)

      self.stackedWidget = QStackedLayout(self)

      self.stackedWidget.addWidget(self.mainMenu)
      self.stackedWidget.addWidget(self.startGame)
      self.stackedWidget.addWidget(self.showResult)

      self.changeFrames(0)

  def changeFrames(self, indx):
    self.stackedWidget.setCurrentIndex(indx)
    changes = {
      0: self.mainMenu.startMenu,
      1: self.startGame.createBoard,
      2: self.showResult.createOptions
    }[indx]()

  def endGame(self):
    self.close()


if __name__ == "__main__":
    app = QApplication([])
    jumpGame = Jump()
    jumpGame.show()
    sys.exit(app.exec())