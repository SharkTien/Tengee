from PyQt5 import QtCore, uic, sip
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from utils.config import SCREEN_HEIGHT, SCREEN_WIDTH


UI_MAIN_PATH = "./ui_files/Home_gui.ui"

USERS_PATH = "./data/users/users.dat"
CARD_PATH = "./ui_files/card.ui"

class HomeScreen(QMainWindow):
    """
        Class HomeScreen:
            
        method:
            __init__(self)

            init_UI(self)

            define_role(self)

    """
    switch_window_quit = QtCore.pyqtSignal()
    switch_window_login = QtCore.pyqtSignal()
    class CardFrame(QWidget):
        """
        class CardFrame: Generate UI Card for fetching data
        method:
            __init__(self, *args, **kwargs)
        """
        def __init__(self, *args, **kwargs):
            """
            initiate class with attributes from class QWidget and load UI file
            """
            super().__init__(*args, **kwargs)
            uic.loadUi(CARD_PATH, self)

    def __init__(self, data, datamanager):
        """
            __init__(self, data): initiate attributes for home screen with users' role and page status to define users' role
        """
        
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi(UI_MAIN_PATH, self)
        self.data = data
        self.datamanager = datamanager
        self.data_courses = self.datamanager.get_data(0)
        self.data_users = self.datamanager.get_data(1)

        self.init_UI()
        self.define_role()

    def define_role(self):
        if self.data.get_this_user()["role"] == 0:
            StudentUIFunctions(self)
        else:
            TeacherUIFunctions(self)

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
        self.noanswer.hide()

class UIFunction(HomeScreen):
    """
        connect_btn(self)

        quit(self)

        maximize_restore(self)

        change(self)

        backlogin(self)
    """
    GLOBAL_STATE = False    
    def __init__(self, ui):
        self.connect_btn(ui)
        self.load_data(ui, "python")
        ui.username.setText(ui.data.get_this_user()["username"])
        ui.rolelabel.setText("teacher" if ui.data.get_this_user()["role"] == "1" else "student")
        ui.Entry_password.setText(ui.data.get_this_user()["password"])
        ui.Entry_username.setText(ui.data.get_this_user()["username"]) 

    def connect_btn(self, ui):
        """
            connect_btn(self): connect functions of button
        """
        ui.btn_maximize.clicked.connect(lambda: self.maximize_restore(ui))
        ui.btn_minimize.clicked.connect(lambda: ui.showMinimized())
        ui.btn_quit.clicked.connect(lambda: self.quit(ui))
        ui.account_btn.clicked.connect(lambda: ui.tabs.setCurrentIndex(1))
        ui.home_btn.clicked.connect(lambda: ui.tabs.setCurrentIndex(0))
        ui.Save.clicked.connect(lambda: self.change(ui))
        ui.logout_btn.clicked.connect(lambda: self.backlogin(ui))
        ui.searchgo_btn.clicked.connect(lambda: self.load_data(ui, ui.search.text()))
        ui.it.clicked.connect(lambda: self.load_data(ui, 'python'))
        ui.marketing.clicked.connect(lambda: self.load_data(ui, 'marketing')) 
        ui.psychology.clicked.connect(lambda: self.load_data(ui, 'psychology'))

    def quit(self, ui):
        """"
        quit(self): show quit screen    
        """
        ui.switch_window_quit.emit()

    def maximize_restore(self, ui):
        """
        maximize_restore(self): check if the window is maximize or not to maximize and minimize
        """
        status = self.GLOBAL_STATE

        if status == False:
            ui.showMaximized()
            self.GLOBAL_STATE = True
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
            ui.btn_maximize.setToolTip("Phóng to")
            ui.centralwidget.setStyleSheet(
                """#centralwidget{ 
                        background-color: rgb(255,255,255);
                        color: rgb(255, 255, 255);
                        border-radius: 10px;
                    }
                    """
            )
    
    def change(self, ui):
        """
        change(self): edit data including password, nameaccount, creditcards and save into data file
        """
        checkValue = ui.Entry_Oldpassword.text()
        checkSubmit = ui.submitPasswordLineEdit.text()
        newPassword = ui.Entry_Newpassword.text()
        d = dict()
        for item in ui.datamanager.get_data(1):
            p = item.get_this_user()
            d[p[0]] = [item.id] + p[1]

        if len(checkValue) * len(checkSubmit) * len(newPassword) == 0:
            if len(checkValue) or len(checkSubmit) or len(newPassword):
                ui.err.show()
                ui.err.setText("The typing process is not complete")
            else:
                if len(ui.Entry_username.text()) < 6:
                    ui.err.show()
                    ui.err.setText("your username is invalid (length must be more than 6 characters)")
                else:
                    d[ui.data[0]][2] = ui.Entry_username.text()
                    
                    with open(USERS_PATH, 'w', encoding='utf-8') as f:
                        pass
                    ui.datamanager.update_data(1, d)
                    ui.Save.setDisabled(True)
                    ui.Save.setText("Saved")
                    ui.username.setText(ui.Entry_username.text())
                    QtCore.QTimer.singleShot(1000, lambda: ui.Save.setText("Save"))
                    QtCore.QTimer.singleShot(1000, lambda: ui.Save.setDisabled(False))
                    ui.err.hide()
            
        elif checkValue == ui.data[1]:
            if checkSubmit == newPassword:
                if len(ui.Entry_username.text()) < 6:
                    ui.err.show()
                    ui.err.setText("your username is invalid (length must be more than 6 characters)")
                else:
                    d[ui.data[0]][2] = ui.Entry_username.text()
                d[ui.data[0]][1] = newPassword
                with open(USERS_PATH, 'w', encoding='utf-8') as f:
                        pass
                ui.datamanager.update_data(1, d)
                ui.Save.setDisabled(True)
                ui.Save.setText("Saved")
                QtCore.QTimer.singleShot(1000, lambda: ui.Save.setText("Save"))
                QtCore.QTimer.singleShot(1000, lambda: ui.Save.setDisabled(False))
                ui.err.hide()
                ui.Entry_password.setText(newPassword)
            else:
                ui.err.show()
                ui.err.setText("The passwords entered do not match")
        else:
            ui.err.show()
            ui.err.setText("The old password is incorrect")
    
    def backlogin(self, ui):
        """
        backlogin(self): sign out account  
        """
        ui.switch_window_login.emit()
    
    def load_data(self, ui, keyword):
        """
        load_data(self, ui, keyword): Fetch data based on the keyword from data file
        """
        ui.noanswer.hide()
        ui.descriptionfilter.setText(f"Help you get more career opportunities with '{keyword}'")
        current_layout = ui.homecontents.layout()
        if current_layout:
            for i in ui.homecontents.children()[2:]:
                i.setParent(None)
        ui.homescroll.verticalScrollBar().setValue(1)

        for item in ui.data_courses:
            course = item.get_this_course()
            if keyword.lower() in ' '.join([course['title'].lower(),course['description'].lower(), course['author'].lower()]):
                ui.Card = ui.CardFrame()
                current_layout.addWidget(ui.Card)
                ui.Card.cardimg.setStyleSheet(f"""
                                border-image: url(./ui_files/src/courses/{course['image']});
                                border-radius: 10px;
                                padding: -50px;
                                            """)
                ui.Card.title.setText(course['title'])
                ui.Card.author.setText(course['author'])
                ui.Card.description.setText(course['description'])
                ui.Card.price.setText(course['price'])
                ui.Card.oldprice.setText(course['oldprice'])
        if len(current_layout) == 1:
            ui.noanswer.show()
            ui.noanswer.setText(f"Sorry, we couldn't find any results for '{keyword}'\n\nTry adjusting your search. Here are some ideas:\n\n •   Make sure all words are spelled correctly\n •   Try different search terms\n •   Try more general search terms")

