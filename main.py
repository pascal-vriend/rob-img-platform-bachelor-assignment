import sys
from GUI.ui import *


class MainWindow(QMainWindow):
    """
    creates the main window and sets up the ui. It also makes sure threads are stopped when the application is closed.
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        QApplication.instance().aboutToQuit.connect(lambda: self.ui.stop_threads_upon_close())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
