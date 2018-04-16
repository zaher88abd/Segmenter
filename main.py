import sys
import os
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from lib.filter import *


class Segmeter(QDialog):
    def __init__(self):
        super().__init__()
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

        self.f_image = filter_image(self.image, 1)
        height, width = self.image.shape[:2]
        max_height = 471
        max_width = 341

        # only shrink if img is bigger than required
        if max_height < height or max_width < width:
            # get scaling factor
            scaling_factor = max_height / float(height)
            if max_width / float(width) < scaling_factor:
                scaling_factor = max_width / float(width)
            # resize image
            self.image = cv2.resize(self.image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()

        f__img = QImage(self.f_image, self.f_image.shape[1], self.f_image.shape[0], self.f_image.strides[0], qformat)
        self.orgImg.setPixmap(QPixmap.fromImage(img))
        self.orgImg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.filImg.setPixmap(QPixmap.fromImage(f__img))
        self.filImg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


app = QApplication(sys.argv)
window = Segmeter()
window.setWindowTitle("Segmeter")
window.show()
sys.exit(app.exec_())
