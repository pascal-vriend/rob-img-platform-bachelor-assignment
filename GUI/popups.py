from PySide2.QtWidgets import QMessageBox


class ErrorDialog:
    """
    A dialog that will pop up when an error occurs.
    """
    def __init__(self, message):
        self.message = message
        self.open_window()

    def open_window(self):
        """
        sets up the window with the provided error message and executes it.
        :return:
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(self.message)
        error_dialog.setWindowTitle('Error')
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()   # exec_() to claim the thread and stop the main program from running


class InfoDialog:
    """
    A dialog that will pop up to display info. this dialog is not blocking, meaning the main thread will continue.
    """
    def __init__(self, message):
        self.message = message
        self.open_window()

    def open_window(self) -> None:
        """
        sets up the window with the provided info message and shows it.
        :return: None
        """
        self.info_dialog = QMessageBox()
        self.info_dialog.setText(self.message)
        self.info_dialog.setWindowTitle('info')
        self.info_dialog.show()       # show() to allow the program thread to keep running

    def close_window(self) -> None:
        """
        closes the window
        :return: None
        """
        if self.info_dialog is not None:
            self.info_dialog.accept()  # Close the dialog
