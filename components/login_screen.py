import time

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from data_init import DataManager

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

        connect_btn()

        default()

        openQuitFrame()

        check_autosave()

        maximize_restore()

        check_SI()

        check_SU()

        open_main()

        get_login_data()


    """
    switch_window_home = QtCore.pyqtSignal(int, list)
    switch_window_quit = QtCore.pyqtSignal()
    enabled = "qwertyuiopasdfghjklzxcvbnm1234567890 @/._"
    GLOBAL_STATE = False
    STATE_ECHOPASS = True

    def __init__(self, datamanager): 
        """
            __init__(): initiate attributes for Login Screen. 
        """
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_PATH, self)
        self.initUI()
        self.datamanager = datamanager
        self.data = self.get_login_data()
        self.connect_btn()
        self.check_autosave()

    def initUI(self):
        """
            initUI(): inititate and move window to center of screen, then initiate attributes     
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
            moveWindow(event): enable to drag the window  
        """
        if self.GLOBAL_STATE == True:
            self.maximize_restore(self)
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        """
            mousePressEvent: catch event dragging
        """
        self.dragPos = event.globalPos()
    
    def connect_btn(self):
        """
            connect_btn(): add function for button close, minimize, maximize
        """
        self.btn_maximize.setToolTip("Phóng to")
        self.btn_minimize.setToolTip("Thu nhỏ")
        self.btn_quit.setToolTip("Đóng")

        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_maximize.clicked.connect(lambda: self.maximize_restore())
        self.btn_quit.clicked.connect(lambda: self.openQuitFrame())

        self.eyeHide_SI.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeHide.clicked.connect(
            lambda: self.PassBox.setEchoMode(QtWidgets.QLineEdit.Password)
        )
        self.eyeShow_SI.clicked.connect(
            lambda: self.PassBox_SI.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        self.eyeShow.clicked.connect(
            lambda: self.PassBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        )
        self.SignIn_Bt.clicked.connect(lambda: self.check_SI())
        self.SignUp_Bt.clicked.connect(lambda: self.check_SU())
        self.ConvertButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.ConvertButton_SU.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        self.ConvertButton_4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.ConvertButton.clicked.connect(lambda: self.default())

    def default(self):
        """
        default(): Function reset state
        """
        self.STATE_ECHOPASS = True
        self.PassBox.clear()
        self.NameBox.clear()
        self.UserBox.clear()
        self.Note_Name.hide()
        self.Note_Pass.hide()
        self.Note_User.hide()
        self.student.setChecked(True)

    def openQuitFrame(self):
        """
        openQuitFrame(): open Quit window
        """
        self.switch_window_quit.emit()

    def check_autosave(self):
        """
        check_autosave(): open data file to check saved account
        """
        with open(USER_PATH, encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > 1:
            self.NameBox_SI.setText(lines[0].rstrip())
            self.PassBox_SI.setText(lines[2].rstrip())
            self.SavePass.setChecked(True)

    def maximize_restore(self):
        """
        maximize_restore(): check if the window is maximize or not to maximize and minimize
        """
        status = self.GLOBAL_STATE

        if status == False:
            self.showMaximized()
            self.GLOBAL_STATE = True
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.btn_maximize.setToolTip("Khôi phục")
            self.bg_frame.setStyleSheet(
                """#bg_frame {
                    border-image: url(:/icons/background-login.png);
                    background-repeat: no-repeat;
                    border-radius: 9px;
                }"""
            )
        else:
            self.showNormal()
            self.GLOBAL_STATE = False
            self.resize(self.width() + 1, self.height() + 1)
            self.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.btn_maximize.setToolTip("Phóng to")
            self.bg_frame.setStyleSheet(
                """#bg_frame {
                    background-image: url(:/icons/background-login.png);
                    background-repeat: no-repeat;
                }"""
            )

    def get_login_data(self):
        """
        get_data() -> list: get data from file data. Format: [{'accountname':['password','username',bool]]
        """
        data = dict()
        for item in self.datamanager.get_data(1):
            p = item.get_this_user()
            data[p[0]] = p[1]
        return data
    
    def check_SI(self):
        self.data = self.get_login_data()
        """
        check_SI(): Function check if the information login is valid
        """
        username = self.NameBox_SI.text()
        password = self.PassBox_SI.text()

        if len(password) * len(username) == 0:
            self.frameError.show()
            self.Error_Content.setText("Chưa điền đầy đủ thông tin đăng nhập")
        else:
            self.frameError.hide()
            if username not in list(self.data.keys()):
                self.frameError.show()
                self.Error_Content.setText("Tên tài khoản không tồn tại. Hãy nhập lại.")
            else:
                if self.data[username][0] != password:
                    self.frameError.show()
                    self.Error_Content.setText("Mật khẩu không chính xác. Hãy nhập lại.")
                else:
                    name, role = [self.data[username][1], int(self.data[username][2])]
                
                    with open(USER_PATH, "w", encoding="utf-8") as f:
                        if self.SavePass.isChecked():
                            f.write(f"{username}\n")
                            f.write(f"{name}\n")
                            f.write(f"{password}\n")
                            f.write(f"{str(role)}")
                    
                    self.open_home(role, [username]+self.data[username])

                QtCore.QTimer.singleShot(3000, lambda: self.frameError.hide())

    def open_home(self, role, data):
        """
            open_home(ui, role, data): open home window
        """
        self.switch_window_home.emit(role, data)

    def check_SU(self):
        """
            check_SU(): check if the register information is valid
        """
        self.data = self.get_login_data()
        check = True
        username = self.NameBox.text()
        password = self.PassBox.text()
        name = self.UserBox.text()

        if len(username) < 8 or list(
            {False for i in username.lower() if i not in self.enabled}
        ) == [False]:
            self.Note_Name.show()
            check = False
        else:
            if username in list(self.data.keys()):
                self.Note_Name.show()
                check = False
            else:
                self.Note_Name.hide()

        if len(password) < 8 or list(
            {False for i in password.lower() if i not in self.enabled}
        ) == [False]:
            self.Note_Pass.show()
            check = False
        else:
            self.Note_Pass.hide()

        if "".join(i for i in name.lower() if i not in self.enabled).isalnum():
            self.Note_User.hide()

        elif "".join(i for i in name.lower() if i not in self.enabled) != "":
            self.Note_User.show()
            check = False
        else:
            self.Note_User.hide()
        if len(name) < 6:
            self.Note_User.show()
            check = False

        if check:
            role = 1 if self.teacher.isChecked() else 0
            self.datamanager.insert_data(1, [username, password, name, role])
            self.NameBox_SI.clear()
            self.PassBox_SI.clear()
            self.SavePass.setChecked(False)
            self.stacked_widget.setCurrentIndex(2)


