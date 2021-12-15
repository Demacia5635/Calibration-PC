import time

import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton

import image_process
from GUI import buttons, colors
from GUI.Fonts import fonts


class HomeScreen(QWidget):

    def __init__(self):
        super(HomeScreen, self).__init__()
        fonts.setup()
        self.setWindowTitle("Calibration Program")
        self.setGeometry(300, 150, 1380, 820)

        title = QLabel("Calibration Program")
        title.setFont(fonts.open_sans_bold(48))
        title.setStyleSheet('color: ' + colors.primary + ';')  # rgb(48, 63, 159)
        title.setContentsMargins(0, 0, 0, 100)
        title.setAlignment(Qt.AlignCenter)

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
        self.set_button_style(self.start)
        self.start.clicked.connect(lambda: buttons.calibrate(self))

        self.add_to = QPushButton()
        self.add_to.setObjectName("add_to_button")
        self.add_to.setText("Add To Calibrate")
        self.set_button_style(self.add_to)
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
        self.set_button_style(self.save)
        self.save.clicked.connect(lambda: buttons.save(self))

        self.trash = QPushButton()
        self.trash.setObjectName("trash_button")
        self.trash.setText("Trash")
        self.set_button_style(self.trash)
        self.trash.clicked.connect(lambda: buttons.trash(self))

        self.discard = QPushButton()
        self.discard.setObjectName("discard_button")
        self.discard.setText("Discard")
        self.set_button_style(self.discard)
        self.discard.clicked.connect(lambda: buttons.discard(self))

        buttons_layout_2.addWidget(self.save)
        buttons_layout_2.addWidget(self.trash)
        buttons_layout_2.addWidget(self.discard)

        # error label:

        self.error = QLabel()
        self.error.setFont(fonts.roboto_bold(26))
        self.error.setStyleSheet('color: ' + colors.error + ';')  # rgb(48, 63, 159)
        self.error.setContentsMargins(0, 100, 0, 0)
        self.error.setAlignment(Qt.AlignCenter)

        # layouts:
        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(title)
        v_box.addLayout(videos_layout)
        v_box.addLayout(buttons_layout_1)
        v_box.addLayout(buttons_layout_2)
        v_box.addWidget(self.error)
        v_box.addStretch()

        self.setLayout(v_box)
        self.setStyleSheet('background-color: ' + colors.background + ';')
        # widget = QWidget()
        # widget.setLayout(v_box)
        # widget.setStyleSheet("background-color: #1F2933;")  # rgb(18, 18, 18)
        # self.setCentralWidget(widget)

        self.show()

    def set_button_style(self, button: QPushButton):
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

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        image, processed_image = image_process.process_image(cv_img)
        qt_img_1 = self.convert_cv_qt(image)
        self.video_1.setPixmap(qt_img_1)
        self.video_1.mousePressEvent = lambda event: image_process.mouse_pos(event=event, window=self)
        qt_img_2 = self.convert_cv_qt(processed_image)
        self.video_2.setPixmap(qt_img_2)

    def update_third_stream(self, cv_img):
        """Updates the image_label with a new opencv image"""
        _, image = image_process.process_image(cv_img)
        qt_img_2 = self.convert_cv_qt(image)
        self.video_3.setPixmap(qt_img_2)

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

    def start_stream(self):
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.video_1 = self.video_1
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def stop_stream(self):
        # stop the video streams
        if type(self.thread) is VideoThread:
            self.thread.stop = True
            self.thread.requestInterruption()
            while self.thread.isRunning():
                pass
            time.sleep(1)
        self.video_1.clear()
        self.video_1.mousePressEvent = None
        self.video_1.setText("Video 1")
        self.video_2.setText("Video 2")
        self.video_3.setText("Video 3")
        self.error.setText("Dumped data!")


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    video_1: QLabel

    stop: bool = False

    def run(self):
        self.video_1.setText("Connecting...")
        capture = cv2.VideoCapture('http://10.56.35.12:8081')
        while True:
            if self.stop:
                return
            ret, cv_img = capture.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            time.sleep(0.01)
