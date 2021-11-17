import time

import PyQt5.uic
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QMainWindow, QPushButton

import image_process
from GUI import buttons


class HomeScreen(QMainWindow):

    def __init__(self):
        super(HomeScreen, self).__init__()
        # PyQt5.uic.loadUi("homescreen.ui", self)

        title = QLabel("Calibration Program")
        title.setStyleSheet('font: 48pt "Secular One"; color: rgb(48, 63, 159);')
        title.setContentsMargins(0,0,0,100)
        title.setAlignment(Qt.AlignCenter)

        # video streams:
        videos_layout: QHBoxLayout = QHBoxLayout()
        videos_layout.setContentsMargins(0,0,0,100)

        self.create_video_labels()
        videos_layout.addWidget(self.video_1)
        videos_layout.addWidget(self.video_2)
        videos_layout.addWidget(self.video_3)

        # buttons:

        # first layout:
        buttons_layout_1: QHBoxLayout = QHBoxLayout()
        buttons_layout_1.setContentsMargins(0, 0, 0, 0)
        buttons_layout_1.setSpacing(50)

        self.start = QPushButton()
        self.start.setObjectName("start_button")
        self.start.setText("Start Calibrate")
        self.start.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One"; text-align: center')
        self.start.clicked.connect(buttons.calibrate)

        self.add_to = QPushButton()
        self.add_to.setObjectName("add_to_button")
        self.add_to.setText("Add To Calibrate")
        self.add_to.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One"; text-align: center')
        self.add_to.clicked.connect(buttons.add_to_calibrate)

        self.save = QPushButton()
        self.save.setObjectName("save_button")
        self.save.setText("Save")
        self.save.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One"; text-align: center')
        self.save.clicked.connect(buttons.save)

        buttons_layout_1.addWidget(self.start)
        buttons_layout_1.addWidget(self.add_to)
        buttons_layout_1.addWidget(self.save)

        # second layout:
        buttons_layout_2: QHBoxLayout = QHBoxLayout()
        buttons_layout_2.setContentsMargins(0, 45, 0, 0)
        buttons_layout_2.setSpacing(100)

        self.trash = QPushButton()
        self.trash.setObjectName("trash_button")
        self.trash.setText("Trash")
        self.trash.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One"; text-align: center')
        self.trash.clicked.connect(buttons.trash)

        self.discard = QPushButton()
        self.discard.setObjectName("discard_button")
        self.discard.setText("Discard")
        self.discard.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One"; text-align: center')
        self.discard.clicked.connect(buttons.discard)

        buttons_layout_2.addWidget(self.trash)
        buttons_layout_2.addWidget(self.discard)

        # layouts:
        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(title)
        v_box.addLayout(videos_layout)
        v_box.addLayout(buttons_layout_1)
        v_box.addLayout(buttons_layout_2)
        v_box.addStretch()

        widget = QWidget()
        widget.setLayout(v_box)
        widget.setStyleSheet("background-color: rgb(18, 18, 18);")
        self.setCentralWidget(widget)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        image_1, image_2 = image_process.process_image(cv_img)
        qt_img_1 = self.convert_cv_qt(image_1)
        self.video_1.setPixmap(qt_img_1)
        qt_img_2 = self.convert_cv_qt(image_2)
        self.video_2.setPixmap(qt_img_2)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def create_video_labels(self):
        self.video_1 = QLabel("Video 1")
        self.video_1.setAlignment(Qt.AlignCenter)
        self.video_1.setObjectName("Video1")
        self.video_1.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One";')

        self.video_2 = QLabel("Video 2")
        self.video_2.setAlignment(Qt.AlignCenter)
        self.video_2.setObjectName("Video2")
        self.video_2.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One";')

        self.video_3 = QLabel("Video 3")
        self.video_3.setAlignment(Qt.AlignCenter)
        self.video_3.setObjectName("Video3")
        self.video_3.setStyleSheet('color: rgb(255, 0, 0); font: 20pt "Secular One";')

        self.display_width = self.video_1.size().width()
        self.display_height = 320


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        capture = cv2.VideoCapture("http://wpilibpi.local:8081")
        while True:
            ret, cv_img = capture.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            time.sleep(0.01)
