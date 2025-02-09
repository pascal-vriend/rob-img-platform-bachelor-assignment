from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QScrollArea, QCheckBox

from GUI.control_widgets.abstract_control_widget import AbstractControlWidget


class ConnectionControlWidget(AbstractControlWidget):

    def __init__(self):
        super().__init__()
        self.connected_devices = []
        self.main_widget: QWidget
        self.setup()

    def setup(self) -> None:
        """
        sets up the visuals for the control panel
        :return: None
        """

        self.setup_basis(module_name="realtime data")
        # refresh button
        self.add_device_button = QPushButton(self.left_content)
        self.add_device_button.setStyleSheet(self.button_style)
        self.add_device_button.setText("add device")
        self.left_layout.addWidget(self.add_device_button, 0, Qt.AlignTop)

        # Scroll Area for the device list
        self.scroll_area = QScrollArea(self.left_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(300, 130)
        #   main widget in the scroll area
        self.device_list_widget = QWidget(self.scroll_area)
        self.device_list_layout = QVBoxLayout(self.device_list_widget)
        #   widget for table info
        self.info_widget = QWidget(self.device_list_widget)
        self.info_widget_layout = QHBoxLayout(self.info_widget)
        #       device label
        self.device_label = QLabel(self.info_widget)
        self.device_label.setText("device")
        self.device_label.setStyleSheet("color:#ffffff")
        self.info_widget_layout.addWidget(self.device_label, 1, Qt.AlignLeft)
        #       is being plotted label
        self.plot_label = QLabel(self.info_widget)
        self.plot_label.setText("plot")
        self.plot_label.setStyleSheet("color:#ffffff")
        self.info_widget_layout.addWidget(self.plot_label, 1, Qt.AlignRight)
        self.device_list_layout.addWidget(self.info_widget, 0, Qt.AlignTop)

        self.scroll_area.setWidget(self.device_list_widget)
        self.left_layout.addWidget(self.scroll_area, 0, Qt.AlignBottom)

    def add_device(self, device_name) -> None:
        """
        add a device to the device list in this widget
        :param device_name: the name of the connected device
        :return: None
        """
        device = Device(device_name)
        self.connected_devices.append(device)
        self.refresh_device_list()

    def refresh_device_list(self) -> None:
        """
        refresh the device list by removing all current devices in the list and reloading them from the
         connected_devices list
        :return: None
        """
        # Clear the existing device list
        for i in reversed(range(self.device_list_layout.count() - 1)):
            widget = self.device_list_layout.itemAt(i + 1).widget()  # +1 because there is a widget for the info labels
            if widget is not None:
                widget.setParent(None)

        # Add the refreshed list of devices
        for device in self.connected_devices:
            self.device_list_layout.addWidget(device.get_widget(), 1, Qt.AlignTop)

    def remove_device(self, device_name) -> None:
        """
        remove a specific device from the list by its name.
        :param device_name: the name of the device to be removed.
        :return: None
        """
        device = self.get_device(device_name)
        self.connected_devices.remove(device)
        self.refresh_device_list()

    def get_device(self, device_name: str) -> 'Device':
        """
        get a device object by its name
        :param device_name: the name of the devices, determined by the connection type
        :return: the device object
        """
        for device in self.connected_devices:
            if device.name == device_name:
                return device

    def get_add_device_button(self) -> QPushButton:
        """
        :return: the button that opens the connection dialog
        """
        return self.add_device_button


class Device:
    """
    a widget for displaying a device in the device list.
    """
    def __init__(self, device_name: str):
        self.main = QWidget()
        self.name = device_name
        self.is_plotting = False
        self.layout = QHBoxLayout(self.main)

        self.label = QLabel(self.main)
        self.label.setText(device_name)
        self.label.setStyleSheet("color:#ffffff;")
        self.checkbox = QCheckBox(self.main)
        self.main.setStyleSheet("background-color: #3a3b3d")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checkbox, 0, Qt.AlignRight)

    def get_widget(self) -> QWidget:
        """
        :return: the main widget
        """
        return self.main

    def is_active(self) -> bool:
        """
        :return: True if the plot data checkbox is checked, else False
        """
        return self.checkbox.isChecked()
