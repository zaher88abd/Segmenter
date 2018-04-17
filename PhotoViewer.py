from PyQt5.QtCore import QSize
from qtconsole.qt import QtGui, QtCore


class MyQGraphicsView(QtGui.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    ...

    def toggleDragMode(self):
        if self.dragMode() == QtGui.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        try:
            if self.scene.isUnderMouse():
                self.photoClicked.emit(QtCore.QPoint(event.pos()))
            # keep the default behaviour
            super(MyQGraphicsView, self).mousePressEvent(event)
        except Exception as e:
            print(e)

    def sizeHint(self):
        return QSize(400, 400)
