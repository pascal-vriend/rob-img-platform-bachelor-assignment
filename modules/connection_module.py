import serial.tools.list_ports

from GUI.popups import ErrorDialog
from GUI.settings import DeviceSettings
from GUI.control_widgets.connection_control_widget import ConnectionControlWidget
from GUI.image_widgets.MatPlotLib_image_widget import MatPlotLibImageWidget
from connections import InternetConnection, AbstractConnection, SerialConnection
import pandas as pd
import threading
import time

from data_manager import DataManager
from modules.abstract_module import AbstractModule


class ConnectionModule(AbstractModule):
    """
    Module to establish connections with devices and handle the incomming data.
    """
    def __init__(self, data_manager, matplotlib_image_widget):
        self.module_name: str = "Realtime data"
        self.settings_file = "settings.json"
        super().__init__(self.module_name, has_image_widget=False, can_load_data=False)
        self.connections = {}
        self.data_manager = data_manager
        self.image_widget = matplotlib_image_widget
        self.control_widget: ConnectionControlWidget
        self.setup()

    def setup(self) -> None:
        """
        initializes the control widget and sets the callback for the connection dialog.
        :return: None
        """
        self.control_widget = ConnectionControlWidget()
        # callbacks
        self.control_widget.get_add_device_button().clicked.connect(lambda: self.open_connection_dialog())

    def open_connection_dialog(self) -> None:
        """
        opens the dialog for connecting to devices. It first scans the ports to detected available serial devices and
        then adds them to the dialog.
        :return: None
        """
        available_ports = [comport.device for comport in serial.tools.list_ports.comports()]
        dialog = DeviceSettings(available_ports, self.control_widget.button_style, self.control_widget.field_style)
        dialog.get_connect_internet_button().clicked.connect(lambda: self.create_internet_connection(dialog))
        dialog.get_connect_serial_button().clicked.connect(lambda: self.create_serial_connection(dialog))
        dialog.get_ok_button().clicked.connect(lambda: self.refresh_on_close_callback(dialog))
        dialog.show()

    def create_internet_connection(self, dialog) -> None:
        """
        Create an internet connection
        :param dialog: the dialog that holds the settings such as ip and port
        :return: None
        """
        ip_address = dialog.ip_line_edit.text()
        port = dialog.port_edit.text()
        device_name = ip_address + ":" + port

        if device_name in self.connections:
            ErrorDialog("Already connected to this device")
            return
        # set up the connection
        connection = InternetConnection(ip_address, port)
        # try to connect to it
        if not connection.connect():
            ErrorDialog(f"failed to connect to {ip_address}:{port}")
            return
        # on success
        self.add_connection(device_name, connection)

    def create_serial_connection(self, dialog) -> None:
        """
        create a serial connection
        :param dialog: the dialog that holds the settings such as port and baud rate
        :return: None
        """
        port = dialog.serial_port_box.currentText()
        baud_rate = dialog.baud_rate_box.currentText()
        device_name = port

        if device_name in self.connections:
            ErrorDialog("Already connected to this device")
            return
        # set up the connection
        connection = SerialConnection(port, baud_rate)
        # try to connect to it
        if not connection.connect():
            ErrorDialog(f"failed to connect to {port} with baudrate {baud_rate}")
            return
        # on success
        self.add_connection(device_name, connection)

    def refresh_on_close_callback(self, dialog) -> None:
        """
        close the dialog and refresh the device list displayed in the control panel.
        :param dialog: the dialog for adding connections
        :return: None
        """
        dialog.close()
        self.control_widget.refresh_device_list()

    def add_connection(self, device_name: str, connection: AbstractConnection) -> None:
        """
        Creates a thread that reads from the connection and adds the connection to the connections list.
        :param device_name: the name of the device
        :param connection: the connection object itself
        :return: None
        """
        # create a new thread for that connection:
        thread = PlotThread(connection, self.data_manager, self.image_widget, self.control_widget, sample_rate=0.01)
        thread.start()
        # on success:
        self.connections[device_name] = {
            'connection': connection,
            'thread': thread
        }
        self.control_widget.add_device(device_name)  # add to device list the control manager
        self.control_widget.refresh_device_list()  # refresh the device list

    def stop_thread(self):
        for device_name, resources in self.connections.items():
            resources['connection'].close()
            resources['thread'].stop()


class PlotThread(threading.Thread):
    """
    A thread that will read data from a connection and plot it in the image widget.
    """
    def __init__(self, connection, data_manager, image_widget, control_widget, sample_rate=1.0):
        super().__init__()
        self._running = True
        self.lock = threading.Lock()
        self.data_manager: DataManager = data_manager
        self.image_widget: MatPlotLibImageWidget = image_widget
        self.control_widget = control_widget
        self.connection = connection
        self.sample_rate = sample_rate

    def run(self) -> None:
        """
        The main method that will be called by the thread. It will read the data and call the plot function.
        :return: None
        """
        while self._running:
            # check if the device is still connected
            if not self.connection.connected:
                ErrorDialog(f"connection to {self.connection.device_name} was lost")
                self.stop()
                return
            data_buffer = []  # Buffer data for this connection
            data = self.connection.read_data()
            device_name = self.connection.device_name
            # check if there is data and if it should be plotted
            if self.control_widget.get_device(device_name).is_active() and data:
                data_buffer.extend(data.split('\n'))
            # Process and plot buffered data
            if data_buffer:     # will be empty if the device is inactive or there was no data
                self.plot_data(data_buffer, device_name)
            time.sleep(self.sample_rate)

    def plot_data(self, data_buffer, device_name) -> None:
        """
        plot data from the buffer, by parsing the points and creating a dataframe out of it.
        :param data_buffer: the buffer that holds the data points
        :param device_name: the name of the device, which will also be the name of the animation in the image widget
        :return: None
        """
        data_list = []
        for point in data_buffer:
            if ',' in point:
                try:
                    x, y = map(float, point.split(','))
                    data_list.append((x, y))
                except ValueError:
                    continue
        if data_list:
            pd_data = pd.DataFrame(data_list)
            self.image_widget.update_animation_data(device_name, pd_data)

    def stop(self) -> None:
        """
        stop the thread
        :return: None
        """
        self._running = False
        self.join()
