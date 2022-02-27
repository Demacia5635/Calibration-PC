import threading

import requests as requests
from PyQt5.QtWidgets import QLabel, QWidget
from networktables import NetworkTables, NetworkTable

dashboard: NetworkTable


def connect(label: QLabel):
    cond = threading.Condition()
    notified = False
    NetworkTables.initialize(server='10.56.35.2')
    NetworkTables.addConnectionListener(lambda connected, info: connection_listener(connected, info, cond),
                                        immediateNotify=True)

    with cond:
        label.setText("Connecting...")
        if not notified:
            cond.wait()

    label.setText("Connected!")
    global dashboard
    dashboard = NetworkTables.getTable("SmartDashboard")
    update_vars()


def connection_listener(connected, info, cond):
    print(info, '; Connected=%s' % connected)
    with cond:
        cond.notify()


def connected_to_robot(label: QLabel):
    try:
        label.setText("Searching for robot...")
        url = 'http://10.56.35.2'
        status_code = requests.get(url, timeout=(2, 1)).status_code
        print(status_code)
        return status_code == 200
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException):
        return False


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


def save_with_input(window: QWidget):
    input = window.save_input.text()
    connect(window.error)
    dashboard.putNumber("calibration-lower-h-" + input, vars.lower[0])
    dashboard.putNumber("calibration-lower-s-" + input, vars.lower[1])
    dashboard.putNumber("calibration-lower-v-" + input, vars.lower[2])
    dashboard.putNumber("calibration-upper-h-" + input, vars.upper[0])
    dashboard.putNumber("calibration-upper-s-" + input, vars.upper[1])
    dashboard.putNumber("calibration-upper-v-" + input, vars.upper[2])
    window.error.setText("Saved!")
    window.disable_save_input()
    window.center()