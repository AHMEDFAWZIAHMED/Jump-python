
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEvent
from pro import Pro

class PlaceHolder(QLabel):

    indx = 0
    validDrag = True
    
    def __init__(self, parent, loc, indx):
        super(QLabel, self).__init__(parent)
        self.setPixmap(QPixmap('empty.png'))
        self.move(loc[0], loc[1])
        self.setAcceptDrops(True)
        self.installEventFilter(self)
        self.setObjectName("PlaceHolder")
        #self.setStyleSheet(Pro.plHoSty)
        self.parent = parent
        self.indx = indx
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        placeRC = Pro.getRowColIndex(self.pos().x(), self.pos().y())
        possMove = Pro.possibleMove(Pro.track[0])
        possJump = []
        for pj in Pro.possibleJump(Pro.track[0]):
            possJump.append(pj[1])

        if placeRC in possMove or placeRC in possJump:
            self.validDrag = True
        else:
            self.validDrag = False
            if Pro.getPlayerIndex(self.pos().x(), self.pos().y()) == Pro.track[0][1]:
                Pro.popupMessage = "Not a move!"
        if len(Pro.track) == 3:
            if placeRC not in possJump:
                self.validDrag = False
            if not Pro.track[2]:
                self.validDrag = False
        if event.mimeData().hasImage() and self.validDrag:
            self.parent.parent().moveRock(self.pos())
        
        else:
            self.parent.parent().popupDialog()
            if len(Pro.track) < 3:
                Pro.track.clear()
                Pro.disabledRocks.clear()

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            QApplication.restoreOverrideCursor()
            Pro.popupMessage = "Cannot move here!"
            return True
        return False