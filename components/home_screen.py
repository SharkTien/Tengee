import os
import random
import string
from PyQt5 import QtCore, uic, sip
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt

from path import *

import shutil

from utils.config import SCREEN_HEIGHT, SCREEN_WIDTH


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
            self.author.setText(ui.datamanager.find_data(2,self.meta_data['author']))
            self.description.setText(self.meta_data['description'].replace("•","\n"))
            self.price.setText(self.meta_data['price'])
            self.oldprice.setText(self.meta_data['oldprice'])
        
        def connect_frame_btn(self):
            """
                connect_btn(ui): initate function for buttons
            """
            self.edit_btn.clicked.connect(lambda: self.edit_course())
            self.enroll_btn.clicked.connect(lambda: self.show_details())
            self.more_information.clicked.connect(lambda: self.show_details())
            self.continue_study.clicked.connect(lambda: self.show_content())
            
        def show_details(self):
            self.ui.tabs.setCurrentIndex(4)
            self.ui.id_hidden.hide()
            self.ui.id_hidden_course.hide()
            self.ui.id_hidden.setText(self.ui.datamanager.find_data(1, self.meta_data["author"]).id)
            self.ui.B_title.setText(self.meta_data["title"])
            self.ui.B_description.setText(self.meta_data["description"].replace("•","\n"))
            self.ui.B_author.setText(self.ui.datamanager.find_data(2,self.meta_data["author"]))
            self.ui.thumbnail_banner.setStyleSheet(f"border-image: url(./ui_files/src/courses/{self.meta_data['image']});")
            self.ui.fl_price.setText(self.meta_data["price"])
            self.ui.fl_oldprice.setText(self.meta_data["oldprice"])
            self.ui.B_title_p.setText(self.ui.B_title.text())
            self.ui.B_description_p.setText(self.ui.B_description.text().replace("•","\n"))
            self.ui.author_p.setText(self.ui.B_author.text())
            self.ui.price_total.setText(str(self.ui.fl_price.text()))
            self.ui.id_hidden_course.setText(self.meta_data["id"])
            self.ui.cardnumber.setText(self.ui.datamanager.find_data(1, self.meta_data["author"]).bank_account.get_this_bank()["cardnumber"])
            self.ui.bankname.setText(self.ui.datamanager.find_data(1, self.meta_data["author"]).bank_account.get_this_bank()["bank_name"])
            self.ui.recipient.setText(self.ui.datamanager.find_data(1, self.meta_data["author"]).bank_account.get_this_bank()["recipient"])
            self.ui.code.setText(str(self.genCode()))

        def genCode(self):
            """
            genCode(self): function generate randomly a series of character
            """
            characters = string.ascii_letters + string.digits
            random_code = ''.join(random.choice(characters) for _ in range(15))
            return random_code
             
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
        self.load_data(ui, "")
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
        ui.home_btn.clicked.connect(lambda: self.load_data(ui, ui.search.text()))
        ui.Save.clicked.connect(lambda: self.change(ui))
        ui.logout_btn.clicked.connect(lambda: self.backlogin(ui))
        ui.searchgo_btn.clicked.connect(lambda: self.load_data(ui, ui.search.text()))
        ui.it.clicked.connect(lambda: self.load_data(ui, 'python'))
        ui.marketing.clicked.connect(lambda: self.load_data(ui, 'marketing')) 
        ui.all.clicked.connect(lambda: self.load_data(ui, ''))

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
        ui.descriptionfilter.setText(f"Help you get more career opportunities with {keyword if keyword else 'our Courses'}")
        current_layout = ui.homecontents.layout()
        if current_layout:
            for i in ui.homecontents.children()[2:]:
                i.setParent(None)
        ui.homescroll.verticalScrollBar().setValue(1)

        for item in ui.datamanager.get_data(0):
            course = item.get_this_course()
            if keyword.lower() in ' '.join([course['title'].lower(),course['description'].lower(), course['author'].lower()]):
                ui.Card = ui.CardFrame(ui, item)
                if ui.data.get_this_user()["role"] == '1':
                    ui.Card.enroll_btn.hide()
                    ui.Card.edit_btn.hide()
                elif ui.data.get_this_user()["role"] == '0':
                    ui.Card.more_information.hide()
                    ui.Card.edit_btn.hide()
                ui.Card.continue_study.hide()
                if item.id in ui.data.data_courses:
                    ui.Card.enroll_btn.setText("Enrolled")
                    ui.Card.enroll_btn.setDisabled(True)

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

            connect_student_btn(self)

            tabPurchase(self)

            genCode(self)

            confirmBanking(self, ui)

            warn_banking_frame(self, ui)
    """
    def __init__(self, ui):
        """
        __init__(self): initiate attributes for Student role and related functions
        """
        super().__init__(ui)
        ui.addCourses_btn.hide()
        ui.creditCardLabel_2.hide()
        ui.creditCardLabel.hide()
        ui.cardholderNameLabel.hide()
        ui.Bankname_entry.hide()
        ui.Cardnumber_entry.hide()
        ui.Recipient_entry.hide()
        self.connect_student_btn(ui)

    def connect_student_btn(self, ui):
        """
            connect_student_btn(self, ui): initiate function for basic student's buttons
        """
        
        ui.purchase.clicked.connect(lambda: ui.tabs.setCurrentIndex(5))
        ui.backbutton_p.clicked.connect(lambda: ui.tabs.setCurrentIndex(4))
        ui.confirm.clicked.connect(lambda: self.confirm_banking(ui))
        ui.ycourses_btn.clicked.connect(lambda: self.load_purchased_course(ui))
        
    def load_purchased_course(self, ui):
        """
        load_purchased_courses(self, ui): Fetch purchased courses of the current user from data file
        """
        ui.data.update_courses()
        ui.tabs.setCurrentIndex(2)
        ui.search.clear()
        ui.no_created_found.hide()
        ui.create_course.hide()
        ui.create_course_btn.hide()
        current_layout = ui.tc_content.layout()
        if current_layout:
            for i in ui.tc_content.children()[3:]:
                i.setParent(None)
        ui.tc_scroll.verticalScrollBar().setValue(1)
        for i in ui.data.data_courses:   
            item = ui.datamanager.find_data(0, i)
            ui.Card = ui.CardFrame(ui, item)
            ui.Card.enroll_btn.hide()
            ui.Card.edit_btn.hide()
            ui.Card.more_information.hide()
            ui.Card.frame_price.hide()
            current_layout.addWidget(ui.Card)

        ui.titl_create_course.setText("YOUR PURCHASED COURSES HERE")
        ui.no_created_found.setText("You have not enrolled any courses yet")
        if len(current_layout) == 2:
            ui.no_created_found.show()

    def confirm_banking(self, ui):
        """
        confirm_banking(self, ui): fuction confirming if users have already transfered tuition fee
        """
        if len(ui.lineEdit.text().split()) == 0:
            ui.lineEdit.setStyleSheet("""
                                        border-bottom: 1px solid rgb(255, 0, 0);
                                        border-radius: 0px;
                                        color: rgb(255, 0, 0);
                                      """)
        elif self.warn_banking_frame(ui):
            ui.lineEdit.setStyleSheet("""
                                        border-bottom: 1px solid gray;
                                        border-radius: 0px;
                                        color: rgb(0, 0, 0);
                                      """)
            ui.tabs.setCurrentIndex(4)
            data = [ui.id_hidden.text(), ui.data.id, ui.B_title_p.text(), ui.price_total.text(), ui.code.text(), ui.lineEdit.text(), ui.thumbnail_banner.styleSheet().split("/")[-1][:-2], ui.id_hidden_course.text()]
            open(PENDING_PATH,'a+',encoding='utf-8').write("•".join(data)+'\n')
            

    def warn_banking_frame(self, ui):
        """
        warn_banking_frame(self): display QMessageBox
        """
        msg = QMessageBox.question(
            ui, 
            "Confirm banking",
            "Confirm successful transfer? If you have not made the transfer or your cardholdername is invalid, your account will be blocked or declined refunds.",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        if msg == QMessageBox.Yes:
            return self.done_banking_frame(ui)
    
    def done_banking_frame(self, ui):
        """
        warn_banking_frame(self): display QMessageBox
        """
        QMessageBox.question(
            ui, 
            "Thankyou message",
            "Thank you for your registration. I will respond to you within the next 24 hours",
            QMessageBox.Yes
        )
        return True



class TeacherUIFunctions(UIFunction):
    """
        class TeacherUIFunctions
            This class generates functions for users who are teachers.
        methods:
            __init__(self)
    """
    class PopupsFrame(QWidget):
        """
        class PopupsFrame: Generate UI notification cards for loading notifications
        method:
            __init__(ui, data)
        """
        def __init__(self, ui, data, *args, **kwargs):
            """
            __init__(ui, data) initiate class with attributes from class QWidget and load UI file
            """
            super().__init__(*args, **kwargs)
            uic.loadUi(NOTIFICATION_POPUP_PATH, self)
            self.ui = ui
            self.data = data
            self.connect_frame_btn()
            if self.data:
                self.cardimg.setStyleSheet(f"""
                            border-image: url(./ui_files/src/courses/{self.data[6]});
                            border-radius: 10px;
                                        """)
            self.title.setText(self.data[2])
            self.cname.setText(self.data[5])
            self.price.setText(self.data[3])
            self.code.setText(self.data[4])
            
        
        def connect_frame_btn(self):
            """
                connect_frame_btn(ui): initate function for buttons
            """
            self.reject.clicked.connect(lambda: self.delete(self.ui))   
            self.accept_btn.clicked.connect(lambda: self.accept(self.ui))
        
        def accept(self, ui):
            if self.warn_accept(ui):
                data = [i.split("•") for i in open(PENDING_PATH, 'r', encoding='utf-8').read().rstrip().split("\n")]
                data.remove(self.data)
                open(PENDING_PATH, 'w', encoding='utf-8').write("\n".join(["•".join(i) for i in data]))
            
            data = open(DATA_COURSES_OWNER, 'r', encoding='utf-8').read().split("\n")[:-1]
            data = {data[i]:data[i+1].split() for i in range(0,len(data),2)}
            data[self.data[1]].append(self.data[7])
            with open(DATA_COURSES_OWNER, 'w') as f:
                for key,value in data.items():
                    f.write("%s\n%s\n" % (key, " ".join(value)))
            
            self.ui.notifications.clicked.emit()


        def delete(self, ui):
            if self.warn_reject(ui):
                data = [i.split("•") for i in open(PENDING_PATH, 'r', encoding='utf-8').read().rstrip().split("\n")]
                data.remove(self.data)
                open(PENDING_PATH, 'w', encoding='utf-8').write("\n".join(["•".join(i) for i in data]))
                self.ui.notifications.clicked.emit()

        def warn_reject(self, ui):
            msg = QMessageBox.question(
            ui, 
            "Ignore request",
            "Confirm ignore this requests? You could be reported by this student.",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
            )
            return msg == QMessageBox.Yes

        def warn_accept(self, ui):
            msg = QMessageBox.question(
            ui, 
            "Accept request",
            "Confirm accept this requests? You cannot undo this action",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
            )
            return msg == QMessageBox.Yes
        
    def __init__(self, ui):
        """
        __init__(self): initiate attributes for Student role and related functions
        """
        super().__init__(ui)
        ui.ycourses_btn.hide()
        ui.create_btn.hide()
        ui.purchase.setDisabled(True)
        self.connect_teacher_btn(ui)
        self.load_created_courses(ui)

    def connect_teacher_btn(self, ui):
        """
            connect_teacher_btn(self, ui): initiate function for basic teacher's buttons
        """
        ui.addCourses_btn.clicked.connect(lambda: self.open_addCourse_page(ui))
        ui.addCourses_btn.clicked.connect(lambda: self.load_created_courses(ui))
        ui.save_btn.clicked.connect(lambda: self.save_data(ui, 0))
        ui.create_btn.clicked.connect(lambda: self.save_data(ui, 1))
        ui.url_thumbnail_btn.clicked.connect(lambda: self.open_thumbnail_file(ui))
        ui.delete_btn.clicked.connect(lambda: self.delete_courses(ui))
        ui.create_course.clicked.connect(lambda: self.add_courses(ui))
        ui.create_course_btn.clicked.connect(lambda: self.add_courses(ui))
        ui.Save.clicked.connect(lambda: self.save_banking(ui))
        ui.notifications.clicked.connect(lambda: self.load_notification(ui))
    
    def load_notification(self, ui):
        ui.tabs.setCurrentIndex(6)
        data = open(PENDING_PATH, 'r', encoding='utf-8').read().rstrip().split("\n")
            
        current_layout = ui.notification_content.layout()
        if current_layout:
            for i in ui.notification_content.children()[2:]:
                i.setParent(None)
        ui.tc_scroll.verticalScrollBar().setValue(1)
        ui.noNotification.hide()
        for item in data:
            i = item.split("•")
            if i[0] == ui.data.id:
                ui.popup = TeacherUIFunctions.PopupsFrame(ui, i)
                current_layout.addWidget(ui.popup)
        
        if len(current_layout) == 1:
            ui.noNotification.show()

    def open_addCourse_page(self, ui):
        ui.tabs.setCurrentIndex(2)
        if not ui.data.bank_account:
            ui.create_course_btn.setText("Add bank account first")
            ui.create_course.setText("Add bank account first")
            ui.create_course_btn.setDisabled(True)
            ui.create_course.setDisabled(True)
        else:
            ui.create_course_btn.setText("Add more")
            ui.create_course.setText("Add a course")
            ui.create_course_btn.setDisabled(False)
            ui.create_course.setDisabled(False)

    def add_courses(self, ui):
        """
        add_courses(self, ui): function open edit tab and run addcourse function
        """
        ui.save_btn.hide()
        ui.create_btn.show()
        ui.tabs.setCurrentIndex(3)
        ui.edit_title_main.setText("Create your awesome courses with us")
        ui.id.setText(ui.datamanager.getID())
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
        ui.data.update_courses()
        ui.search.clear()
        ui.no_created_found.hide()
        ui.create_course.hide()
        ui.create_course_btn.show()
        ui.delete_btn.show()
        ui.save_btn.show()
        ui.create_btn.hide()
        current_layout = ui.tc_content.layout()
        if current_layout:
            for i in ui.tc_content.children()[3:]:
                i.setParent(None)
        ui.tc_scroll.verticalScrollBar().setValue(1)
        for i in ui.data.data_courses:   
            item = ui.datamanager.find_data(0, i)
            ui.Card = ui.CardFrame(ui, item)
            ui.Card.enroll_btn.hide()
            ui.Card.continue_study.hide()
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
        description = ui.description_entry.toPlainText().replace("\n","•")
        price = ui.price.text()
        oldprice = ui.oldprice.text()
        thumbnail = ui.thumbnail_entry.text()
        if not create:
            d = ui.datamanager.get_data(0)
            for item in d:
                if item.id == ui.id.text():
                    item.title = title
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
            ui.datamanager.insert_data(0, [title if title else "Untitle Course", ui.data.id, description, 
                                        price if price else "0", oldprice, thumbnail.split('/')[-1] if thumbnail else "tengee.png", ui.data.id])
            if thumbnail:
                shutil.copy(thumbnail, "./ui_files/src/courses")
            ui.create_btn.setDisabled(True)
            QtCore.QTimer.singleShot(1000, lambda: ui.create_btn.setDisabled(False))
            ui.data.data_courses.append(str(open(DATA_AMMOUNT_COURSE, 'r').read()))
            self.load_created_courses(ui)
            ui.tabs.setCurrentIndex(2)
            ui.delete_btn.show()
            ui.save_btn.show()
            ui.create_btn.hide()

    def delete_courses(self, ui):
        if self.warn_close_frame(ui):
            this_course = ui.datamanager.find_data(0, ui.id.text())
            ui.datamanager.delete(this_course, 0)
            ui.data.data_courses.remove(ui.id.text())
            ui.data_courses = ui.datamanager.get_data(0)
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
    
    def save_banking(self, ui):
        bankname = ui.Bankname_entry.text()
        cardnumber = ui.Cardnumber_entry.text()
        recipient = ui.Recipient_entry.text()
        ui.data.insert_bank(bankname, cardnumber, recipient)