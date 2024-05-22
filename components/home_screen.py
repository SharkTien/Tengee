from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from utils.config import SCREEN_HEIGHT, SCREEN_WIDTH


UI_MAIN_PATH = "./ui_files/Home_gui.ui"
DATA_USERS_PATH = "./data/users/data_users.dat"

class HomeScreen(QMainWindow):
    """
        Class HomeScreen:
            
        method:
            __init__(self, role)

            init_UI(self)

            define_role(self)
    """
    switch_window_quit = QtCore.pyqtSignal()
        
    def __init__(self, role, data):
        """
            __init__(self, role): initiate attributes for home screen with users' role and page status to define users' role
        """
        self.role = role
        self.data = data
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        self.init_UI()
        self.define_role()
        
    def init_UI(self):
        """
            init_UI(self): initiate attributes for home screen
        """
        self.move(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
        )
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.tabs.setCurrentIndex(0)
        self.err.hide()
        
    def define_role(self):
        """
            define_role(self): divides class functions based on users' role
        """
        if self.role == 1:
            TeacherUIFunctions(self)
        if self.role == 0:
            StudentUIFunctions(self)

class UIFunctions(HomeScreen):
    """
        class UIFunctions:
            setup all functions needed for both students and teachers role

        methods:
            __init__(self, ui)

            connect_btn(self, ui)

            quit(self, ui)

            maximize_restore(self, ui)

    """
    def __init__(self, ui):  
        """
            __init__(self): initiate buttton functions and data connection.
        """
        self.GLOBAL_STATE = False
        self.connect_btn(ui)
        ui.username.setText(ui.data[0])
        ui.rolelabel.setText("teacher" if ui.data[3] == "1" else "student")
        ui.Entry_password.setText(ui.data[1])
        

    def connect_btn(self, ui):
        """
            connect_btn(self, ui): connect functions of button
        """
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: self.quit(ui))
        ui.account_btn.clicked.connect(lambda: ui.tabs.setCurrentIndex(1))
        ui.home_btn.clicked.connect(lambda: ui.tabs.setCurrentIndex(0))
        ui.SavePassword.clicked.connect(lambda: self.changePassword(ui))

    def quit(self, ui):
        """"
        quit(self, ui): show quit screen    
        """
        ui.switch_window_quit.emit()

    def maximize_restore(self, ui):
        """
        maximize_restore(ui): check if the window is maximize or not to maximize and minimize
        """
        status = self.GLOBAL_STATE

        if status == False:
            ui.showMaximized()
            self.GLOBAL_STATE = True
            ui.verticalLayout.setContentsMargins(0, 0, 0, 0)
            ui.btn_maximize.setToolTip("Khôi phục")
            ui.centralwidget.setStyleSheet(
                """#centralwidget{ 
                    background-color: rgb(255,255,255);
                    color: rgb(255, 255, 255);
                }"""
            )
        else:
            ui.showNormal()
            self.GLOBAL_STATE = False
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.verticalLayout.setContentsMargins(10, 10, 10, 10)
            ui.btn_maximize.setToolTip("Phóng to")
            ui.centralwidget.setStyleSheet(
                """#centralwidget{ 
                        background-color: rgb(255,255,255);
                        color: rgb(255, 255, 255);
                        border-radius: 10px;
                    }
                    """
            )
    
    def changePassword(self, ui):
        checkValue = ui.Entry_Oldpassword.text()
        checkSubmit = ui.submitPasswordLineEdit.text()
        newPassword = ui.Entry_Newpassword.text()
        if len(checkValue) * len(checkSubmit) * len(newPassword) == 0:
            ui.err.show()
            ui.err.setText("The typing process is not complete")
        elif checkValue == ui.data[1]:
            if checkSubmit == newPassword:
                with open(DATA_USERS_PATH, 'r', encoding="utf-8") as f:
                    a = f.read().split("\n")
                    d = {a[i]:a[i+1:i+4] for i in range(0, len(a), 4)}
                    d.pop('')
                d[ui.data[0]][0] = newPassword
                with open(DATA_USERS_PATH, 'w', encoding='utf-8') as f:
                    for i in list(d.keys()):
                        f.write(f"{i}\n")
                        f.write(f"{d[i][0]}\n")
                        f.write(f"{d[i][1]}\n")
                        f.write(f"{d[i][2]}\n")
                ui.SavePassword.setDisabled(True)
                ui.SavePassword.setText("Password Changed")
                ui.err.hide()
            else:
                ui.err.show()
                ui.err.setText("The passwords entered do not match")
        else:
            ui.err.show()
            ui.err.setText("The old password is incorrect")
        
class StudentUIFunctions(UIFunctions):
    """
        class StudentUIFunctions
            This class generates functions for users who are students.
        methods:
            __init__(self, ui)
    """
    def __init__(self, ui):
        super().__init__(ui)

class TeacherUIFunctions(UIFunctions):
    """
        class TeacherUIFunctions
            This class generates functions for users who are teachers.
        methods:
            __init__(self, ui)
    """
    def __init__(self, ui):
        super().__init__(ui)
