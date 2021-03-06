import calibration
import vars
from networktables import NetworkTable, NetworkTables
from PyQt5.QtWidgets import QWidget, QPushButton

from Utils import networktables_handler


def calibrate(window: QWidget):
    # initialize the calibrate
    window.error.setText("Enter a camera stream url, or your camera port (default: 0).")
    window.enable_input()


def add_to_calibrate(window: QWidget):
    # add data to the calibrate memory
    if len(calibration.data) > 0:
        calibration.add_to_calibrate(window)
    else:
        window.error.setText("Click the left stream at least once to start calibrate")
    window.center()


def undo(window: QWidget):
    # delete the last data
    if len(calibration.data) > 0:
        calibration.data.pop()
        if len(calibration.data) > 0:
            calibration.update_data(window)
        else:
            window.update_sliders(vars.lower, vars.upper)
        window.error.setText("Removed last data!")
    else:
        window.error.setText("Can't undo. No data found!")
    window.center()


def discard(window: QWidget):
    # stops the calibration program, and reset everything
    window.stop_stream()
    calibration.data = []
    vars.lower = vars.lower_default
    vars.upper = vars.upper_default
    window.center()


def save(window: QWidget):
    # saves the data and upload to network tables
    if networktables_handler.connected_to_robot(window.error, False):
        window.enable_save_input()
    else:
        window.error.setText("Can't connect!\nMax hsv: " + str(vars.upper) + ", Min HSV: " + str(vars.lower))
    window.center()


def backup(window: QWidget):
    calibration.backups.append((vars.lower.copy(), vars.upper.copy()))
    window.error.setText("Data stored.")


def restore_backup(window: QWidget):
    if len(calibration.backups) > 0:
        min_hsv, max_hsv = calibration.backups.pop()
        window.update_sliders(min_hsv, max_hsv)
        window.error.setText("Backup restored.")
    else:
        window.error.setText("No available backups found!")
