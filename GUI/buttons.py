import calibration
import vars
from networktables import NetworkTable, NetworkTables
from PyQt5.QtWidgets import QWidget
from Utils import networktables_handler


def calibrate(window: QWidget):
    # initialize the calibrate
    window.error.setText("Enter a camera stream url, or your camera port (default: 0).")
    window.enable_input()


def add_to_calibrate(window: QWidget):
    # add data to the calibrate memory
    if calibration.calibrate_amount:
        calibration.add_to_calibrate(window)
    else:
        window.error.setText("Click the left stream at least once to start calibrate")


def undo(window: QWidget):
    # delete the last data
    if calibration.calibrate_amount > 0:
        calibration.calibrate_amount -= 1
        calibration.data.pop()
        if calibration.calibrate_amount > 0:
            calibration.update_data()
        window.error.setText("Removed last data!")
    else:
        window.error.setText("Can't undo. No data found!")


def discard(window: QWidget):
    # stops the calibration program, and reset everything
    window.stop_stream()
    calibration.data = []
    calibration.calibrate_amount = 0
    vars.lower = vars.lower_default
    vars.upper = vars.upper_default


def save(window: QWidget):
    # saves the data and upload to network tables
    if networktables_handler.connected_to_robot(window.error, False):
        window.enable_save_input()
    else:
        window.error.setText("Can't connect!\nMax hsv: " + str(vars.upper) + ", Min HSV: " + str(vars.lower))
