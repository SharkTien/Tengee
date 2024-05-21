import sys

from PyQt5 import QtWidgets
from ui_files import resource


from components import quit, loading_screen, login_screen

class Controller:
    """
    Controller: Class controll opened windows and related functions.
    method:
        __init__(version)

        show_loading

        show_quit

        disabled_windows

    """
    def __init__(self, version):
        """
        __init__ initiate the attributes for Controller

        """
        self.version = version
        self.main = None
        self.pg = None

    def show_loading(self):
        """
        show_loading: open loading window
        """
        self.loading = loading_screen.LoadingScreen(self.version)
        self.loading.switch_window.connect(self.show_login)
        self.loading.show()

    def show_login(self, pg=None):
        """
        show_login: open login window
        """
        if pg:
            self.pg = pg
        self.login = login_screen.LoginScreen(self.pg)
        # self.login.switch_window_home.connect(self.reset_login)
        # self.login.switch_window_home.connect(self.show_main)
        self.login.switch_window_quit.connect(self.show_quit)
        self.loading.close()
        self.login.show()
        self.login.raise_()
   
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
        # if self.main:
        #     self.main.setDisabled(
        #         state
        #     ) if all_main else self.main.frame_func_btn.setDisabled(state)
        
    def close_pg(self):
        """
            close_pg(): close window
        """
        try:
            self.pg.close()
        except:
            pass
        sys.exit()

def main(version):
    """
    main: main function initiate controller class
    """
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller(version)
    controller.show_loading()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main("0.0.0")