import glob
import os
import sys
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLineEdit
from PyQt5.uic import loadUi
from qtconsole.qt import QtCore, QtGui

from UtilOpencv import *
from lib.filter import *

import numpy as np


class Segmeter(QDialog):

    def __init__(self):
        self.currentInd = 0
        self.files = []
        self.filter_number = 1
        self.saved_dir = None
        self.base_color = (255, 255, 255)
        self.selected_tool = 0  # nothing
        try:
            super().__init__()
            loadUi('main.ui', self)
            self.image = None
            self.openBtn.clicked.connect(self.openFile)
            self.openBtnDir.clicked.connect(self.open_dir)
            self.nextBtn.clicked.connect(self.next_image)
            self.prvBtn.clicked.connect(self.prv_image)

            self.color_selected.setStyleSheet("background-color: white")
            self.blackBtn.setStyleSheet("background-color: black")
            self.blueBtn.setStyleSheet("background-color: blue")
            self.greenBtn.setStyleSheet("background-color: green")
            self.whiteBtn.setStyleSheet("background-color: white")
            self.redBtn.setStyleSheet("background-color: red")
            self.yellowkBtn.setStyleSheet("background-color: yellow")
            self.yellowkBtn.clicked.connect(self.set_yellow_color)
            self.redBtn.clicked.connect(self.set_red_color)
            self.blueBtn.clicked.connect(self.set_blue_color)
            self.whiteBtn.clicked.connect(self.set_white_color)
            self.greenBtn.clicked.connect(self.set_green_color)
            self.blackBtn.clicked.connect(self.set_black_color)

            self.saveBtn.clicked.connect(self.save_image)

            self.fillBtn.clicked.connect(self.fill_tool)
            self.pencilBtn.clicked.connect(self.pencil_tool)
            self.pencilSBtn.clicked.connect(self.pencil_s_tool)

            self.radBtnEG.clicked.connect(lambda: self.rd_btn_check(self.radBtnEG))
            self.radBtnNDI.clicked.connect(lambda: self.rd_btn_check(self.radBtnNDI))
            self.radBtnNon.clicked.connect(lambda: self.rd_btn_check(self.radBtnNon))

        except Exception as e:
            print(e)

    def rd_btn_check(self, rad):
        if rad.objectName() in "radBtnNon":
            self.filter_number = 0
            return
        elif rad.objectName() in "radBtnNDI":
            self.filter_number = 2
        elif rad.objectName() in "radBtnEG":
            self.filter_number = 1

    def save_image(self):
        file_name = QFileDialog.getSaveFileName(self, 'Dialog Save')
        self.file_name = file_name[0]
        print("Save name", file_name)
        cv2.imwrite(file_name[0], self.f_image)

    def fill_tool(self):
        self.selected_tool = 1

    def pencil_tool(self):
        self.selected_tool = 2
        pass

    def pencil_s_tool(self):
        self.selected_tool = 3
        pass

    def set_black_color(self):
        self.base_color = (0, 0, 0)
        self.color_selected.setStyleSheet("background-color: black")

    def set_blue_color(self):
        self.base_color = (255, 0, 0)
        self.color_selected.setStyleSheet("background-color: blue")

    def set_yellow_color(self):
        self.base_color = (0, 255, 255)
        self.color_selected.setStyleSheet("background-color: yellow")

    def set_green_color(self):
        self.base_color = (0, 255, 0)
        self.color_selected.setStyleSheet("background-color: green")

    def set_white_color(self):
        self.base_color = (255, 255, 255)
        self.color_selected.setStyleSheet("background-color: white")

    def set_red_color(self):
        self.base_color = (0, 0, 255)
        self.color_selected.setStyleSheet("background-color: red")

    def floodfill_(self):
        try:
            if not hasattr(self, 'f_image'):
                return
            if self.seed_pt == None:
                return

            flooded = self.f_image.copy()
            self.mask[:] = 0
            flags = self.connectivity
            if True:  # fixed_range
                flags |= cv2.FLOODFILL_FIXED_RANGE

            cv2.floodFill(flooded, self.mask, self.seed_pt, self.base_color, (20,) * 3, (20,) * 3, flags)
            self.f_image = flooded
            self.update_image()
        except Exception as e:
            print(e)

    def points_(self, isLeft):
        try:
            if not hasattr(self, 'f_image'):
                return
            if self.seed_pt == None:
                return

            flooded = self.f_image.copy()
            print("s22sss", self.seed_pt)

            if isLeft:
                cv2.circle(flooded, self.seed_pt, 1, self.base_color, -1)

            else:
                ss = flooded[self.seed_pt[1], self.seed_pt[0]]
                if not np.array_equal(ss, [0, 0, 0]):
                    cv2.circle(flooded, self.seed_pt, 1, self.base_color, -1)

            self.f_image = flooded
            self.update_image()
        except Exception as e:
            print(e)

    def points_original(self, isLeft):
        try:
            if not hasattr(self, 'f_image'):
                return
            if self.seed_pt == None:
                return
            print("sss", self.seed_pt)
            flooded = self.f_image.copy()
            if isLeft:
                cv2.circle(flooded, self.seed_pt, 2, self.base_color, -1)

            # else:
            #     ss = flooded[self.seed_pt[1], self.seed_pt[0]]
            #     if not np.array_equal(ss, [0, 0, 0]):
            #         cv2.circle(flooded, self.seed_pt, 1, self.base_color, -1)

            self.f_image = flooded
            self.update_image()
        except Exception as e:
            print(e)

    def update_image(self):
        try:
            fimg = QImage(self.f_image, self.f_image.shape[1], self.f_image.shape[0], self.f_image.strides[0],
                          get_image_format(self.f_image))
            fimg = fimg.rgbSwapped()
            self.f_view.setPixmap(QPixmap.fromImage(fimg))
            self.f_view.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self, "Open file")
        self.file_name = file_name[0]
        self.load_image()

    @pyqtSlot()
    def open_dir(self):
        try:
            # path of the Dir
            self.dir = QFileDialog.getExistingDirectory(self, "Open a folder", "*.jpg", QFileDialog.ShowDirsOnly)
            os.chdir(self.dir)
            types = ("*.jpg", "*.png")
            # create folder for seg images
            self.create_folder(self.dir)
            # name of the files
            for TYPE in types:
                self.files.extend(glob.glob(TYPE))
            if self.files != 0:
                self.load_image(current_image=True)
        except Exception as e:
            print(e)

    def create_folder(self, dir):
        try:
            s_dir = Path(dir)
            s_dir = Path(s_dir.parents[0], "segmenter", s_dir.parts[len(s_dir.parts) - 1])
            print(s_dir)
            if not os.path.exists(s_dir):
                os.makedirs(s_dir)
            self.saved_dir = s_dir
        except Exception as e:
            print(e)

    # Save the filtred Image
    def save_current_segment(self):
        if self.saved_dir is None:
            self.saved_dir = QFileDialog.getExistingDirectory(self, "Save an image", "*.jpg", QFileDialog.ShowDirsOnly)
        file_name = os.path.join(self.saved_dir, self.files[self.currentInd])
        print("Save name", file_name)
        cv2.imwrite(file_name, self.f_image)

    # Show the next image in the list and save the current one if there
    def next_image(self):
        try:
            self.save_current_segment()
            self.currentInd += 1
            if self.currentInd == len(self.files):
                self.currentInd = 0
                # self.initUI()
            self.load_image(current_image=True)
        except Exception as e:
            print(e)

    # Show the privese image in the list and save the current one if there
    def prv_image(self):
        try:
            self.save_current_segment()
            self.currentInd -= 1
            if self.currentInd == 0:
                self.currentInd = len(self.files) - 1
                # self.initUI()
            self.load_image(current_image=True)
        except Exception as e:
            print(e)

    # load read image and load it with selected filter
    def load_image(self, current_image=False):
        if current_image:
            self.file_name = self.dir + "/" + self.files[self.currentInd]

        if self.saved_dir is not None and Path(os.path.join(self.saved_dir, self.files[self.currentInd])).is_file():
            self.f_image = cv2.imread(os.path.join(self.saved_dir, self.files[self.currentInd]))
        else:
            self.f_image = None
        self.image = cv2.imread(self.file_name)
        self.display_image()

    # put image at widget
    @staticmethod
    def show_image(widget, img):
        widget.setPixmap(QPixmap.fromImage(
            QImage(img, img.shape[1], img.shape[0]
                   , img.strides[0], get_image_format(img)).rgbSwapped()))
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    # read image from attr and show them at UI
    def display_image(self):
        try:
            if self.f_image is None:
                self.f_image = filter_image(self.image, self.filter_number)

            height, width = self.image.shape[:2]
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
            self.show_image(self.orgImg, self.image)

            # Show filtered photo
            if self.filter_number == 1:
                if not self.f_image.dtype == 'uint8':
                    self.f_image = np.uint8(self.f_image)
                    self.f_image = covertGrayRGB(self.f_image)
            self.show_image(self.f_view, self.f_image)

            h, w = self.f_image.shape[:2]
            self.mask = np.zeros((h + 2, w + 2), np.uint8)
            self.connectivity = 4
            self.color = 0
        except Exception as e:
            print(e)

    # Add Filter on the events
    def eventFilter(self, source, event):
        if source == self.f_view:
            if event.type() == QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton and self.selected_tool == 2:
                    try:
                        point = QtCore.QPoint(event.pos())
                        x = int(point.x())
                        y = int(point.y())
                        self.seed_pt = x, y
                        self.points_(True)
                    except Exception as e:
                        print(e)
                elif event.buttons() == QtCore.Qt.RightButton and self.selected_tool == 2:
                    try:
                        point = QtCore.QPoint(event.pos())
                        x = int(point.x())
                        y = int(point.y())
                        self.seed_pt = x, y
                        self.points_(False)
                    except Exception as e:
                        print(e)
            elif event.type() == QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.LeftButton and self.selected_tool == 1:
                try:
                    point = QtCore.QPoint(event.pos())
                    x = int(point.x())
                    y = int(point.y())
                    self.seed_pt = x, y
                    print("ssss", source.objectName())
                    self.floodfill_()
                except Exception as e:
                    print(e)
        return False


app = QApplication(sys.argv)
window = Segmeter()
window.setWindowTitle("Segmeter")
window.show()
app.installEventFilter(window)
sys.exit(app.exec_())