class StudentUIFunctions(UIFunction):
    """
        class StudentUIFunctions
            This class generates functions for users who are students.
        methods:
            __init__(self)
    """
    def __init__(self, ui):
        """
        __init__(self): initiate attributes for Student role and related functions
        """
        super().__init__(ui)
        ui.addCourses_btn.hide()
        ui.cardholderNameLabel.hide()
        ui.cardholderNameLineEdit.hide()
        ui.creditCardLabel.hide()
        ui.creditCardLineEdit.hide()

class TeacherUIFunctions(UIFunction):
    """
        class TeacherUIFunctions
            This class generates functions for users who are teachers.
        methods:
            __init__(self)
    """
    def __init__(self, ui):
        """
        __init__(self): initiate attributes for Student role and related functions
        """
        super().__init__(ui)
        ui.ycourses_btn.hide()
        ui.cart_btn.hide()
        self.connect_teacher_btn(ui)
        self.load_created_courses(ui)

    def connect_teacher_btn(self, ui):
        ui.addCourses_btn.clicked.connect(lambda: ui.tabs.setCurrentIndex(2))
    
    def load_created_courses(self, ui):
        """
        load_created_courses(self, ui): Fetch created courses of the current user from data file
        """
        ui.no_created_found.hide()
        ui.create_course.hide()
        ui.create_course_btn.show()
        current_layout = ui.tc_content.layout()
        if current_layout:
            for i in ui.tc_content.children()[3:]:
                i.setParent(None)
        ui.tc_scroll.verticalScrollBar().setValue(1)
        
        for i in ui.data.data_courses:     
            item = ui.datamanager.find_data(0, i).get_this_course()
            ui.Card = ui.CardFrame()
            current_layout.addWidget(ui.Card)
            ui.Card.cardimg.setStyleSheet(f"""
                            border-image: url(./ui_files/src/courses/{item['image']});
                            border-radius: 10px;
                            padding: -50px;
                                        """)
            ui.Card.title.setText(item['title'])
            ui.Card.author.setText(item['author'])
            ui.Card.description.setText(item['description'])
            ui.Card.price.setText(item['price'])
            ui.Card.oldprice.setText(item['oldprice'])
            ui.Card.enroll_btn.setText("Edit")
            ui.Card.enroll_btn.clicked.connect(lambda: self.editCourse(ui, ui.Card, item))
        current_layout.addStretch()
    
        if len(current_layout) == 3:
            ui.no_created_found.show()
            ui.create_course.show()
            ui.create_course_btn.hide()
    def editCourse(self, ui, card, data):
        ui.tabs.setCurrentIndex(3)
        if data:
            ui.title_entry.setText(data["title"])
            ui.author_entry.setText(data["author"])
            ui.description_entry.setText(data["description"])
            ui.thumbnail_entry.setText(data["image"])
            ui.price.setText(data["price"])
            ui.oldprice.setText(data["oldprice"])

        ui.save_btn.clicked.connect(lambda: self.edit_course_information(ui.Card))
            
    