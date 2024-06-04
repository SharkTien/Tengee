import os 
from PyQt5 import QtCore, uic, sip
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import shutil

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
    GLOBAL_STATE = False
    #========================= ClASS CARD ======================== #
    class CardFrame(QWidget):
        """
        class CardFrame: Generate UI Card for fetching data
        method:
            __init__(self, *args, **kwargs)
        """
        def __init__(self, ui, data, *args, **kwargs):
            """
            initiate class with attributes from class QWidget and load UI file
            """
            super().__init__(*args, **kwargs)
            uic.loadUi(CARD_PATH, self)
            self.ui = ui
            self.data = data
            self.meta_data = self.data.get_this_course()
            self.connect_frame_btn()
            if self.data:
                self.cardimg.setStyleSheet(f"""
                            border-image: url(./ui_files/src/courses/{self.meta_data['image']});
                            border-radius: 10px;
                            padding: -50px;
                                        """)
            self.title.setText(self.meta_data['title'])
            self.author.setText(self.meta_data['author'])
            self.description.setText(self.meta_data['description'].replace("•","\n"))
            self.price.setText(self.meta_data['price'])
            self.oldprice.setText(self.meta_data['oldprice'])
        
        def connect_frame_btn(self):
            """
                connect_btn(ui): initate function for buttons
            """
            self.edit_btn.clicked.connect(lambda: self.edit_course())
            self.enroll_btn.clicked.connect(lambda: self.show_details())
            
        def show_details(self):
            self.ui.tabs.setCurrentIndex(4)
            self.ui.B_title.setText(self.meta_data["title"])
            self.ui.B_description.setText(self.meta_data["description"])
            self.ui.B_author.setText(self.meta_data["author"])
            self.ui.thumbnail_banner.setStyleSheet(f"border-image: url(./ui_files/src/courses/{self.meta_data['image']});")
            self.ui.fl_price.setText(self.meta_data["price"])
            self.ui.fl_oldprice.setText(self.meta_data["oldprice"])
             
        def edit_course(self):
            """
                edit_course(): link to the editcourse tab and change data course of current card
            """
            self.ui.tabs.setCurrentIndex(3)
            self.ui.edit_title_main.setText("Edit courses page")
            self.ui.id.setText(self.meta_data["id"])
            self.ui.title_entry.setText(self.meta_data["title"])
            self.ui.description_entry.setText(self.meta_data["description"].replace("•","\n"))
            self.ui.thumbnail_entry.setText(self.meta_data["image"])
            self.ui.price.setText(self.meta_data["price"])
            self.ui.oldprice.setText(self.meta_data["oldprice"])
            
    #================== END CLASS CARD =======================================#

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
        self.title_bar.mouseMoveEvent = self.moveWindow 
        self.define_role()

    def define_role(self):
        """
            define_role(self): separate student and teacher function
        """
        if self.data.get_this_user()["role"] == '0':
            StudentUIFunctions(self)
        elif self.data.get_this_user()["role"] == '1':
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
        
        d = ui.datamanager.get_data(1)
        
        if len(checkValue) * len(checkSubmit) * len(newPassword) == 0:
            if len(checkValue) or len(checkSubmit) or len(newPassword):
                ui.err.show()
                ui.err.setText("The typing process is not complete")
            else:
                if len(ui.Entry_username.text()) < 6:
                    ui.err.show()
                    ui.err.setText("your username is invalid (length must be more than 6 characters)")
                else:
                    for item in d:
                        if item.get_this_user()["accountname"] == ui.data.get_this_user()["accountname"]:
                            item.change_username(ui.Entry_username.text())
                    with open(USERS_PATH, 'w', encoding='utf-8') as f:
                        pass
                    data = []
                    for item in d:
                        i = item.get_this_user()
                        data.append([i["id"], 1, i["accountname"], i["password"], i["username"], i["role"]])
                    ui.datamanager.update_data(1, data)
                    ui.Save.setDisabled(True)
                    ui.Save.setText("Saved")
                    ui.username.setText(ui.Entry_username.text())
                    QtCore.QTimer.singleShot(1000, lambda: ui.Save.setText("Save"))
                    QtCore.QTimer.singleShot(1000, lambda: ui.Save.setDisabled(False))
                    ui.err.hide()
            
        elif checkValue == ui.data.get_this_user()["password"]:
            if checkSubmit == newPassword:
                if len(ui.Entry_username.text()) < 6:
                    ui.err.show()
                    ui.err.setText("your username is invalid (length must be more than 6 characters)")
                else:
                    for item in d:
                        if item.get_this_user()["accountname"] == ui.data.get_this_user()["accountname"]:
                            item.change_username(ui.Entry_username.text()) 
                for item in d:
                        if item.get_this_user()["accountname"] == ui.data.get_this_user()["accountname"]:
                            item.change_password(newPassword)
                with open(USERS_PATH, 'w', encoding='utf-8') as f:
                        pass
                data = []
                for item in d:
                    i = item.get_this_user()
                    data.append([i["id"], 1, i["accountname"], i["password"], i["username"], i["role"]])
                ui.datamanager.update_data(1, data)
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
                ui.Card = ui.CardFrame(ui, item)
                if ui.data.get_this_user()["role"] == 1:
                    ui.Card.enroll_btn.hide()
                    ui.Card.addtocard_btn.hide()
                else:
                    ui.Card.more_information.hide()
                    ui.Card.edit_btn.hide()
                current_layout.addWidget(ui.Card)
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
        self.connect_teacher_btn(ui)
        self.load_created_courses(ui)

    def connect_teacher_btn(self, ui):
        """
            connect_teacher_btn(self, ui): initiate function for basic teacher's buttons
        """
        ui.addCourses_btn.clicked.connect(lambda: ui.tabs.setCurrentIndex(2))
        ui.addCourses_btn.clicked.connect(lambda: self.load_created_courses(ui))
        ui.save_btn.clicked.connect(lambda: self.save_data(ui, 0))
        ui.url_thumbnail_btn.clicked.connect(lambda: self.open_thumbnail_file(ui))
        ui.delete_btn.clicked.connect(lambda: self.delete_courses(ui))
        ui.create_course.clicked.connect(lambda: self.add_courses(ui))
        ui.create_course_btn.clicked.connect(lambda: self.add_courses(ui))

    def add_courses(self, ui):
        """
        add_courses(self, ui): function open edit tab and run addcourse function
        """
        ui.tabs.setCurrentIndex(3)
        ui.edit_title_main.setText("Create your awesome courses with us")
        ui.title_entry.clear()
        ui.description_entry.clear()
        ui.thumbnail_entry.clear()
        ui.price.clear()
        ui.oldprice.clear()
        ui.delete_btn.hide()

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
            item = ui.datamanager.find_data(0, int(i))
            ui.Card = ui.CardFrame(ui, item)
            ui.Card.enroll_btn.hide()
            current_layout.addWidget(ui.Card)

        if len(current_layout) == 2:
            ui.no_created_found.show()
            ui.create_course.show()
            ui.create_course_btn.hide()
    
    def save_data(self, ui, create):
        """
        save_data(ui): save current edited data in course edit page
        """
        title = ui.title_entry.text()
        username = ui.username.text()
        description = ui.description_entry.toPlainText().replace("\n","•")
        price = ui.price.text()
        oldprice = ui.oldprice.text()
        thumbnail = ui.thumbnail_entry.text()
        if not create:
            d = ui.datamanager.get_data(0)
            for item in d:
                if item.id == ui.id.text():
                    item.title = title
                    item.author = username
                    item.description = description
                    item.price = price if price else 0
                    item.oldprice = oldprice
                    item.image = thumbnail
            ui.datamanager.update_data(0, d)
            ui.save_btn.setDisabled(True)
            ui.save_btn.setText("Saved")
            QtCore.QTimer.singleShot(1000, lambda: ui.save_btn.setText("Save"))
            QtCore.QTimer.singleShot(1000, lambda: ui.save_btn.setDisabled(False))
        else:
            try:
                ui.datamanager.insert_data(0, [title if title else "Untitle Course", username, description, 
                                           price if price else "0", oldprice, thumbnail.split('/')[-1] if thumbnail else "tengee.png", ui.data.id])
                if thumbnail:
                    shutil.copy(thumbnail, "./ui_files/src/courses")
                ui.save_btn.setDisabled(True)
                ui.save_btn.setText("Created")
                QtCore.QTimer.singleShot(1000, lambda: ui.save_btn.setText("Save"))
                QtCore.QTimer.singleShot(1000, lambda: ui.save_btn.setDisabled(False))
                ui.data.data_courses.append(len(ui.datamanager.get_data(0)))
                self.load_created_courses(ui)
                ui.tabs.setCurrentIndex(2)
            except:
                ui.tabs.setCurrentIndex(2)
            ui.delete_btn.show()

    def delete_courses(self, ui):
        if self.warn_close_frame(ui):
            self.load_created_courses(ui)
        ui.tabs.setCurrentIndex(2)
            

    def warn_close_frame(self, ui):
        msg = QMessageBox.question(
            ui, 
            "Delete course",
            "Confirm delete this courses? You cannot backup this action",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        return msg == QMessageBox.Yes
    
    def open_thumbnail_file(self, ui):
        HOME_PATH = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        file_path = QFileDialog.getOpenFileName(ui, "Open file", HOME_PATH, "*.png;*.jfif;*.pjpeg;*.jpeg;*.pjp;*.jpg;*.heic;*.webp")
        if file_path[0]:
            ui.thumbnail_entry.setText(file_path[0])
            