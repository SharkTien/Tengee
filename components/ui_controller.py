import sys

from PyQt5 import QtWidgets

from components import quit, loading_screen, login_screen, home_screen

class Controller:
    """
    Controller: Class controll opened windows and related functions.
    method:
        __init__(version)

        show_loading

        show_home(self, role, data)

        show_quit

        disabled_windows

    """
    def __init__(self, version, data):
        """
        __init__ initiate the attributes for Controller

        """
        self.version = version
        self.data = data
        self.home = None

    def show_loading(self): 
        """
        show_loading: open loading window
        """
        self.loading = loading_screen.LoadingScreen(self.version)
        self.loading.switch_window_login.connect(self.show_login)
        self.loading.show()

    def show_login(self):
        """
        show_login: open login window
        """
        self.login = login_screen.LoginScreen(self.data)
        self.login.switch_window_home.connect(self.close_login)
        self.login.switch_window_home.connect(self.show_home)
        self.login.switch_window_quit.connect(self.show_quit)
        self.loading.close()
        self.login.show()
        self.login.raise_()

    def show_home(self, data=None, datamanager=None):
        """
            show_home(self, role, data): show home screen after sign in succession
        """
        self.home = home_screen.HomeScreen(data, datamanager)
        self.home.switch_window_quit.connect(self.show_quit)
        self.home.switch_window_login.connect(self.close_home)
        self.home.switch_window_login.connect(self.show_login)
        self.home.show()    

    def show_quit(self):
        """
        show_quit: open quit window
        """
        self.quit = quit.QuitFrame()
        self.quit.reset_state.connect(lambda: self.disable_windows(state=False, all_main=True))
        self.quit.close_window.connect(self.close_pg)
        self.disable_windows(state=True, all_main=True)
        self.quit.show()

    def disable_windows(self, state, all_main=False):
        """
        disable_windows(state): Disable windows, Users cannot interact to windows when this function is running
        """
        if self.login:
            self.login.setDisabled(state)
        if self.home:
            self.home.setDisabled(
                state
            ) if all_main else self.home.mainlayout.setDisabled(state)

    def close_login(self):
        """
            close_login(self): close login window after sign in succession
        """
        self.login.close()
        self.login = None

    def close_home(self):
        """
            close_home(self): close home window after logout
        """
        self.home.close()
        self.home = None
 
    def close_pg(self):
        """
            close_pg(): close window
        """
        sys.exit()

def main(version, data):
    """
    main: main function initiate controller class
    """
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller(version, data)
    controller.show_loading()
    sys.exit(app.exec_())
