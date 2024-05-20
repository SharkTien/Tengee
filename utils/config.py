from PyQt5.QtWidgets import QApplication

def screen_resolution():
    app = QApplication([])
    screen_resolution = app.desktop().availableGeometry()
    return screen_resolution.width(), screen_resolution.height()

SCREEN_WIDTH, SCREEN_HEIGHT = screen_resolution()
