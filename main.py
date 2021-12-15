print("Loading...")
import sys

from PyQt5.QtWidgets import QApplication

import GUI.homescreen


def run_gui():
    print("Starting program...")
    app = QApplication(sys.argv)
    homescreen = GUI.homescreen.HomeScreen()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    run_gui()
