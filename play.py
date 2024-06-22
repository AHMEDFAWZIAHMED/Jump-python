from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QDialog
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QTimer, Qt, QEvent, QPoint
import copy
from dragableLabel import DragableLabel
from placeHolder import PlaceHolder
from pro import Pro

class Play(QFrame):

    def __init__(self, parent):
        QFrame.__init__(self, parent)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QImage("background3.jpg")))
        self.setPalette(palette)
        self.installEventFilter(self)
        self.parent = parent

    def createBoard(self):
        self.board = QLabel(self)
        self.board.setPixmap(QPixmap("board1.jpg"))
        self.board.move(50, 100)
        self.board.show()

        for i in range(25):
            PlaceHolder(self.board, Pro.matrix[Pro.allRowCOl[i][0], Pro.allRowCOl[i][1]], i)
        for i in range(2):
            revIndex = (-1+i)*-1# turns 0 to 1 and 1 to 0
            button = QPushButton(Pro.buttonsText[revIndex], self)
            button.setGeometry(300, (i*600)+25, 250, 50)
            button.setStyleSheet(Pro.bttnSty)
            button.clicked.connect(lambda checked, revIndex=revIndex: self.endTurn(revIndex))
            button.setDisabled(True)
            button.show()
            Pro.buttons.append(button)
            for j in range(12):
                rock = DragableLabel(self.board, i, (revIndex*13)+j)
                Pro.rocks[i].append(rock)
        for i in range(2):
            undoBttn = QPushButton("Undo", self)
            undoBttn.setGeometry(180, (i*600)+25, 100, 50)
            undoBttn.setStyleSheet(Pro.bttnSty)
            undoBttn.clicked.connect(lambda checked, i=i: self.undoLastMove(i))
            undoBttn.setDisabled(True)
            undoBttn.show()
            Pro.buttons.append(undoBttn)

            backBttn = QPushButton("Back\nto\nmenu", self)
            backBttn.setGeometry(50, (i*600)+15, 100, 70)
            backBttn.setStyleSheet(Pro.bckBttnSty)
            backBttn.clicked.connect(lambda: self.backToMenu())
            backBttn.show()


    def moveRock(self, pos):
        # olPlIn = old player index (copy of the first list in track)
        olPlIn = copy.deepcopy(Pro.track[0])
        plyIndx = Pro.getPlaIndx(olPlIn)
        playerIndex = Pro.getPlayerIndex(pos.x(), pos.y())
        Pro.rocks[olPlIn[0]][plyIndx].move(pos)
        Pro.rocks[olPlIn[0]][plyIndx].changeIndx(playerIndex)

        jumpList = Pro.possibleJump(olPlIn)
        if jumpList:
            # Check if the player index is in the list that inside the jump list
            for jump in jumpList:
                if (jump[1][0]*5)+jump[1][1] == playerIndex:
                    # roTore: rock to remove (from 0 to 24)
                    roTore = (jump[0][0]*5)+jump[0][1]
                    # plaIndx: index of the rock in players list (from 0 to 11)
                    plaIndx = Pro.getPlaIndx([Pro.playTurn, roTore])
                    if len(Pro.track) >= 2:
                        Pro.track[1].append([Pro.playTurn, plaIndx, roTore])
                    else:
                        Pro.track.append([[Pro.playTurn, plaIndx, roTore]])
                    QTimer.singleShot(
                        500, lambda: self.jumpProcess([Pro.playTurn, plaIndx], pos, True))
                    break
        else:
            Pro.track[0][1] = playerIndex
        Pro.players[olPlIn[0]][plyIndx] = playerIndex
        Pro.buttons[Pro.playTurn].setDisabled(False)
        Pro.buttons[Pro.playTurn+2].setDisabled(False)
    
    def undoLastMove(self, num):
        # For current player's rock only
        Pro.rocks[Pro.track[0][0]][Pro.getPlaIndx(Pro.track[0])].returnToLastPosition()

        # Function for disable buttons and clear lists
        def disAndCl():
            Pro.track.clear()
            Pro.disabledRocks.clear()
            Pro.buttons[num+2].setDisabled(True)
        
        # For removed rock/s checking track size
        if len(Pro.track) > 1:
            #laReRoc: last removed rock
            laReRoc = Pro.track[1][-1]
            Pro.rocks[laReRoc[0]][laReRoc[1]].setHidden(False)
            Pro.players[laReRoc[0]][laReRoc[1]] = laReRoc[2]
            # Remove the last removed rock from track
            Pro.track[1].pop()
            # Check if there is a multible jump before disable and clear
            if not Pro.track[1]:
                disAndCl()

        else:
            disAndCl()
        Pro.buttons[num].setDisabled(True)

    def animation(self, playerIndx, location, isJump):
        # playerIndx: [1, index range from 0 to 11 including 11]
        # plyIndx: value of player location index: index range from 0 to 24 including 24
        plyIndx = Pro.players[1][playerIndx[1]]
        
        anim = QPropertyAnimation(Pro.rocks[1][playerIndx[1]], b'pos', self)
        anim.setStartValue(Pro.getLocation([playerIndx[0], plyIndx]))
        anim.setEndValue(location)
        anim.setDuration(1000)
        anim.start(QAbstractAnimation.DeleteWhenStopped)

        QTimer.singleShot(1050, lambda: self.computer(playerIndx[0], playerIndx[1], location, isJump))

    def computer(self, firIndx, secIndx, loc, isJump):
        trackCopy = copy.deepcopy(Pro.track)
        Pro.rocks[firIndx][secIndx].move(loc)
        Pro.rocks[firIndx][secIndx].changeIndx(Pro.getPlayerIndex(loc.x(), loc.y()))
        Pro.players[firIndx][secIndx] = Pro.getPlayerIndex(loc.x(), loc.y())
        if isJump:
            QTimer.singleShot(
                400, lambda: self.jumpProcess(
                    [Pro.track[1][0], Pro.getPlaIndx([trackCopy[1][0], trackCopy[1][1]])], loc))
        else:
            self.endTurn(1)

    def jumpProcess(self, indxList, pos, user=False):
        Pro.rocks[indxList[0]][indxList[1]].setHidden(True)
        Pro.players[indxList[0]][indxList[1]] = -1
        playrIndx = [Pro.track[0][0], Pro.getPlayerIndex(pos.x(), pos.y())]
        Pro.track[0][1] = playrIndx[1]

        if max(Pro.players[0]) == -1:
            self.gameOver("Player two win!")
            return
        elif max(Pro.players[1]) == -1:
            self.gameOver("Player One win!")
            return

        if not user:
            # Check for another jump for Computer
            if Pro.possibleJump(playrIndx):
                # Call cpuChoice with true parameter for double jump
                cpu = Pro.cpuChoice(True)
                if cpu:
                    QTimer.singleShot(500, lambda: self.animation(cpu[0], cpu[1], cpu[2]))
                else:
                    self.endTurn(1)
            else:
                self.endTurn(1)
        # Check for another jump for User
        elif Pro.possibleJump(playrIndx):
            if len(Pro.track) == 3:
                Pro.track[2][0] = True
            else:
                Pro.track.append([True])
            # Remove playrIndx from disabledRock
            disabled = [l for l in Pro.disabledRocks if l != playrIndx]
            Pro.disabledRocks = disabled
        else:
            Pro.disabledRocks.append(playrIndx)
            if len(Pro.track) == 3:
                Pro.track[2][0] = False

    def endTurn(self, num):
        Pro.buttons[Pro.playTurn].setDisabled(True)
        Pro.buttons[Pro.playTurn+2].setDisabled(True)
        Pro.playTurn = num
        Pro.track.clear()
        Pro.disabledRocks.clear()
        if Pro.menuResult[0] == 1 and num != 1:# User vs Computer (only for user use)
            cpu = Pro.cpuChoice()
            if cpu:
                QTimer.singleShot(500, lambda: self.animation(cpu[0], cpu[1], cpu[2]))
            else:
                # Something went wrong or all Computer's rocks are traped
                print("No more move for Computer")
                # If Computer's rocks are traped: Game over: Computer win or draw?
        elif Pro.menuResult[0] == 2:# User vs User
            Pro.locTrack = QPoint(self.board.pos().x()+150, self.board.pos().y()+120)
            Pro.popupMessage = Pro.startTurn[num]
            self.popupDialog()
        
    def popupDialog(self):
        dialog = QDialog(self)
        dialog.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        dialog.setAttribute(Qt.WA_TranslucentBackground)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.move(self.parent.pos().x()+Pro.locTrack.x(), self.parent.pos().y()+Pro.locTrack.y()+130)
        msg = QLabel(dialog)
        msg.setText(Pro.popupMessage)
        msg.setStyleSheet(Pro.msgSty)
        dialog.setFixedSize(350, 40)
        dialog.show()
        QTimer.singleShot(1000, lambda: dialog.hide())

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            QApplication.restoreOverrideCursor()
            return True
        return False

    def gameOver(self, result):
        Pro.resultMsg = result
        Pro.resetValues()
        self.parent.changeFrames(2)

    def backToMenu(self):
        Pro.resetValues()
        self.parent.changeFrames(0)