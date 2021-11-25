import time

from PyQt5.QtWidgets import QLabel, QWidget
from networktables import NetworkTables, NetworkTable

import calibration
import vars

dashboard: NetworkTable


def calibrate(window: QWidget):
    # initialize the calibrate
    if NetworkTables.initialize(server='10.56.36.2'):
        global dashboard
        dashboard = NetworkTables.getTable("SmartDashboard")
    else:
        window.start_stream()
        window.error.setText("Can't connect!")


def add_to_calibrate(window: QWidget):
    # add data to the calibrate memory
    if calibration.calibrate_amount >= 3:
        calibration.add_to_calibrate(window)
    else:
        window.error.setText("Click the ball in the left stream at least 3 times to start calibrate")


def trash(window: QWidget):
    # delete the last data
    calibration.data.pop()
    calibration.update_data()
    window.error.setText("Removed last data!")


def discard(window: QWidget):
    # stops the calibration program, and reset everything
    window.stop_stream()
    calibration.data = []
    calibration.calibrate_amount = 0
    vars.lower = vars.lower_default
    vars.upper = vars.upper_default


def save(window: QWidget):
    # saves the data and upload to network tables
    dashboard.putNumber("calibration-lower-h", vars.lower[0])
    dashboard.putNumber("calibration-lower-s", vars.lower[1])
    dashboard.putNumber("calibration-lower-v", vars.lower[2])
    dashboard.putNumber("calibration-upper-h", vars.upper[0])
    dashboard.putNumber("calibration-upper-s", vars.upper[1])
    dashboard.putNumber("calibration-upper-v", vars.upper[2])
    window.error.setText("Saved!")