
import socket
from typing import Union

import serial
#import rospy
from GUI.popups import ErrorDialog, InfoDialog
# from std_msgs.msg import String


class AbstractConnection:
    """
    Template for a connection. If any of the methods below is not implemented,
    the newly made connection class is not sufficient.
    """
    def __init__(self):
        self.device_name: str = None
        self.connected: bool = False

    def connect(self):
        raise NotImplemented

    def read_data(self):
        raise NotImplemented

    def close(self):
        raise NotImplemented


class InternetConnection(AbstractConnection):
    """
    A class for establishing an internet connection.
    """
    def __init__(self, ip_address, port):
        """
        constructor for the internet connection
        :param ip_address: the ipv4 address of the connection
        :param port: the port of the connection
        """
        super().__init__()
        self.ip_address = ip_address
        self.port = int(port)
        self.device_name = ip_address + ":" + port  # device name will follow this standard, so it can be compared to
        # existing connections
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.connected = False

    def connect(self) -> bool:
        """
        connect to the internet address and port.
        :return: true if successful, false if an error occurred during connection
        """
        # display a blocking info dialog that shows a connection is being established to prevent button spam.
        info_dialog = InfoDialog("connecting")
        try:
            self.sock.connect((self.ip_address, self.port))
            self.connected = True
            return True
        except Exception:
            return False
        finally:
            info_dialog.close_window()

    def read_data(self) -> Union[str, None]:
        """
        Reads data from the connection in utf-8 format
        :return: the data in utf-8 format if successful, else None is returned
        """
        if self.connected:
            try:
                data = self.sock.recv(1024)
                return data.decode('utf-8')
            except socket.timeout:
                self.close()
                return None
            except Exception as e:
                ErrorDialog(f"error while reading data from connection: {self.device_name}, error : {e}")
                self.close()
                return None
        else:
            return None

    def close(self) -> None:
        """
        Closes the connection
        :return: None
        """
        self.connected = False
        self.sock.close()


class SerialConnection(AbstractConnection):
    """
    A class for establishing a serial connection.
    """
    def __init__(self, port, baudrate, timeout=1):
        """
        constructor for the serial connection
        :param port: the port to which the device is connected
        :param baudrate: the baud rate of the device
        :param timeout: standard timeout of 1
        """
        super().__init__()
        self.device_name = port  # device name will follow this standard, so it can be compared to existing connections
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.connected = False

    def connect(self) -> bool:
        """
        connect to the serial device through the port.
        :return: true if successful, false if an error occurred during connection
        """
        info_dialog = InfoDialog("connecting")
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.connected = True
            return True
        except Exception:
            return False
        finally:
            info_dialog.close_window()

    def read_data(self) -> Union[str, None]:
        """
        read data from the serial connection
        :return: the data in utf-8 format if successful, else None is returned
        """
        if self.connected:
            try:
                data = self.serial.readline().decode('utf-8')
                return data
            except serial.SerialTimeoutException:
                self.close()
                return None
            except Exception:
                ErrorDialog(f"error while reading data from connection: {self.device_name}")
                self.connected = False
                return None
        else:
            return None

    def close(self) -> None:
        """
        Closes the serial connection
        :return: None
        """
        if self.serial and self.serial.isOpen():
            self.serial.close()
        self.connected = False


# class ROSConnection(AbstractConnection):
#     def __init__(self, node_name, topic_name, message_type=String):
#         super().__init__()
#         self.node_name = node_name
#         self.topic_name = topic_name
#         self.message_type = message_type
#         self.connected = False
#         self.data = None
#
#     def connect(self) -> bool:
#         try:
#             rospy.init_node(self.node_name, anonymous=True)
#             self.subscriber = rospy.Subscriber(self.topic_name, self.message_type, self.callback)
#             self.connected = True
#             return True
#         except rospy.ROSException as e:
#             ErrorDialog(f"Failed to connect to ROS topic {self.topic_name}: {str(e)}")
#             return False
#
#     def callback(self, msg):
#         self.data = msg.data
#
#     def read_data(self):
#         if self.connected:
#             return self.data
#         else:
#             return None
#
#     def close(self):
#         if self.connected:
#             rospy.signal_shutdown("Closing ROS connection")
#             self.connected = False
