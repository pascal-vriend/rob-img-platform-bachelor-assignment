from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout


class AbstractControlWidget:
    def __init__(self):
        self.main_widget: QWidget
        self.button_style = "background-color: #3a3b3d;color:#ffffff}:hover{background-color: #4e4f50;}"
        self.field_style = "background-color: #3a3b3d;color:#ffffff;border: none; color: #ffffff;"
        self.combobox_size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.setup_basis()

    def setup_basis(self, module_name="not implemented") -> None:
        """
        sets up the main container for the control widgets. it also displays "not implemented" if this method is called
        by the abstract control widget class.
        :param module_name: the name of the module that will be displayed above the control panel
        :return: None
        """
        # main widget that holds everything
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_widget.setStyleSheet(u"background-color: #242527")
        # label with module name
        self.module_label = QLabel()
        self.module_label.setStyleSheet(u"font-size:20px; color:#ffffff")
        self.module_label.setText(module_name)
        self.main_layout.addWidget(self.module_label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        # content beneath the label
        self.control_content_holder = QWidget()
        self.content_layout = QHBoxLayout(self.control_content_holder)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.left_content = QWidget(self.control_content_holder)
        self.left_layout = QVBoxLayout(self.left_content)
        self.left_layout.setContentsMargins(5, 5, 5, 5)
        # add the left content to the control widget
        self.content_layout.addWidget(self.left_content)
        self.main_layout.addWidget(self.control_content_holder)

    def get_widget(self) -> QWidget:
        """
        :return: the main widget
        """
        return self.main_widget

    def add_data(self, filename: str) -> None:
        """
        Incase a control widget has something like a combo box to select data to plot, this method should be overwritten
        """
        pass

    def remove_data_by_filename(self, filename: str) -> None:
        """
        Incase a control widget has something like a combo box to select data to plot, this method should be overwritten
        """
        pass

