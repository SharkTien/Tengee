import sys

from PyQt5 import QtWidgets

from components import quit, loading_screen


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
    
    def show_loading(self):
        """
        show_loading: open loading window
        """
        self.loading = loading_screen.LoadingScreen(self.version)
        # self.loading.switch_window.connect(self.show_login)
        self.loading.show()

    def show_quit(self):
        """
        show_quit: open quit window
        """
        self.quit = quit.QuitFrame()
        self.quit.reset_state.connect(lambda: self.disable_windows())

    
    def disable_windows(self, state, all_main=False):
        """
        disable_windows(state): Disable windows, Users cannot interact to windows when this function is running
        """
        # if self.login:
        #     self.login.setDisabled(state)
        if self.main:
            self.main.setDisabled(
                state
            ) if all_main else self.main.frame_func_btn.setDisabled(state)
        

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