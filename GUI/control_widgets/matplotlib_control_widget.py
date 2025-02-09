from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QHBoxLayout, QLabel

from GUI.control_widgets.abstract_control_widget import AbstractControlWidget
from GUI.settings import FilterSettingsDialog


class MatPlotLibControlWidget(AbstractControlWidget):

    def __init__(self):
        super().__init__()
        self.main_widget: QWidget
        self.setup()

    def setup(self) -> None:
        """
        sets up the visuals for the control panel
        :return: None
        """
        ###############################################################################################################
        # main window widget
        ###############################################################################################################
        self.setup_basis(module_name="MatPlotLib")
        ###############################################################################################################
        # left content
        ###############################################################################################################


        # plot widget
        self.plot_widget = QWidget(self.left_content)
        self.plot_widget_layout = QHBoxLayout(self.plot_widget)
        self.plot_widget_layout.setContentsMargins(0, 0, 0, 0)
        #          combobox
        self.choose_data = QComboBox(self.plot_widget)
        self.choose_data.setStyleSheet(self.field_style)
        self.combobox_size_policy.setHeightForWidth(self.choose_data.sizePolicy().hasHeightForWidth())
        self.choose_data.setSizePolicy(self.combobox_size_policy)
        self.plot_widget_layout.addWidget(self.choose_data)
        #          erase button
        self.erase_button = QPushButton(self.plot_widget)
        self.erase_icon = QIcon()
        self.erase_icon.addFile(u"GUI/icons/eraser_white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.erase_button.setIcon(self.erase_icon)
        self.plot_widget_layout.addWidget(self.erase_button, 0, Qt.AlignRight)
        #          plot button
        self.plot_button = QPushButton(self.plot_widget)
        self.plot_button.setText("plot")
        self.plot_button.setStyleSheet(self.button_style)
        self.plot_widget_layout.addWidget(self.plot_button, 0, Qt.AlignRight)
        self.left_layout.addWidget(self.plot_widget)
        # title edit widget
        self.title_edit_widget = QWidget(self.left_content)
        self.title_edit_layout = QHBoxLayout(self.title_edit_widget)
        self.title_edit_layout.setSpacing(6)
        self.title_edit_layout.setContentsMargins(0, 0, 0, 0)
        #   line edit
        self.title_edit = QLineEdit(self.title_edit_widget)
        self.title_edit.setPlaceholderText("title")
        self.title_edit.setStyleSheet(self.field_style)
        self.title_edit_layout.addWidget(self.title_edit)
        #   button
        self.title_button = QPushButton(self.title_edit_widget)
        self.title_button.setText("set title")
        self.title_button.setStyleSheet(self.button_style)
        self.title_edit_layout.addWidget(self.title_button)
        self.left_layout.addWidget(self.title_edit_widget)

        # ylabel edit
        self.ylabel_widget = QWidget(self.left_content)
        self.ylabel_layout = QHBoxLayout(self.ylabel_widget)
        self.ylabel_layout.setSpacing(6)
        self.ylabel_layout.setContentsMargins(0, 0, 0, 0)
        #   line edit
        self.ylabel_edit = QLineEdit(self.title_edit_widget)
        self.ylabel_edit.setPlaceholderText("ylabel")
        self.ylabel_edit.setStyleSheet(self.field_style)
        self.ylabel_layout.addWidget(self.ylabel_edit)
        #   button
        self.ylabel_button = QPushButton(self.ylabel_widget)
        self.ylabel_button.setText("set ylabel")
        self.ylabel_button.setStyleSheet(self.button_style)
        self.ylabel_layout.addWidget(self.ylabel_button)
        self.left_layout.addWidget(self.ylabel_widget)

        # xlabel edit
        self.xlabel_widget = QWidget(self.left_content)
        self.xlabel_layout = QHBoxLayout(self.xlabel_widget)
        self.xlabel_layout.setSpacing(6)
        self.xlabel_layout.setContentsMargins(0, 0, 0, 0)
        #   line edit
        self.xlabel_edit = QLineEdit(self.xlabel_widget)
        self.xlabel_edit.setPlaceholderText("xlabel")
        self.xlabel_edit.setStyleSheet(self.field_style)
        self.xlabel_layout.addWidget(self.xlabel_edit)
        #   button
        self.xlabel_button = QPushButton(self.title_edit_widget)
        self.xlabel_button.setText("set ylabel")
        self.xlabel_button.setStyleSheet(self.button_style)
        self.xlabel_layout.addWidget(self.xlabel_button)
        self.left_layout.addWidget(self.xlabel_widget)

        # clear plot button
        self.clear_button = QPushButton(self.left_content)
        self.clear_button.setText("clear graph")
        self.clear_button.setStyleSheet(self.button_style)
        self.left_layout.addWidget(self.clear_button)



        ###############################################################################################################
        # right content
        ###############################################################################################################
        # main widget
        self.right_content = QWidget(self.control_content_holder)
        self.right_layout = QVBoxLayout(self.right_content)
        self.right_layout.setContentsMargins(5, 5, 5, 5)

        # widget to convolve two data vectors with each other
        self.convolve_widget = QWidget(self.right_content)
        self.convolve_layout = QHBoxLayout(self.convolve_widget)
        self.convolve_layout.setContentsMargins(0, 0, 0, 0)
        #    combo box
        self.convolve_data = QComboBox(self.convolve_widget)
        self.convolve_data.setStyleSheet(self.field_style)
        self.combobox_size_policy.setHeightForWidth(self.convolve_data.sizePolicy().hasHeightForWidth())
        self.convolve_data.setSizePolicy(self.combobox_size_policy)
        self.convolve_layout.addWidget(self.convolve_data)
        #    convolve button
        self.convolve_button = QPushButton(self.convolve_widget)
        self.convolve_button.setText("convolve")
        self.convolve_button.setStyleSheet(self.button_style)
        self.convolve_layout.addWidget(self.convolve_button, 0, Qt.AlignRight)
        self.right_layout.addWidget(self.convolve_widget, 0, Qt.AlignTop)

        # limit widget to set a lower and upper limit for data
        self.limit_widget = QWidget(self.right_content)
        self.limit_layout = QHBoxLayout(self.limit_widget)
        self.limit_layout.setSpacing(6)
        self.limit_layout.setContentsMargins(0, 0, 0, 0)
        #    widget to hold the settings
        self.limit_settings = QWidget(self.limit_widget)
        self.limit_settings_layout = QHBoxLayout(self.limit_settings)
        self.limit_settings_layout.setContentsMargins(0, 0, 0, 0)
        #       min value field
        self.limit_min = QLineEdit(self.limit_settings)
        self.limit_min.setStyleSheet(self.field_style)
        self.limit_min.setPlaceholderText("min")
        self.limit_settings_layout.addWidget(self.limit_min)
        #       max value field
        self.limit_max = QLineEdit(self.limit_settings)
        self.limit_max.setPlaceholderText("max")
        self.limit_max.setStyleSheet(self.field_style)
        self.limit_settings_layout.addWidget(self.limit_max)
        self.limit_layout.addWidget(self.limit_settings)
        #    limit button
        self.limit_button = QPushButton(self.limit_widget)
        self.limit_button.setText("limit")
        self.limit_button.setStyleSheet(self.button_style)
        self.limit_layout.addWidget(self.limit_button)
        self.right_layout.addWidget(self.limit_widget, 0, Qt.AlignTop)

        # filter widget to apply a butter filter to the data that is selected
        self.filter_widget = QWidget(self.right_content)
        self.filter_layout = QHBoxLayout(self.filter_widget)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        #   open settings button
        self.filter_settings_button = QPushButton(self.filter_widget)
        self.filter_settings_button.setText("open filter settings")
        self.filter_settings_button.setStyleSheet(self.button_style)
        self.filter_settings_button.clicked.connect(lambda: self.open_filter_dialog())
        self.filter_layout.addWidget(self.filter_settings_button)
        #   filter button to apply the filter
        self.filter_button = QPushButton(self.filter_widget)
        self.filter_button.setText("filter")
        self.filter_button.setStyleSheet(self.button_style)
        self.filter_layout.addWidget(self.filter_button)
        self.right_layout.addWidget(self.filter_widget, 0, Qt.AlignTop)

        # add the content
        self.content_layout.addWidget(self.right_content, 0, Qt.AlignLeft)

    def add_data(self, filename: str) -> None:
        """
        :param filename: the filename that will be added to the combo boxes
        :return: None
        """
        self.get_choose_data_combo().addItem(filename)
        self.get_convolve_data_combo().addItem(filename)

    def remove_data_by_filename(self, filename: str) -> None:
        """
        remove a file from the combo boxes
        :param filename: the name of the file to be removed
        :return: None
        """
        choose_data_box = self.get_choose_data_combo()
        convolve_data_box = self.get_convolve_data_combo()
        index = choose_data_box.findText(filename)
        if index != -1:  # If the string is found in the combobox
            choose_data_box.removeItem(index)
        index = convolve_data_box.findText(filename)
        if index != -1:  # If the string is found in the combobox
            convolve_data_box.removeItem(index)

    def open_filter_dialog(self) -> None:
        """
        open the dialog for setting the filter settings
        :return: None
        """
        self.filter_settings_dialog = FilterSettingsDialog(self.field_style, self.button_style)
        self.filter_settings_dialog.exec_()

    # Button getters
    def get_erase_button(self) -> QPushButton:
        """
        :return: the button to erase a line from the plot
        """
        return self.erase_button

    def get_plot_button(self) -> QPushButton:
        """
        :return: the button to plot a line
        """
        return self.plot_button

    def get_title_button(self) -> QPushButton:
        """
        :return: the button to set the title
        """
        return self.title_button

    def get_xlabel_button(self) -> QPushButton:
        """
        :return: the button to set the x label
        """
        return self.xlabel_button

    def get_ylabel_button(self) -> QPushButton:
        """
        :return: the button to set the y label
        """
        return self.ylabel_button

    def get_clear_button(self) -> QPushButton:
        """
        :return: the button to clear the entire canvas
        """
        return self.clear_button

    def get_convolve_button(self) -> QPushButton:
        """
        :return: the button to compute and plot the convolution of the two selected data sets
        """
        return self.convolve_button

    def get_limit_button(self) -> QPushButton:
        """
        :return: the button for limiting the data selected in the combo box
        """
        return self.limit_button

    def get_filter_button(self) -> QPushButton:
        """
        :return: the button to filter the data selected in the combo box
        """
        return self.filter_button

    # QLineEdit getters

    def get_title_edit(self) -> str:
        """
        :return: the field to get the title
        """
        return self.title_edit.text()

    def get_xlabel_edit(self) -> str:
        """
        :return: the field to get the x label
        """
        return self.xlabel_edit.text()

    def get_ylabel_edit(self) -> str:
        """
        :return: the field to get the y label
        """
        return self.ylabel_edit.text()

    def get_limit_min_edit(self) -> str:
        """
        :return: the field to get the minimal value for the limit
        """
        return self.limit_min.text()

    def get_limit_max_edit(self) -> str:
        """
        :return: the field to get the maximal value for the limit
        """
        return self.limit_max.text()

    # QComboBox getters

    def get_choose_data_combo(self) -> QComboBox:
        """
        :return: the combo box for choosing data to plot
        """
        return self.choose_data

    def get_convolve_data_combo(self):
        """
        :return: the combo box for choosing data to convolve
        """
        return self.convolve_data

