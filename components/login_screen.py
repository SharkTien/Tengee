import time

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

USER_PATH = "./data/users/users.dat"
UI_PATH = "./ui_files/Login_gui.ui"
DATA_USERS_PATH = "./data/users/data_users.dat"
from utils.config import SCREEN_HEIGHT, SCREEN_WIDTH

class LoginScreen(QMainWindow):
    """
    class LoginScreen:
    method:

        __init__()

        initUI()

        moveWindow(event)

        mousePressEvent(event)

    """
    switch_window_home = QtCore.pyqtSignal(int, list)
    switch_window_quit = QtCore.pyqtSignal()

    def __init__(self): 
        """
            __init__(): initiate attributes for Login Screen. 
        """
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_PATH, self)
        self.initUI()
        LoginFunctions(self)

    def initUI(self):
        """
            initUI: inititate and move window to center of screen, then initiate attributes     
        """
        self.frameError.hide()
        self.eyeHide_SI.hide()
        self.eyeHide.hide()
        self.stacked_widget.setCurrentIndex(0)
        self.Note_Name.hide()
        self.Note_Pass.hide()
        self.Note_User.hide()
        self.setGeometry(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
            self.width(),
            self.height(),
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.title_bar.mouseMoveEvent = self.moveWindow

        self.move(
            round((SCREEN_WIDTH - self.width()) / 2),
            round((SCREEN_HEIGHT - self.height()) / 2),
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    
    def moveWindow(self, event):
        """
            moveWindow: enable to drag the window  
        """
        if LoginFunctions.GLOBAL_STATE == True:
            LoginFunctions.maximize_restore(self)
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        """
            mousePressEvent: catch event dragging
        """
        self.dragPos = event.globalPos()


class LoginFunctions(LoginScreen):
    """
    class LoginFunctions:
        method:
        __init__(ui)

        connect_btn(ui)

        default(ui)

        openQuitFrame(ui)

        check_autosave(ui)

        maximize_restore(ui)

        check_SI(ui)

        check_SU(ui)

        open_main(ui)

        get_data(ui)

    """
    enabled = "qwertyuiopasdfghjklzxcvbnm1234567890 @/._"
    GLOBAL_STATE = False
    STATE_ECHOPASS = True

    def __init__(self, ui):
        """
            __init__(ui): initiate functions for ui
        """
        self.data = self.get_data()
        self.connect_btn(ui)
        self.check_autosave(ui)

    def connect_btn(self, ui):
        """
            connect_btn(ui): add function for button close, minimize, maximize
        """
        ui.btn_maximize.setToolTip("Phóng to")
        ui.btn_minimize.setToolTip("Thu nhỏ")
        ui.btn_quit.setToolTip("Đóng")

        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_quit.clicked.connect(lambda: self.openQuitFrame(ui))

        ui.eyeHide_SI.clicked.connect(
            lambda: ui.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        ui.eyeHide.clicked.connect(
            lambda: ui.PassBox.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        ui.eyeShow_SI.clicked.connect(
            lambda: ui.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        ui.eyeShow.clicked.connect(
            lambda: ui.PassBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        ui.SignIn_Bt.clicked.connect(lambda: self.check_SI(ui))
        ui.SignUp_Bt.clicked.connect(lambda: self.check_SU(ui))
        ui.ConvertButton.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(1))

        ui.ConvertButton_SU.clicked.connect(
            lambda: ui.stacked_widget.setCurrentIndex(0)
        )
        ui.ConvertButton_4.clicked.connect(lambda: ui.stacked_widget.setCurrentIndex(0))
        ui.ConvertButton.clicked.connect(lambda: self.default(ui))

    def default(self, ui):
        """
        default(ui): Function reset state
        """
        ui.STATE_ECHOPASS = True
        ui.PassBox.clear()
        ui.NameBox.clear()
        ui.UserBox.clear()
        ui.Note_Name.hide()
        ui.Note_Pass.hide()
        ui.Note_User.hide()
        ui.student.setChecked(True)

    def openQuitFrame(self, ui):
        """
        openQuitFrame(ui): open Quit window
        """
        ui.switch_window_quit.emit()

    def check_autosave(self, ui):
        """
        check_autosave(ui): open data file to check saved account
        """
        with open(USER_PATH, encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > 1:
            ui.NameBox_SI.setText(lines[0].rstrip())
            ui.PassBox_SI.setText(lines[2].rstrip())
            ui.SavePass.setChecked(True)

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
            ui.bg_frame.setStyleSheet(
                """#bg_frame {
                    border-image: url(:/icons/background-login.png);
                    background-repeat: no-repeat;
                    border-radius: 9px;
                }"""
            )
        else:
            ui.showNormal()
            self.GLOBAL_STATE = False
            ui.resize(ui.width() + 1, ui.height() + 1)
            ui.verticalLayout.setContentsMargins(10, 10, 10, 10)
            ui.btn_maximize.setToolTip("Phóng to")
            ui.bg_frame.setStyleSheet(
                """#bg_frame {
                    background-image: url(:/icons/background-login.png);
                    background-repeat: no-repeat;
                }"""
            )

    def get_data(self):
        with open(DATA_USERS_PATH, 'r') as f:
            a = f.read().split("\n")
            d = {a[i]:a[i+1:i+4] for i in range(0, len(a), 4)}
            d.pop('')
            return d

    def check_SI(self, ui):
        self.data = self.get_data()
        """
        check_SI(ui): Function check if the information login is valid
        """
        username = ui.NameBox_SI.text()
        password = ui.PassBox_SI.text()

        if len(password) * len(username) == 0:
            ui.frameError.show()
            ui.Error_Content.setText("Chưa điền đầy đủ thông tin đăng nhập")
        else:
            ui.frameError.hide()
            if username not in list(self.data.keys()):
                ui.frameError.show()
                ui.Error_Content.setText("Tên tài khoản không tồn tại. Hãy nhập lại.")
            else:
                if self.data[username][0] != password:
                    ui.frameError.show()
                    ui.Error_Content.setText("Mật khẩu không chính xác. Hãy nhập lại.")
                else:
                    name, role = [self.data[username][1], int(self.data[username][2])]
                
                    with open(USER_PATH, "w", encoding="utf-8") as f:
                        if ui.SavePass.isChecked():
                            f.write(f"{username}\n")
                            f.write(f"{name}\n")
                            f.write(f"{password}\n")
                            f.write(f"{str(role)}")
                    
                    self.open_home(ui, role, [username]+self.data[username])

                QtCore.QTimer.singleShot(3000, lambda: ui.frameError.hide())

    def open_home(self, ui, role, data):
        """
            open_home(ui, role): open home window
        """
        ui.switch_window_home.emit(role, data)

    def check_SU(self, ui):
        """
            check_SU(ui): check if the register information is valid
        """
        self.data = self.get_data()
        check = True
        username = ui.NameBox.text()
        password = ui.PassBox.text()
        name = ui.UserBox.text()

        if len(username) < 8 or list(
            {False for i in username.lower() if i not in self.enabled}
        ) == [False]:
            ui.Note_Name.show()
            check = False
        else:
            if username in list(self.data.keys()):
                ui.Note_Name.show()
                check = False
            else:
                ui.Note_Name.hide()

        if len(password) < 8 or list(
            {False for i in password.lower() if i not in self.enabled}
        ) == [False]:
            ui.Note_Pass.show()
            check = False
        else:
            ui.Note_Pass.hide()

        if "".join(i for i in name.lower() if i not in self.enabled).isalnum():
            ui.Note_User.hide()

        elif "".join(i for i in name.lower() if i not in self.enabled) != "":
            ui.Note_User.show()
            check = False
        else:
            ui.Note_User.hide()
        if len(name) < 6:
            ui.Note_User.show()
            check = False

        if check:
            role = 1 if ui.teacher.isChecked() else 0
            with open(DATA_USERS_PATH, 'a+', encoding='utf-8') as f:
                f.write(f"{username}\n")
                f.write(f"{password}\n")
                f.write(f"{name}\n")
                f.write(f"{str(role)}\n")
            ui.NameBox_SI.clear()
            ui.PassBox_SI.clear()
            ui.SavePass.setChecked(False)
            ui.stacked_widget.setCurrentIndex(2)


