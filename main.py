import glob
import os
import sys
from datetime import time
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLineEdit
from PyQt5.uic import loadUi
from qtconsole.qt import QtCore, QtGui

from UtilOpencv import *
from lib.filter import *
import json
import numpy as np

from multiprocessing import Process, Queue
# import ui

class Segmeter(QDialog):

    def __init__(self):
        self.currentInd = 0
        self.files = []
        self.filter_number = 1
        self.actionList = []
        self.saved_dir = None
        self.base_color = (255, 255, 255)
        self.selected_tool = 0  # nothing
        self.image = None
        self.custom_hsv_filters = []
        self.f_image = None
        self.file_name = None
        self.stem_points = []
        self.dir = None

        try:
            super().__init__()
            loadUi('main.ui', self)
            # ui.load_ui(self)
            # the width of the view area is 640
            # the height of the view area is 512
            self.undoBtn.clicked.connect(self.undo)
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
            self.cleanBtn.clicked.connect(self.clean_image)
            self.cleanBtn_2.clicked.connect(self.clean_image_2)

            self.radBtnNon.filter_number = 0
            self.radBtnNon.toggled.connect(self.rd_btn_check)
            self.radBtnEG.filter_number = 1
            self.radBtnEG.toggled.connect(self.rd_btn_check)
            self.radBtnNDI.filter_number = 2
            self.radBtnNDI.toggled.connect(self.rd_btn_check)
            self.radBtnCive.filter_number = 3
            self.radBtnCive.toggled.connect(self.rd_btn_check)
            self.radBtnExred.filter_number = 4
            self.radBtnExred.toggled.connect(self.rd_btn_check)
            self.radBtnNdi.filter_number = 5
            self.radBtnNdi.toggled.connect(self.rd_btn_check)
            self.radBtnHsv.filter_number = 6
            self.radBtnHsv.toggled.connect(self.rd_btn_check)
            self.radBtnEdges.filter_number = 7
            self.radBtnEdges.toggled.connect(self.rd_btn_check)
            self.radBtnLaplacian.filter_number = 8
            self.radBtnLaplacian.toggled.connect(self.rd_btn_check)
            self.radBtnCustom.filter_number = 9
            self.radBtnCustom.toggled.connect(self.rd_btn_check)

            self.radBtnNon.setChecked(True)

            self.hue_min_slider.valueChanged.connect(self.value_change)
            self.hue_max_slider.valueChanged.connect(self.value_change)
            self.saturation_min_slider.valueChanged.connect(self.value_change)
            self.saturation_max_slider.valueChanged.connect(self.value_change)
            self.value_min_slider.valueChanged.connect(self.value_change)
            self.value_max_slider.valueChanged.connect(self.value_change)

            self.add_custom_btn.clicked.connect(self.add_custom_thresh)
            self.remove_custom_btn.clicked.connect(self.remove_custom_thresh)

            self.dilation_btn.clicked.connect(self.dilation_clicked)
            self.erosion_btn.clicked.connect(self.erosion_clicked)
            self.opening_btn.clicked.connect(self.opening_clicked)

            self.kernel_ln_edit.setValidator(QIntValidator())
            self.kernel_ln_edit.setMaxLength(2)
            self.kernel_ln_edit.setAlignment(Qt.AlignRight)
            self.kernel_ln_edit.setFont(QFont("Arial", 20))

            self.exgr_slider.valueChanged.connect(self.value_change)

            self.deleteBtn.clicked.connect(self.delete_img)

            self.stem_btn.clicked.connect(self.stem_btn_clicked)
            self.remove_stems_btn.clicked.connect(self.remove_stems_btn_clicked)
            self.openBagFileBtn.clicked.connect(self.open_bag_file_btn_clicked)
        except Exception as e:
            print(e)

    def process_bag_file(self, bag_path, queue):
        """ process bag file and run command line. Don't return anything."""
        is_success = False
        # do code here
        # set status code here
        # set is_success here
        queue.put(is_success)

    def open_bag_file_btn_clicked(self):
        """open dialog box, open bag file, process bag file, store in data-folder of annotation tool, load the data into annotation tool"""
        bag_path = "blah"
        queue = Queue()
        self.bag_status_label.setText("Working!")
        p = Process(target=self.process_bag_file, args=(bag_path, queue))
        p.start()
        is_success = queue.get()
        p.join()
        self.bag_status_label.setText("Sleeping")

    def remove_stems_btn_clicked(self):
        self.stem_points = []
        self.display_image(change_filter=False)

    def delete_img(self):
        if len(self.files) > 0 and self.currentInd < len(self.files):
            path, file_name = os.path.split(self.files[self.currentInd])
            self.stem_points = []
            if os.path.isfile(self.files[self.currentInd]):
                os.remove(self.files[self.currentInd])
            self.filename_lbl.setText("")
            json_file = os.path.join(self.saved_dir, os.path.splitext(file_name)[0] + ".json")
            if os.path.isfile(json_file):
                os.remove(json_file)
            segmented_file = os.path.join(self.saved_dir, os.path.splitext(file_name)[0] + ".png")
            if os.path.isfile(segmented_file):
                os.remove(segmented_file)
            self.image = None
            self.f_image = None
            self.file_name = None
            # remove file_name from self.files
            self.files.pop(self.currentInd)
            if self.currentInd == len(self.files):
                self.currentInd = 0
            self.f_view.setText("Empty")
            self.orgImg.setText("Empty")
            self.actionList = []

            # if length of files is > 0 then open next file else show empty
            self.load_stem_points()
            self.load_image(current_image=True)

    def stem_btn_clicked(self):
        self.selected_tool = 5

    def erosion_clicked(self):
        if self.f_image is not None:
            kernel = np.ones((int(self.kernel_ln_edit.text()), int(self.kernel_ln_edit.text())), np.uint8)
            self.f_image = cv2.erode(self.f_image, kernel, iterations=1)
            self.display_image()

    def dilation_clicked(self):
        if self.f_image is not None:
            kernel = np.ones((int(self.kernel_ln_edit.text()), int(self.kernel_ln_edit.text())), np.uint8)
            self.f_image = cv2.dilate(self.f_image, kernel, iterations=1)
            self.display_image()

    def opening_clicked(self):
        if self.f_image is not None:
            kernel = np.ones((int(self.kernel_ln_edit.text()), int(self.kernel_ln_edit.text())), np.uint8)
            self.f_image = cv2.morphologyEx(self.f_image, cv2.MORPH_OPEN, kernel)
            self.display_image()

    def remove_custom_thresh(self):
        if self.custom_list.currentRow() >= 0:
            self.custom_hsv_filters.pop(self.custom_list.currentRow())
            item = self.custom_list.takeItem(self.custom_list.currentRow())
            item = None
        self.radBtnNon.filter_number = 0
        self.radBtnNon.setChecked(True)
        self.display_image(change_filter=True)

    def add_custom_thresh(self):
        self.custom_hsv_filters.append(((self.hue_min_slider.value(), self.hue_max_slider.value()),
                                        (self.saturation_min_slider.value(), self.saturation_max_slider.value()),
                                        (self.value_min_slider.value(), self.value_max_slider.value())))
        self.custom_list.addItem(((self.hue_min_slider.value(), self.hue_max_slider.value()),
                                  (self.saturation_min_slider.value(), self.saturation_max_slider.value()),
                                  (self.value_min_slider.value(), self.value_max_slider.value())).__str__())
        self.radBtnNon.filter_number = 0
        self.radBtnNon.setChecked(True)
        self.display_image(change_filter=True)

    def value_change(self):
        slider = self.sender()
        if slider == self.hue_min_slider:
            if self.hue_max_slider.value() <= self.hue_min_slider.value():
                self.hue_min_slider.setValue(self.hue_max_slider.value() - 1)
        if slider == self.hue_max_slider:
            if self.hue_max_slider.value() <= self.hue_min_slider.value():
                self.hue_max_slider.setValue(self.hue_max_slider.value() + 1)

        if slider == self.saturation_min_slider:
            if self.saturation_max_slider.value() <= self.saturation_min_slider.value():
                self.saturation_min_slider.setValue(self.saturation_max_slider.value() - 1)
        if slider == self.saturation_max_slider:
            if self.saturation_max_slider.value() <= self.saturation_min_slider.value():
                self.saturation_max_slider.setValue(self.saturation_max_slider.value() + 1)

        if slider == self.value_min_slider:
            if self.value_max_slider.value() <= self.value_min_slider.value():
                self.value_min_slider.setValue(self.value_max_slider.value() - 1)
        if slider == self.value_max_slider:
            if self.value_max_slider.value() <= self.value_min_slider.value():
                self.value_max_slider.setValue(self.value_max_slider.value() + 1)

        self.display_image(change_filter=True)

    def rd_btn_check(self):
        rd_btn = self.sender()
        if rd_btn.isChecked():
            self.filter_number = rd_btn.filter_number
            self.display_image(change_filter=True)
        pass

    def save_image(self):
        self.save_stem_points()
        self.save_current_segment()

    def undo(self):
        print("undoing", len(self.actionList))
        try:
            self.f_image = self.actionList.pop()
            self.update_f_image()
        except IndexError:
            print("Nothing to undo")

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
            self.actionList.append(self.f_image)

            self.mask[:] = 0
            flags = self.connectivity
            if True:  # fixed_range
                flags |= cv2.FLOODFILL_FIXED_RANGE

            cv2.floodFill(flooded, self.mask, self.seed_pt, self.base_color, (20,) * 3, (20,) * 3, flags)
            self.f_image = flooded
            self.update_f_image()
        except Exception as e:
            print(e)

    def points_(self, isLeft):
        try:
            if not hasattr(self, 'f_image'):
                return
            if self.seed_pt == None:
                return
            self.actionList.append(self.f_image)
            flooded = self.f_image.copy()

            point_size = self.horizontalSlider.value()

            if isLeft:
                cv2.circle(flooded, self.seed_pt, point_size, self.base_color, -1)

            else:
                ss = flooded[self.seed_pt[1], self.seed_pt[0]]
                if not np.array_equal(ss, [0, 0, 0]):
                    cv2.circle(flooded, self.seed_pt, point_size, self.base_color, -1)

            self.f_image = flooded
            self.update_f_image()
        except Exception as e:
            print(e)

    def points_original(self, isLeft):
        try:
            if not hasattr(self, 'f_image'):
                return
            if self.seed_pt == None:
                return
            point_size = self.horizontalSlider.value()
            self.actionList.append(self.f_image)
            flooded = self.f_image.copy()
            if isLeft:
                cv2.circle(flooded, self.seed_pt, point_size, self.base_color, -1)
                cv2.circle(self.image, self.seed_pt, point_size, self.base_color, -1)

            else:
                if not np.array_equal(flooded[self.seed_pt[1], self.seed_pt[0]], [0, 0, 0]):
                    cv2.circle(flooded, self.seed_pt, point_size, self.base_color, -1)
                    cv2.circle(self.image, self.seed_pt, point_size, self.base_color, -1)

            self.f_image = flooded
            self.update_f_image()
            self.update_org_image()
        except Exception as e:
            print(e)

    def update_f_image(self):
        try:
            self.show_image(self.f_view, self.f_image)
        except Exception as e:
            print(e)

    def update_org_image(self):
        try:
            # Show original Photo
            self.show_image(self.orgImg, self.image)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def openFile(self):
        file_name_tuple = QFileDialog.getOpenFileName(self, "Open file")
        if file_name_tuple is not None and file_name_tuple[0] != '':
            self.file_name = file_name_tuple[0]
            path = os.path.dirname(self.file_name)
            self.dir = path
            self.create_folder(path)

            self.files = [self.file_name]
            self.currentInd = 0
            self.load_stem_points()
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
                self.currentInd = 0
                self.load_stem_points()
                self.load_image(current_image=True)
        except Exception as e:
            print(e)

    def create_folder(self, dir):
        try:
            s_dir = os.path.join(dir, "segmented_imgs")
            if not os.path.exists(s_dir):
                os.makedirs(s_dir)
            self.saved_dir = s_dir
        except Exception as e:
            print(e)

    # Save the filtred Image
    def save_current_segment(self):
        if len(self.files) <= 0:
            return
        if self.saved_dir is None:
            self.saved_dir = QFileDialog.getExistingDirectory(self, "Save an image", "*.png", QFileDialog.ShowDirsOnly)
        file_name = os.path.join(self.saved_dir, os.path.splitext(self.files[self.currentInd])[0] + ".png")
        cv2.imwrite(file_name, self.f_image)

    def save_stem_points(self):
        if len(self.stem_points) > 0:
            with open(os.path.join(self.saved_dir, os.path.splitext(self.files[self.currentInd])[0] + ".json"),
                      'w') as outfile:
                json.dump(self.stem_points, outfile)

    def load_stem_points(self):
        self.stem_points = []
        try:
            if len(self.files) > 0:
                with open(
                        os.path.join(self.saved_dir, os.path.splitext(self.files[self.currentInd])[0] + ".json")) as f:
                    self.stem_points = json.load(f)
                    self.stem_points = [tuple(x) for x in self.stem_points]
        except FileNotFoundError as e:
            pass

    def next_image(self):
        """ Show the next image in the list and save the current one if there """
        try:
            self.save_stem_points()
            self.save_current_segment()
            self.currentInd += 1
            if self.currentInd == len(self.files):
                self.currentInd = 0
                # self.initUI()
            self.load_stem_points()
            self.load_image(current_image=True)
            self.actionList = []
        except Exception as e:
            print(e)

    # Show the previous image in the list and save the current one if there
    def prv_image(self):
        try:
            self.save_stem_points()
            self.save_current_segment()
            self.currentInd -= 1
            if self.currentInd == -1:
                self.currentInd = len(self.files) - 1
                # self.initUI()
            self.load_stem_points()
            self.load_image(current_image=True)
            self.actionList = []
        except Exception as e:
            print(e)

    # load read image and load it with selected filter
    def load_image(self, current_image=False):
        if len(self.files) <= 0:
            return
        if current_image:
            self.file_name = self.dir + "/" + self.files[self.currentInd]

        save_path = os.path.join(self.saved_dir, os.path.splitext(self.files[self.currentInd])[0] + ".png")
        if self.saved_dir is not None and Path(save_path).is_file():
            self.f_image = cv2.imread(os.path.join(self.saved_dir, os.path.splitext(self.files[self.currentInd])[0] + ".png"))
        else:
            self.f_image = None
        self.filename_lbl.setText(self.files[self.currentInd])
        self.image = cv2.imread(self.file_name)
        self.display_image()

    # put image at widget
    def show_image(self, widget, img):
        temp_img = img.copy()
        for point in self.stem_points:
            cv2.circle(temp_img, point, 3, (233, 20, 100), -1)
        widget.setPixmap(QPixmap.fromImage(
            QImage(temp_img, temp_img.shape[1], temp_img.shape[0]
                   , temp_img.strides[0], get_image_format(temp_img)).rgbSwapped()))
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    # put image at widget
    @staticmethod
    def show_image_(widget, img):
        img = np.array(img).astype(np.uint8)
        widget.setPixmap(QPixmap.fromImage(
            QImage(img, img.shape[1], img.shape[0]
                   , img.strides[0], get_image_format(img)).rgbSwapped()))
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    # read image from attr and show them at UI
    def display_image(self, change_filter=False):
        try:

            if self.f_image is None or change_filter:
                self.f_image = filter_image(self.image, self.filter_number, self)
            height, width = self.image.shape[:2]

            # resize to see how it works with kernels
            # rgb_img = ad.resize(rgb_img, [proper_h, proper_w])

            # max_height = 512
            # max_width = 640

            # old way
            # only shrink if img is bigger than required
            # if max_height < height or max_width < width:
            #     # get scaling factor
            #     scaling_factor = max_height / float(height)
            #     if max_width / float(width) < scaling_factor:
            #         scaling_factor = max_width / float(width)
            #     # resize image
            #     self.image = cv2.resize(self.image, None, fx=scaling_factor, fy=scaling_factor,
            #                             interpolation=cv2.INTER_AREA)

            # another way
            # if width > height:
            #     scaling_factor = max_width/width
            #
            # else:
            #     scaling_factor = max_height/height
            # self.image = cv2.resize(self.image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

            # new way
            smallest_edge = 600
            if width > height:
                new_height = smallest_edge
                scaling_factor = new_height / height
                new_width = int(width * scaling_factor)
            else:
                new_width = smallest_edge
                scaling_factor = new_width / width
                new_height = int(height * scaling_factor)
            self.image = cv2.resize(self.image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            self.orgImg.setGeometry(
                QtCore.QRect(self.orgImg.x(), self.orgImg.y(), new_width, new_height))  # (x, y, height, width)
            self.f_image = cv2.resize(self.f_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            self.f_view.setGeometry(
                QtCore.QRect(self.f_view.x(), self.f_view.y(), new_width, new_height))  # (x, y, height, width)

            min_screen_width = 1700
            # if (smallest_edge*2) + 150 < min_screen_width:
            #     screen_width = min_screen_width
            # else:
            #     screen_width = (smallest_edge*2) + 150
            # self.setGeometry(
            #     QtCore.QRect(self.x(), self.y(), screen_width, self.height())
            # )

            # win.resize(new_width*2 + 100, new_height*2 + 100)

            # Show original Photo
            self.show_image(self.orgImg, self.image)

            # Show filtered photo
            if self.f_image.ndim == 2:
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

    def clean_image(self):
        ss = np.where((self.f_image == [255, 255, 255]).all(axis=2))
        self.f_image[ss] = [0, 0, 0]
        self.update_f_image()

    def clean_image_2(self):
        lower_white = np.array([250, 250, 250], dtype="uint8")
        upper_white = np.array([255, 255, 255], dtype="uint8")
        mask = cv2.inRange(self.f_image, lower_white, upper_white)
        ss = np.where(np.isin(mask, 255))
        self.f_image[ss] = [0, 0, 0]  # clear White color

        lower_white = np.array([0, 0, 0], dtype="uint8")
        upper_white = np.array([125, 125, 125], dtype="uint8")
        mask = cv2.inRange(self.f_image, lower_white, upper_white)
        ss = np.where(np.isin(mask, 255))
        self.f_image[ss] = [0, 0, 0]  # clear White color

        ssd = np.where((self.f_image == [255, 0, 0]).all(axis=2))
        self.f_image[ssd] = [0, 0, 0]  # clear Blue color
        self.update_f_image()

    def zoom_original(self, x, y):
        try:

            zoomed_img = crop(self.image, x, y)
            if zoomed_img.size != 0:

                zoomed_img = Zoom(zoomed_img, 2)

                if zoomed_img is not None:
                    self.show_image_(self.zoomImg, zoomed_img)
        except Exception as e:
            print(e)

    def clean_images(self):
        if len(self.actionList) >= 1000:
            print("clean list")
            self.actionList = self.actionList[:1000]

    # Add Filter on the events
    def eventFilter(self, source, event):
        try:
            if source == self.f_view:
                if event.type() == QEvent.MouseMove:
                    point = QtCore.QPoint(event.pos())
                    x = int(point.x())
                    y = int(point.y())
                    self.seed_pt = x, y
                    if event.buttons() == QtCore.Qt.LeftButton and self.selected_tool == 2:
                        self.points_(True)
                        self.clean_images()
                    elif event.buttons() == QtCore.Qt.RightButton and self.selected_tool == 2:
                        self.points_(False)
                        self.clean_images()
                elif event.type() == QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.LeftButton and self.selected_tool == 1:
                    self.actionList = self.actionList[:500]
                    self.floodfill_()
                    self.actionList.append(self.f_image)
                elif event.type() == QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.LeftButton and self.selected_tool == 5:
                    point = QtCore.QPoint(event.pos())
                    x = int(point.x())
                    y = int(point.y())
                    self.stem_points.append((x, y))
                    self.update_f_image()
            elif source == self.orgImg:
                if event.type() == QEvent.MouseMove:
                    point = QtCore.QPoint(event.pos())
                    x = int(point.x())
                    y = int(point.y())
                    self.seed_pt = x, y
                    if not self.image is None:
                        self.zoom_original(x, y)
                    if event.buttons() == QtCore.Qt.LeftButton and self.selected_tool == 3:
                        self.points_original(True)
                        self.clean_images()
                    elif event.buttons() == QtCore.Qt.RightButton and self.selected_tool == 3:
                        self.points_original(False)
                        self.clean_images()
            return False
        except Exception as e:
            print(e)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Segmeter()
    window.setWindowTitle("Segmeter")
    window.show()
    app.installEventFilter(window)
    sys.exit(app.exec_())
