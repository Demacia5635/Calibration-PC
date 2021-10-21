import sys

import cv2

import GUI.homescreen

from PyQt5.QtWidgets import QApplication, QStackedWidget


def print_hi():
    app = QApplication(sys.argv)
    homescreen = GUI.homescreen.HomeScreen()
    widget = QStackedWidget()
    widget.addWidget(homescreen)
    widget.setFixedWidth(1200)
    widget.setFixedHeight(800)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


if __name__ == '__main__':
    print_hi()
