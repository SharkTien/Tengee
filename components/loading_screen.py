import time

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow

UI_PATH = "./ui_files/Loading_Screen.ui"
from utils.config import SCREEN_HEIGHT, SCREEN_WIDTH

class LoadingScreen(QMainWindow):
    """
    class LoadingScreen:
    method:

        __init__(version)

        initUI(version)

    """
    counter = 0
    switch_window = QtCore.pyqtSignal(object)

    def __init__(self, version): 
        """
            __init__(version): initiate attributes for Loading Screen
        """
        self.version = version

        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_PATH, self)
        self.initUI()
        UIFunction(self)

    def initUI(self):
        """
            initUI: inititate and move window to center of screen, then initiate attributes     
        """
        self.move(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.frame.hide()


class UIFunction(LoadingScreen):
    """
        class UIFunction for LoadingScreen including methods processing progress bar.
        Include version, 
    """
    pg = None

    def __init__(self, ui):
        """
            __init__ initiate methods and attributes for UIFunction
        """
        self.update_version(ui)
        ui.timer = QtCore.QTimer()
        ui.timer.timeout.connect(lambda: self.progress(ui))
        ui.timer.start(20) 
    

    def update_version(self, ui):
        """
        update_version(ui): update the version of the entire Uis
        """
        ui.versionLabel.setText(
            f'<html><head/><body><p align="right"><span style=" font-size:14pt; color:#ffffff;">v{ui.version}</span></p></body></html>'
        )

    def delay(self, point, wait):
        """
            delay(point, wait): This affects to progress function, if count == /point then time.sleep(/wait)
        """
        if self.counter == point:
            time.sleep(wait)

    def progress(self, ui):
        """
            progress(ui): the preprocessing data, ui,... before running the Home Window and functions...
            This include increasing value of progressBar in range 0 to 100
        """
        ui.progressBar.setValue(self.counter)
        if self.counter >= 100:
            ui.timer.stop()
            ui.switch_window.emit(self.pg)

        if self.counter == 6:
            ui.timer.singleShot(
                1500, lambda: ui.Loading_label.setText("kiểm tra kết nối ...")
            )
                
        if self.counter == 14:
            ui.timer.singleShot(2905, lambda: ui.Loading_label.setText("khởi động ..."))
            
        if self.counter == 50:
            ui.Loading_label.setText("đang kết nối...")
        if self.counter == 73:
            time.sleep(3)
                    
        self.delay(99, 1)
        self.counter += 1
         