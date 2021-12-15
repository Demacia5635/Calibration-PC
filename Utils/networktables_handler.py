import threading
import urllib.request

from PyQt5.QtWidgets import QLabel
from networktables import NetworkTables


def connect(label: QLabel):
    cond = threading.Condition()
    notified = False
    NetworkTables.initialize(server='10.56.35.2')
    NetworkTables.addConnectionListener(lambda connected, info: connection_listener(connected, info, cond), immediateNotify=True)

    with cond:
        label.setText("Connecting...")
        if not notified:
            cond.wait()

    label.setText("Connected!")


def connection_listener(connected, info, cond):
    print(info, '; Connected=%s' % connected)
    with cond:
        cond.notify()


def connected_to_robot():
    url = '10.56.35.2'
    status_code = urllib.request.urlopen(url).getcode()
    return status_code == 200
