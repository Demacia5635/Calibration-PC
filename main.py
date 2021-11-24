import sys

import GUI.homescreen

from PyQt5.QtWidgets import QApplication, QStackedWidget

from GUI.Fonts import fonts


def run_gui():
    print("test")
    app = QApplication(sys.argv)
    homescreen = GUI.homescreen.HomeScreen()
    # widget = QStackedWidget()
    # widget.addWidget(homescreen)
    # widget.setFixedWidth(1480)
    # widget.setFixedHeight(920)
    # widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


if __name__ == '__main__':
    run_gui()
