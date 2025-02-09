import json
import socket

from PySide2.QtGui import QIntValidator

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QLineEdit, QComboBox, \
    QDialogButtonBox


def update_json_file(file: str, new_settings: dict) -> None:
    """
    universal method to update a json file with new content.
    :param file: the path to the file
    :param new_settings: the new settings.
    :return: None
    """
    try:
        with open(file, 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {}

    settings.update(new_settings)

    with open(file, 'w') as f:
        json.dump(settings, f, indent=4)


class SettingsDialog(QDialog):
    """
    class for the settings dialog, that will open upon clicking the gear icon in the bottom left of the gui.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.settings_file = 'settings.json'

        # Create layout and add widgets
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # port settings
        self.port_widget = QWidget(self)
        self.port_layout = QHBoxLayout(self.port_widget)
        #   Qlabel
        self.port_label = QLabel("internet settings")
        self.port_layout.addWidget(self.port_label)
        #   line edit for ip
        self.ip_line_edit = QLineEdit()
        self.ip_line_edit.setPlaceholderText("ip-address")
        self.ip_line_edit.setMaxLength(15)
        self.port_layout.addWidget(self.ip_line_edit)
        #   line edit for port
        self.port_edit = QLineEdit(self)
        self.port_edit.setPlaceholderText("port number")
        self.port_edit.setValidator(QIntValidator(0, 65535, self))
        self.port_layout.addWidget(self.port_edit)
        layout.addWidget(self.port_widget)

        # OK Button to close the dialog
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(lambda: self.save_settings_on_close())
        layout.addWidget(self.ok_button, 0, Qt.AlignRight)

        # load the previously saved settings:
        self.load_settings()

    def save_settings_on_close(self) -> None:
        """
        saves the settings upon closing the dialog
        :return:
        """
        self.save_settings()
        self.close()

    def save_settings(self) -> None:
        """
        fetches the settings from the dialog and writes them to the jason file
        :return: None
        """
        ip_address = self.ip_line_edit.text()
        port = self.port_edit.text()

        new_settings = {
            "ip-address": ip_address,
            "port": port
        }

        update_json_file(self.settings_file, new_settings)

    def load_settings(self) -> None:
        """
        makes sure that upon opening the settings dialog, the previously saved settings will be displayed.
        :return: None
        """
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.ip_line_edit.setText(settings.get("ip-address", ""))
                self.port_edit.setText(settings.get("port", ""))
        except FileNotFoundError:
            pass


class FilterSettingsDialog(QDialog):
    """
    Filter settings dialog to set the settings for the butterworth filter in the matplotlib module.
    """

    def __init__(self, field_style, button_style):
        super().__init__()
        self.setWindowTitle("Filter Settings")
        self.settings_file = "settings.json"
        self.field_style = field_style
        self.button_style = button_style
        self.setup()

    def setup(self) -> None:
        """
        sets up the main visuals for the dialog
        :return: None
        """
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.filter_widget = QWidget(self)
        self.filter_layout = QVBoxLayout(self.filter_widget)
        self.filter_widget.setLayout(self.filter_layout)
        layout.addWidget(self.filter_widget)

        # Combobox for filter types
        self.filter_type = QComboBox(self.filter_widget)
        self.filter_type.setStyleSheet(self.field_style)
        self.filter_type.addItems(['low', 'high', 'band', 'stop'])
        self.filter_layout.addWidget(self.filter_type)

        # Line edit for cutoff
        self.cutoff = QLineEdit(self.filter_widget)
        self.cutoff.setPlaceholderText("cutoff (comma separated for band)")
        self.cutoff.setStyleSheet(self.field_style)
        self.filter_layout.addWidget(self.cutoff)

        # Line edit for sampling frequency
        self.sampling_frequency = QLineEdit(self.filter_widget)
        self.sampling_frequency.setPlaceholderText("sampling frequency)")
        self.sampling_frequency.setStyleSheet(self.field_style)
        self.filter_layout.addWidget(self.sampling_frequency)

        # Line edit for order
        self.order = QLineEdit(self.filter_widget)
        self.order.setPlaceholderText("order")
        self.order.setStyleSheet(self.field_style)
        self.filter_layout.addWidget(self.order)

        # OK Button to close the dialog
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(lambda: self.save_settings_on_close())
        layout.addWidget(self.ok_button, 0, Qt.AlignRight)

        # load the previously saved settings:
        self.load_settings()

    def save_settings_on_close(self) -> None:
        """
        saves the settings upon closing the dialog
        :return: None
        """
        self.save_settings()
        self.close()

    def save_settings(self) -> None:
        """
        fetches the settings from the dialog and writes them to the jason file
        :return: None
        """
        filter_type = self.filter_type.currentText()
        cutoff = self.cutoff.text()
        sampling_frequency = self.sampling_frequency.text()
        order = self.order.text()

        new_settings = {
            "filter-type": filter_type,
            "sampling-frequency": sampling_frequency,
            "filter-cutoff": cutoff,
            "filter-order": order
        }
        update_json_file(self.settings_file, new_settings)

    def load_settings(self) -> None:
        """
        makes sure that upon opening the settings dialog, the previously saved settings will be displayed.
        :return: None
        """
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.filter_type.setCurrentText(settings.get("filter-type", "low"))
                self.order.setText(settings.get("filter-order", ""))
                self.cutoff.setText(settings.get("filter-cutoff", ""))
                self.sampling_frequency.setText(settings.get("sampling-frequency", ""))
        except FileNotFoundError:
            pass


class DeviceSettings(QDialog):
    """
    A class for the settings dialog in which you can connect to devices.
    """
    SUPPORTED_BAUD_RATES = [1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

    def __init__(self, available_ports, field_style, button_style):
        super().__init__()
        self.setWindowTitle("Device Settings")
        self.settings_file = "settings.json"
        self.available_ports = available_ports
        self.field_style = field_style
        self.button_style = button_style
        self.setup()

    def setup(self) -> None:
        """
        sets up the main visuals for the dialog
        :return: None
        """
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        ###############################################################################################################
        # internet widget
        ###############################################################################################################
        self.internet_widget = QWidget(self)
        self.internet_layout = QVBoxLayout(self.internet_widget)
        self.internet_widget.setObjectName("frame")
        self.internet_widget.setStyleSheet("#frame { border: 1px solid black; }")
        #   Qlabel
        self.port_label = QLabel("internet settings")
        self.internet_layout.addWidget(self.port_label, 0, Qt.AlignCenter)
        # settings widget
        self.internet_settings_widget = QWidget(self.internet_widget)
        self.internet_settings_layout = QHBoxLayout(self.internet_settings_widget)
        #   line edit for ip
        self.ip_line_edit = QLineEdit(self.internet_settings_widget)
        self.ip_line_edit.setPlaceholderText("ip-address")
        self.ip_line_edit.setMaxLength(15)
        self.internet_settings_layout.addWidget(self.ip_line_edit)
        #   line edit for port
        self.port_edit = QLineEdit()
        self.port_edit.setPlaceholderText("port number")
        self.port_edit.setValidator(QIntValidator(0, 65535, self.internet_settings_widget))
        self.internet_settings_layout.addWidget(self.port_edit)
        self.internet_layout.addWidget(self.internet_settings_widget)
        # connect internet button
        self.connect_internet_button = QPushButton()
        self.connect_internet_button.setText("connect")
        self.internet_layout.addWidget(self.connect_internet_button)
        layout.addWidget(self.internet_widget)

        ###############################################################################################################
        # serial widget
        ###############################################################################################################
        self.serial_widget = QWidget(self)
        self.serial_layout = QVBoxLayout(self.serial_widget)
        self.serial_widget.setObjectName("frame")
        self.serial_widget.setStyleSheet("#frame { border: 1px solid black; }")
        #   Qlabel
        self.serial_label = QLabel("serial connection")
        self.serial_layout.addWidget(self.serial_label, 0, Qt.AlignCenter)
        # serial settings widget
        self.serial_settings_widget = QWidget(self.serial_widget)
        self.serial_settings_layout = QHBoxLayout(self.serial_settings_widget)
        #   Combobox for port type
        self.serial_port_box = QComboBox()
        for port in self.available_ports:
            self.serial_port_box.addItem(port)
        self.serial_settings_layout.addWidget(self.serial_port_box)
        #   Combobox for baud rate
        self.baud_rate_box = QComboBox()
        for baud_rate in self.SUPPORTED_BAUD_RATES:
            self.baud_rate_box.addItem(str(baud_rate))
        self.serial_settings_layout.addWidget(self.baud_rate_box)
        self.serial_layout.addWidget(self.serial_settings_widget)
        # connect serial button
        self.connect_serial_button = QPushButton()
        self.connect_serial_button.setText("connect")
        self.serial_layout.addWidget(self.connect_serial_button)
        layout.addWidget(self.serial_widget)

        # OK Button to close the dialog
        self.ok_button = QPushButton("OK")
        layout.addWidget(self.ok_button, 0, Qt.AlignRight)

        # load the previously saved settings:
        self.load_settings()

    def load_settings(self):
        """
        makes sure that upon opening the settings dialog, the previously saved settings will be displayed.
        :return: None
        """
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.ip_line_edit.setText(settings.get("ip-address", ""))
                self.port_edit.setText(settings.get("port", ""))
                current_baud_rate_index = self.baud_rate_box.findText(settings.get("baud-rate", "1200"))
                self.baud_rate_box.setCurrentIndex(current_baud_rate_index)
        except FileNotFoundError:
            pass

    def get_connect_internet_button(self):
        """
        :return: the button to connect to the provided internet address
        """
        return self.connect_internet_button

    def get_connect_serial_button(self):
        """
        :return: the button to connect to the selected serial device
        """
        return self.connect_serial_button

    def get_ok_button(self):
        """
        :return: The ok button which closes the dialog
        """
        return self.ok_button


class PlotSettingsDialog(QDialog):
    def __init__(self, options):
        super().__init__()
        self.setWindowTitle('Plot Settings')
        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.label.setText("multiple data sets were found. Please select one to plot")
        self.layout.addWidget(self.label)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(options)
        self.layout.addWidget(self.combo_box)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_selected_option(self):
        return self.combo_box.currentText()
