import glob
import os

from PyQt5 import QtGui
from PyQt5.QtGui import QFont


def setup():
    font_db = QtGui.QFontDatabase()
    for file in glob.glob('GUI/Fonts/*/*.ttf'):
        id = font_db.addApplicationFont(file)
        # print(font_db.applicationFontFamilies(id))


def open_sans(font_size):
    return QFont("Open Sans", font_size)


def open_sans_bold(font_size):
    font = open_sans(font_size)
    font.setBold(True)
    return font


def open_sans_semi_bold(font_size):
    return QFont("Open Sans SemiBold", font_size)


def roboto(font_size):
    return QFont("Roboto", font_size)


def roboto_bold(font_size):
    font = roboto(font_size)
    font.setBold(True)
    return font
