import sys
import glob, os

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QGraphicsScene, QLineEdit, QGraphicsView, QMessageBox
from PyQt5.uic import loadUi
from qtconsole.qt import QtCore
from lib.filter import *
from lib.UtilOpenCV import *


class Segmeter(QDialog):

    def __init__(self):
        try:
            super().__init__()
            loadUi('main.ui', self)
            self.image = None
            self.editPixInfo = QLineEdit(self)
            self.openBtn.clicked.connect(self.openFile)
            self.openBtnDir.clicked.connect(self.openDir)
            self.nextBtn.clicked.connect(self.nextImage)
            self.prvBtn.clicked.connect(self.prvImage)
            # self.editPixInfo.setReadOnly(True)
            self.scene = QGraphicsScene(self)
            self.f_view.setScene(self.scene)

            self.base_color = (255, 255, 255)
            self.redBtn.clicked.connect(self.set_red_color)
            self.blueBtn.clicked.connect(self.set_blue_color)

        except Exception as e:
            print(e)

    def set_blue_color(self):
        print("testBlue Btn")
        self.base_color = (0, 0, 255)

    def set_red_color(self):
        self.base_color = (255, 0, 0)

    def mousePressEvent(self, event):
        try:
            point = QtCore.QPoint(event.pos())
            x = int(point.x())
            y = int(point.y())
            print("X ", x, " XX", x - 530)
            print("Y ", y, " YY", y - 70)
            self.seed_pt = x - 530, y - 70
            if x >= 530 and x <= 1042:
                if y >= 70 and y <= 454:
                    self.floodfill_(x, y)
            # if self.imgQ.isUnderMouse():
            #     self.photoClicked.emit(QtCore.QPoint(event.pos()))
            super(Segmeter, self).mousePressEvent(event)
        except Exception as e:
            print(e)

    def floodfill_(self, x, y):
        try:
            if self.seed_pt == None:
                return
            color = (self.f_image[y - 70, x - 530])
            colorm = (self.mask[y - 70, x - 530])
            print("Base Color", color)
            print("Base Color M", colorm)
            flooded = self.f_image.copy()
            print(self.f_image.shape)
            print(self.mask.shape)
            self.mask[:] = 0
            # lo = cv2.getTrackbarPos('lo', 'floodfill')
            # hi = cv2.getTrackbarPos('hi', 'floodfill')
            flags = self.connectivity
            if True:  # fixed_range
                flags |= cv2.FLOODFILL_FIXED_RANGE

            print("Color new", self.base_color)
            cv2.floodFill(flooded, self.mask, self.seed_pt, self.base_color, (20,) * 3, (20,) * 3, flags)
            # cv2.circle(flooded, self.seed_pt, 2, self.color, -1)
            # cv2.imshow('floodfill', flooded)
            self.f_image = flooded
            self.update_Image()
        except Exception as e:
            print(e)

    def update_Image(self):
        try:
            scaled_image = Image.fromarray(self.f_image)
            img = ImageQt(scaled_image)
            pixMap = QPixmap.fromImage(img)
            self.scene = QGraphicsScene(self)
            self.f_view.setScene(self.scene)
            self.scene.addPixmap(pixMap)
            self.f_view.fitInView(QRectF(0, 0, self.f_image.shape[1], self.f_image.shape[0]), Qt.KeepAspectRatio)
            self.scene.update()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self, "Open file")
        self.file_name = file_name[0]
        self.loadImage()

    @pyqtSlot()
    def openDir(self):
        self.dir = QFileDialog.getExistingDirectory(self, "Open a folder", "*.jpg", QFileDialog.ShowDirsOnly)
        os.chdir(self.dir)
        types = ("*.jpg", "*.png")
        self.files = []
        for type in types:
            self.files.extend(glob.glob(type))
        self.currentInd = 0
        if (self.files) != 0:
            self.loadImage(current_image=True)

    def nextImage(self):
        try:
            self.currentInd += 1
            if self.currentInd == len(self.files):
                self.currentInd = 0
                # self.initUI()
            self.loadImage(current_image=True)
        except Exception as e:
            print(e)

    def prvImage(self):
        try:
            self.currentInd -= 1
            if self.currentInd == 0:
                self.currentInd = len(self.files - 1)
                # self.initUI()
            self.loadImage(current_image=True)
        except Exception as e:
            print(e)

    def loadImage(self, current_image=False):
        if current_image == True:
            self.file_name = self.dir + "/" + self.files[self.currentInd]
        self.image = cv2.imread(self.file_name)
        self.displayImage()

    def displayImage(self):
        try:
            self.scene.clear()
            qformat = QImage.Format_Indexed8
            if len(self.image.shape) == 3:
                if (self.image.shape[2]) == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888

            self.f_image = filter_image(self.image, 1)
            height, width = self.image.shape[:2]
            print("F_image shape", self.f_image.shape)
            max_height = 384
            max_width = 512

            # only shrink if img is bigger than required
            if max_height < height or max_width < width:
                # get scaling factor
                scaling_factor = max_height / float(height)
                if max_width / float(width) < scaling_factor:
                    scaling_factor = max_width / float(width)
                # resize image
                self.image = cv2.resize(self.image, None, fx=scaling_factor, fy=scaling_factor,
                                        interpolation=cv2.INTER_AREA)

            # Show original Photo
            img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
            img = img.rgbSwapped()
            self.orgImg.setPixmap(QPixmap.fromImage(img))
            self.orgImg.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            # self.f_image = np.uint8(self.f_image)
            self.f_image = covertGrayRGB(np.uint8(self.f_image))
            scaled_image = Image.fromarray(self.f_image)
            self.imgQ = ImageQt(scaled_image)
            pixMap = QPixmap.fromImage(self.imgQ)
            self.scene.addPixmap(pixMap)
            self.f_view.fitInView(QRectF(0, 0, self.f_image.shape[1], self.f_image.shape[0]), Qt.KeepAspectRatio)
            self.scene.update()

            h, w = self.f_image.shape[:2]
            self.mask = np.zeros((h + 2, w + 2), np.uint8)
            self.connectivity = 4
            self.color = 0
        except Exception as e:
            print(e)


app = QApplication(sys.argv)
window = Segmeter()
window.setWindowTitle("Segmeter")
window.show()
sys.exit(app.exec_())
