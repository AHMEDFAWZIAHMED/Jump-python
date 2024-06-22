from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QPoint, QEvent
from PyQt5.QtGui import QPixmap, QDrag, QPainter
from pro import Pro


class DragableLabel(QLabel):

    plrIndx = []
    hisIndx = []
    
    def __init__(self, parent, indx, plInx):
        super(QLabel, self).__init__(parent)
        self.setPixmap(QPixmap(Pro.imgPath[indx]))
        self.move(Pro.getLocation([indx, plInx]))
        self.installEventFilter(self)
        self.setObjectName("DragableLabel")
        self.setStyleSheet(Pro.drLabSty)
        self.indx = indx
        self.parent = parent
        self.plrIndx = [indx, plInx]
        self.show()

    def changeIndx(self, newIndx):
        self.hisIndx.append(self.plrIndx[1])
        self.plrIndx[1] = newIndx

    def returnToLastPosition(self):
        loc = Pro.getLocation([self.indx, self.hisIndx[-1]])
        Pro.players[self.indx][Pro.getPlaIndx(self.plrIndx)] = Pro.getPlayerIndex(loc.x(), loc.y())
        Pro.track[0][1] = Pro.getPlayerIndex(loc.x(), loc.y())
        self.move(loc)
        self.plrIndx[1] = self.hisIndx[-1]
        self.hisIndx.pop()

    def mousePressEvent(self, event):
        if self.plrIndx in Pro.disabledRocks:
            Pro.locTrack = self.pos()
            self.parent.parent().popupDialog()
            return
        if event.button() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)
            self.drag_start_position = event.pos()
            if not Pro.track:
                Pro.track.append(self.plrIndx)
                #print("Track added by User: {}".format(Pro.track))
            
    def mouseMoveEvent(self, event):
        if self.plrIndx in Pro.disabledRocks:
            return
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setImageData(self.pixmap())

        drag.setMimeData(mimedata)
        pixmap = QPixmap(Pro.imgPath[self.indx])
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        self.setHidden(True)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(35, 35))
        drag.deleteLater()
        drag.exec_()
        self.setHidden(False)

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            # For illegal rock for user player vs computer:
            if Pro.illegalMove(self.plrIndx) or Pro.menuResult[0] == self.indx:
                QApplication.setOverrideCursor(Qt.ForbiddenCursor)
                Pro.disabledRocks.append(self.plrIndx)
                Pro.popupMessage = "Cannot move this rock!"
                return True
            # For players turn. user vs user mode
            if Pro.menuResult[0] == 2 and self.indx == Pro.playTurn:
                QApplication.setOverrideCursor(Qt.ForbiddenCursor)
                Pro.disabledRocks.append(self.plrIndx)
                Pro.popupMessage = "Not your turn!"
                return True
            if Pro.track:
                # For after move only
                if len(Pro.track) == 1:
                    QApplication.setOverrideCursor(Qt.ForbiddenCursor)
                    Pro.disabledRocks.append(self.plrIndx)
                    Pro.popupMessage = "No move left!"
                    return True
                # For after jump only
                if len(Pro.track) == 2:
                    QApplication.setOverrideCursor(Qt.ForbiddenCursor)
                    Pro.disabledRocks.append(self.plrIndx)
                    Pro.popupMessage = "Only double jumps!"
                    return True
                # For after double jump only
                if len(Pro.track) == 3:
                    if self.plrIndx != Pro.track[0]:
                        QApplication.setOverrideCursor(Qt.ForbiddenCursor)
                        Pro.disabledRocks.append(self.plrIndx)
                        Pro.popupMessage = "Only the last rock!"
                        return True
                    elif not Pro.track[2][0]:
                        QApplication.setOverrideCursor(Qt.ForbiddenCursor)
                        Pro.disabledRocks.append(self.plrIndx)
                        Pro.popupMessage = "Only jump for this rock!"
                        return True
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
            self.setPixmap(QPixmap(Pro.hovImgPath[self.indx]))
            return True
        if event.type() == QEvent.Leave:
            QApplication.restoreOverrideCursor()
            self.setPixmap(QPixmap(Pro.imgPath[self.indx]))
        return False