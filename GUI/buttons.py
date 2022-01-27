import calibration
import vars
from networktables import NetworkTable, NetworkTables
from PyQt5.QtWidgets import QWidget
from Utils import networktables_handler

dashboard: NetworkTable


def calibrate(window: QWidget):
    # initialize the calibrate
    if networktables_handler.connected_to_robot(window.error):
        global dashboard
        networktables_handler.connect(window.error)
        dashboard = NetworkTables.getTable("SmartDashboard")
        update_vars()
        window.start_stream()
    else:
        window.error.setText("Can't connect!")


def add_to_calibrate(window: QWidget):
    # add data to the calibrate memory
    if calibration.calibrate_amount:
        calibration.add_to_calibrate(window)
    else:
        window.error.setText("Click the ball in the left stream at least 3 times to start calibrate")


def trash(window: QWidget):
    # delete the last data
    if calibration.calibrate_amount > 0:
        calibration.calibrate_amount -= 1
        calibration.data = calibration.saved_data.copy()
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
    if calibration.calibrate_amount >= 5:
        if networktables_handler.connected_to_robot(window.error):
            networktables_handler.connect(window.error)
            dashboard.putNumber("calibration-lower-h", vars.lower[0])
            dashboard.putNumber("calibration-lower-s", vars.lower[1])
            dashboard.putNumber("calibration-lower-v", vars.lower[2])
            dashboard.putNumber("calibration-upper-h", vars.upper[0])
            dashboard.putNumber("calibration-upper-s", vars.upper[1])
            dashboard.putNumber("calibration-upper-v", vars.upper[2])
            window.error.setText("Saved!")
        else:
            window.error.setText("Can't connect!\nPlease connect to the robot and try again.")
    else:
        window.error.setText("You need to add calibration info at least 5 times before saving!")


def update_vars():
    vars.lower[0] = dashboard.getNumber("calibration-lower-h", vars.lower[0])
    vars.lower[1] = dashboard.getNumber("calibration-lower-s", vars.lower[1])
    vars.lower[2] = dashboard.getNumber("calibration-lower-v", vars.lower[2])
    vars.upper[0] = dashboard.getNumber("calibration-upper-h", vars.upper[0])
    vars.upper[1] = dashboard.getNumber("calibration-upper-s", vars.upper[1])
    vars.upper[2] = dashboard.getNumber("calibration-upper-v", vars.upper[2])
    vars.lower_default = vars.lower
    vars.upper_default = vars.upper
    vars.aov = dashboard.getNumber("camera-aov", vars.aov)
    vars.ball_radius = dashboard.getNumber("ball_radius", vars.ball_radius)
    vars.h_max_diff = dashboard.getNumber("calibration-h-diff", vars.h_max_diff)
    vars.s_max_diff = dashboard.getNumber("calibration-s-diff", vars.s_max_diff)
    vars.v_max_diff = dashboard.getNumber("calibration-v-diff", vars.v_max_diff)
