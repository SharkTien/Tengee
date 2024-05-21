from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow


QUIT_FILE = "./ui_files/QuitFrame.ui"

class QuitFrame(QMainWindow):
    """
    Class QuitFrame: Using QMainWindow widgets from PyQt5 library
    This will make a menu buttons including "Quit" and "Deny Quit" when users create a quit event.
    """
    close_window = QtCore.pyqtSignal()
    reset_state = QtCore.pyqtSignal()

    def __init__(self):

        """
        __init__: inititate attributes and run methods for QuitFrame
        """
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(QUIT_FILE, self)
        self.init_UI()  
    
    def init_UI(self):
        """
        init_UI: set attributes for QuitFrame
        """
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.Accept.clicked.connect(self.AcceptQuit)
        self.Deny.clicked.connect(self.DenyQuit)

    def AcceptQuit(self):
        """
        AcceptQuit: Quit App
        """
        self.close_window.emit()

    def DenyQuit(self):
        """
        DenyQuit: Quit QuitFrame (continuing using App)
        """
        self.close()
        self.reset_state.emit()
