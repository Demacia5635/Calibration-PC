import time

import PyQt5.uic
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout


class HomeScreen(QDialog):

    def __init__(self):
        super(HomeScreen, self).__init__()
        PyQt5.uic.loadUi("homescreen.ui", self)

        self.videos_layout: QHBoxLayout = self.videos_layout
        # while self.videos_layout.count() > 1:
        #     item = self.videos_layout.itemAt(0)
        #     widget = item.widget()
        #     widget.deleteLater()
        # self.videos_layout.layout().deleteLater()

        self.display_width = 426
        self.display_height = 320

        # create the label that holds the image
        self.image_label = self.video_label_1 #QLabel(self)
        # self.image_label.setFont(QFont=QFont("Secular One", 40))
        self.image_label.resize(self.display_width, self.display_height)

        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        # vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        capture = cv2.VideoCapture("http://wpilibpi.local:8081")
        while True:
            ret, cv_img = capture.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            time.sleep(0.01)
