import os
import sys
import time

import image_process
import numpy as np
from cv2 import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QDesktopWidget, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QWidget)

from GUI import buttons, colors
from GUI.Fonts import fonts
from Utils import networktables_handler


def set_button_style(button: QPushButton):
    style = 'QPushButton {' \
            'color: ' + colors.primary_variant + ';' \
            'background-color: ' + colors.secondary + ';' \
            'border-style: outset; border-width: px;' \
            'border-radius: 15px; border-color: 121212; padding: 4px;' \
            '}' \
            'QPushButton::pressed {' \
            'background-color: ' + colors.secondary_bright + ';' \
            '}'
    button.setStyleSheet(style)
    button.setFont(fonts.roboto_bold(18))


class HomeScreen(QWidget):

    def __init__(self):
        super(HomeScreen, self).__init__()
        fonts.setup()
        icon_path = os.path.join(running_path(), 'icon.png')
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Calibration Program")
        self.setGeometry(300, 500, 1380, 820)

        title = QLabel("Calibration Program")
        title.setFont(fonts.open_sans_bold(48))
        title.setStyleSheet('color: ' + colors.primary + ';')  # rgb(48, 63, 159)
        title.setContentsMargins(0, 0, 0, 100)
        title.setAlignment(Qt.AlignCenter)

        self.thread = None

        # video streams:
        videos_layout: QHBoxLayout = QHBoxLayout()
        videos_layout.setContentsMargins(0, 0, 0, 100)

        self.create_video_labels()
        videos_layout.addWidget(self.video_1)
        videos_layout.addWidget(self.video_2)
        videos_layout.addWidget(self.video_3)

        # buttons:

        # first layout:
        buttons_layout_1: QHBoxLayout = QHBoxLayout()
        buttons_layout_1.setContentsMargins(400, 0, 400, 0)
        buttons_layout_1.setSpacing(50)

        self.start = QPushButton()
        self.start.setObjectName("start_button")
        self.start.setText("Start Calibrate")
        set_button_style(self.start)
        self.start.clicked.connect(lambda: buttons.calibrate(self))

        self.add_to = QPushButton()
        self.add_to.setObjectName("add_to_button")
        self.add_to.setText("Add To Calibrate")
        set_button_style(self.add_to)
        self.add_to.clicked.connect(lambda: buttons.add_to_calibrate(self))

        buttons_layout_1.addWidget(self.start)
        buttons_layout_1.addWidget(self.add_to)

        # second layout:
        buttons_layout_2: QHBoxLayout = QHBoxLayout()
        buttons_layout_2.setContentsMargins(420, 45, 420, 0)
        buttons_layout_2.setSpacing(100)

        self.save = QPushButton()
        self.save.setObjectName("save_button")
        self.save.setText("Save")
        set_button_style(self.save)
        self.save.clicked.connect(lambda: buttons.save(self))

        self.undo = QPushButton()
        self.undo.setObjectName("undo_button")
        self.undo.setText("Undo")
        set_button_style(self.undo)
        self.undo.clicked.connect(lambda: buttons.undo(self))

        self.discard = QPushButton()
        self.discard.setObjectName("discard_button")
        self.discard.setText("Discard")
        set_button_style(self.discard)
        self.discard.clicked.connect(lambda: buttons.discard(self))

        buttons_layout_2.addWidget(self.save)
        buttons_layout_2.addWidget(self.undo)
        buttons_layout_2.addWidget(self.discard)

        # error label:
        self.error = QLabel()
        self.error.setFont(fonts.roboto_bold(26))
        self.error.setStyleSheet('color: ' + colors.error + ';')  # rgb(48, 63, 159)
        self.error.setContentsMargins(0, 80, 0, 0)
        self.error.setAlignment(Qt.AlignCenter)

        # input label:
        self.input = QLineEdit()
        self.input.returnPressed.connect(lambda: self.disable_input())
        self.input.setText("0")
        self.input.setFont(fonts.roboto_bold(20))
        self.input.setStyleSheet('color: ' + colors.secondary + ';')  # rgb(48, 63, 159)
        self.input.setContentsMargins(0, 20, 0, 0)
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setVisible(False)
        self.input.setEnabled(False)

        # save input index label:
        self.save_input = QLineEdit()
        self.save_input.returnPressed.connect(lambda: networktables_handler.save_with_input(self))
        self.save_input.setText("0")
        self.save_input.setFont(fonts.roboto_bold(20))
        self.save_input.setStyleSheet('color: ' + colors.secondary + ';')  # rgb(48, 63, 159)
        self.save_input.setContentsMargins(0, 20, 0, 0)
        self.save_input.setAlignment(Qt.AlignCenter)
        self.save_input.setVisible(False)
        self.save_input.setEnabled(False)

        # layouts:
        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(title)
        v_box.addLayout(videos_layout)
        v_box.addLayout(buttons_layout_1)
        v_box.addLayout(buttons_layout_2)
        v_box.addWidget(self.error)
        v_box.addWidget(self.input)
        v_box.addWidget(self.save_input)
        v_box.addStretch()

        self.setLayout(v_box)
        self.setStyleSheet('background-color: ' + colors.background + ';')
        # widget = QWidget()
        # widget.setLayout(v_box)
        # widget.setStyleSheet("background-color: #1F2933;")  # rgb(18, 18, 18)
        # self.setCentralWidget(widget)

        self.show()
        self.center()

    def enable_input(self):
        self.input.setVisible(True)
        self.input.setEnabled(True)
        self.center()

    def check_input(self):
        text: str = self.input.text()
        if text.isnumeric():
            return 'number'
        return 'valid url'

    def disable_input(self):
        if not self.input.isEnabled():
            return
        camera_stream = self.input.text()
        input_status = self.check_input()
        if input_status == 'invalid':
            self.error.setText("Invalid URL.")
            return
        elif input_status == 'cant connect':
            self.error.setText("Can't connect to the given url.")
            return
        elif input_status == 'number':
            camera_stream = int(camera_stream)
        self.error.setText('')
        self.input.setVisible(False)
        self.input.setEnabled(False)
        self.start_stream(camera_stream)
        self.center()

    def disable_save_input(self):
        self.save_input.setVisible(False)
        self.save_input.setEnabled(False)
        self.center()

    def enable_save_input(self):
        self.save_input.setVisible(True)
        self.save_input.setEnabled(True)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        if not self.thread.stop:
            image, processed_image = image_process.process_image(cv_img)
            qt_img_1 = self.convert_cv_qt(image)
            if not self.thread.stop:
                self.video_1.setPixmap(qt_img_1)
                self.video_1.mousePressEvent = lambda event: image_process.mouse_pos(event=event, window=self,
                                                                                     cv_img=cv_img)
                qt_img_2 = self.convert_cv_qt(processed_image)
                self.video_2.setPixmap(qt_img_2)

    def update_third_stream(self, cv_img, masked=False):
        """Updates the image_label with a new opencv image"""
        if masked:
            image = cv_img
        else:
            _, image = image_process.process_image(cv_img)
        if image is not None:
            qt_img_2 = self.convert_cv_qt(image)
            if not self.thread.stop:
                self.video_3.setPixmap(qt_img_2)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
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

    def start_stream(self, camera_stream: str):
        if networktables_handler.connected_to_robot(self.error):
            networktables_handler.connect(self.error)
        # create the video capture thread
        self.thread = VideoThread(video_stream=self.video_1, camera_stream=camera_stream, window=self, update_image=self.update_image)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def stop_stream(self):
        # stop the video streams
        if type(self.thread) is VideoThread and self.thread.isRunning():
            self.thread.stop = True
            self.thread.requestInterruption()
            while self.thread.isRunning():
                pass
            self.video_1.mousePressEvent = None
            self.video_1.clear()
            self.video_2.clear()
            self.video_3.clear()
            self.video_1.setText("Video 1")
            self.video_2.setText("Video 2")
            self.video_3.setText("Video 3")
            self.error.setText("Dumped data!")
        else:
            self.error.setText("No data to dump!")
        self.center()


def running_path():
    application_path = None
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)
    return application_path


class VideoThread(QThread):

    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, video_stream, camera_stream, window, update_image):

        super().__init__()
        self.video_stream: QLabel = video_stream

        self.stop: bool = False

        self.camera_stream = camera_stream

        self.window: QWidget = window

    def run(self):
        self.video_stream.setText("Connecting...")
        capture = cv2.VideoCapture(self.camera_stream)
        self.window.center()
        while True:
            if self.stop:
                return
            ret, cv_img = capture.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            time.sleep(0.01)
