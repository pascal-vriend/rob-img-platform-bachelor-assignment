from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QLabel, QFileDialog, QSizePolicy


class SidebarWidget:
    def __init__(self, module_name, can_load_data=True):
        self.can_load_data = can_load_data
        self.main_widget: QWidget
        self.toggle_widget: QWidget
        self.datalabel_widget: QWidget
        self.toggle_button: QPushButton
        self.load_data_button: QPushButton
        self.loaded_data: list['DataCard']
        # set up the widget
        self.setup(module_name)

    def setup(self, name: str) -> None:
        """
        sets up the visuals of the widget
        :param name: Name of the module
        :return: None
        """
        self.toggledown_icon = QIcon()
        self.toggledown_icon.addFile(u"GUI/icons/arrow_down_white.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toggleup_icon = QIcon()
        self.toggleup_icon.addFile(u"GUI/icons/arrow_up_white.svg", QSize(), QIcon.Normal, QIcon.Off)
        ###############################################################################################################
        # main widget
        ###############################################################################################################
        main_widget: QWidget = QWidget()
        self.main_widget = main_widget
        module_layout = QVBoxLayout(main_widget)
        module_layout.setSpacing(0)
        module_layout.setContentsMargins(0, 0, 0, 0)
        # toggle button
        toggle_button = QPushButton(main_widget)
        self.toggle_button = toggle_button
        toggle_button.setLayoutDirection(Qt.RightToLeft)
        toggle_button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        toggle_button.setObjectName(u"toggle_button")
        toggle_button.setStyleSheet(u"#toggle_button{\n"
                                    "text-align:left;\n"
                                    "padding:5px;\n"
                                    "padding-right:80px;\n"
                                    "background-color: #3a3b3d;\n"
                                    "color: #ffffff;\n"
                                    "}\n"

                                    "#toggle_button:hover {\n"
                                    "background-color: #4e4f50;\n"
                                    "}")
        # if the module can load data, it should have a dropdown icon
        if self.can_load_data:
            toggle_button.setIcon(self.toggledown_icon)
        toggle_button.setText(name)
        module_layout.addWidget(toggle_button)

        # set up the dropdown widget if the module can load data
        if self.can_load_data:
            self.setup_dropdown_widget()

    def setup_dropdown_widget(self) -> None:
        """
        sets up the dropdown widget that holds data cards and the + button for adding data.
        :return: None
        """
        toggle_widget = QWidget()
        toggle_widget_layout = QVBoxLayout(toggle_widget)
        toggle_widget_layout.setSpacing(0)
        toggle_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.toggle_widget = toggle_widget

        # widget that holds the data labels inside the toggle widget
        datalabel_widget = QWidget(toggle_widget)
        datalabel_widget_layout = QVBoxLayout(datalabel_widget)
        datalabel_widget_layout.setSpacing(0)
        datalabel_widget_layout.setContentsMargins(0, 0, 0, 0)
        toggle_widget_layout.addWidget(datalabel_widget)
        self.datalabel_widget = datalabel_widget

        # button to load new data in the module inside the toggle widget
        load_data_button = QPushButton()
        self.load_data_button = load_data_button
        load_data_button.setObjectName(u"load_data_button")
        font = QFont()
        font.setPointSize(8)
        load_data_button.setFont(font)
        load_data_button.setStyleSheet(u"#load_data_button{\n"
                                       "background-color:#242527;\n"
                                       "color:#ffffff\n"
                                       "}\n"
                                       "#load_data_button:hover{\n"
                                       "font-size:15px;\n"
                                       "}")
        load_data_button.setFlat(True)
        load_data_button.setText(u"+")
        toggle_widget_layout.addWidget(load_data_button)

    def add_datacard(self, filename: str) -> 'DataCard':
        """
        Adds a data card with the filename to the dropdown widget.
        :param filename: the name of the file to be added
        :return: the DataCard object itself.
        """
        datacard = DataCard(self.datalabel_widget, filename)
        self.datalabel_widget.layout().addWidget(datacard)
        return datacard

    def remove_datacard(self, datacard: 'DataCard') -> None:
        """
        removes a DataCard object from the dropdown widget
        :param datacard: the DataCard to be removed
        :return: None
        """
        self.datalabel_widget.layout().removeWidget(datacard)

    def get_load_data_button(self) -> QPushButton:
        """
        :return: the load data button
        """
        return self.load_data_button

    def get_toggle_button(self) -> QPushButton:
        """
        :return: the main button in this widget for toggling the module on or off.
        """
        return self.toggle_button

    def toggle_module_on(self) -> None:
        """
        if the module can load data, the dropdown widget will be displayed and the icon will be changed.
        :return: None
        """
        if self.can_load_data:
            self.toggle_button.setIcon(self.toggleup_icon)
            self.main_widget.layout().addWidget(self.toggle_widget)

    def toggle_module_off(self) -> None:
        """
        If the module can load data, the dropdown widget will be hidden and the icon will be changed.
        :return: None
        """
        if self.can_load_data:
            self.toggle_button.setIcon(self.toggledown_icon)
            self.main_widget.layout().removeWidget(self.toggle_widget)

    def get_widget(self) -> QWidget:
        """
        :return: returns the main widget.
        """
        return self.main_widget


class DataCard(QWidget):
    """
    class for a widget displaying a file alongside a trash icon to delete that file from the UI.
    The data cards will be displayed in the dropdown widget.
    """
    def __init__(self, parent_widget, filename):
        super().__init__(parent_widget)
        self.filename = filename
        # main frame that holds the button and label
        self.setStyleSheet(u"background-color:#transparent")
        loaded_data_layout = QHBoxLayout(self)
        loaded_data_layout.setContentsMargins(5, 5, 0, 5)

        # the label of the file name
        datalabel = QLabel(self)
        datalabel.setStyleSheet(u"color:#ffffff")
        datalabel.setText(filename)
        loaded_data_layout.addWidget(datalabel, 0, Qt.AlignLeft)

        # button to delete the loaded data
        self.delete_data_button = QPushButton(self)
        self.delete_data_button.setStyleSheet(u"background-color:transparent;")
        icon = QIcon()
        icon.addFile(u"GUI/icons/trashcan_white.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.delete_data_button.setIcon(icon)
        self.delete_data_button.setText("")
        loaded_data_layout.addWidget(self.delete_data_button, 0, Qt.AlignRight)

    def get_delete_button(self):
        """
        :return: the button to delete the file
        """
        return self.delete_data_button

    def get_filename(self):
        """
        :return: the filename of this data card
        """
        return self.filename
