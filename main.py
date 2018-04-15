import cv2
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from lib.filter import *


class Segmeter(QDialog):
    def __init__(self):
        super(Segmeter, self).__init__()
        loadUi('main.ui', self)
        self.image = None
        self.openBtn.clicked.connect(self.openFile)

    @pyqtSlot()
    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self, "Open file")
        self.file_name = file_name[0]
        self.loadImage()

    def loadImage(self):
        self.image = cv2.imread(self.file_name)
        self.displayImage()

    def displayImage(self):
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        self.fimage = filter()
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()
        f_img = QImage()
        self.orgImg.setPixmap(QPixmap.fromImage(img))
        self.orgImg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


app = QApplication(sys.argv)
window = Segmeter()
window.setWindowTitle("Segmeter")
window.show()
sys.exit(app.exec_())
