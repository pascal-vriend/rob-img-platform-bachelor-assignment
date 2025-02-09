from PySide2.QtWidgets import QFileDialog, QWidget, QPushButton

from GUI.popups import ErrorDialog
from GUI.sidebar import SidebarWidget, DataCard
from GUI.image_widgets.abstract_image_widget import AbstractImageWidget
from GUI.control_widgets.abstract_control_widget import AbstractControlWidget
from data_manager import DataManager


class AbstractModule:
    """
    Abstract class for modules. Some basic functionality is included. This class should be extended by actual modules.
    """

    def __init__(self, module_name: str, allowed_file_tpes: list[str] = None, has_image_widget=True,
                 has_control_panel=True, can_load_data=True) -> None:
        self.has_image_widget = has_image_widget
        self.has_control_panel = has_control_panel
        self.can_load_data = can_load_data
        self.is_active: bool = False
        self.allowed_file_types: list[str] = allowed_file_tpes
        self.data_manager: DataManager
        self.image_widget: AbstractImageWidget
        self.control_widget: AbstractControlWidget
        self.sidebar_widget: SidebarWidget = SidebarWidget(module_name, can_load_data)
        self.set_widgets()
        self.set_load_data_callback()

    def set_widgets(self) -> None:
        """
        loads abstract widgets. In reality, when a module should have one of these widgets, the field will be
        overwritten by the actual implemented widget. If this is not done, a widget displaying "Not Implemented"
        will be shown as a warning.
        :return: None
        """
        if self.has_image_widget:
            self.image_widget = AbstractImageWidget()
        if self.has_control_panel:
            self.control_widget = AbstractControlWidget()

    def set_load_data_callback(self) -> None:
        """
        fetches the + button from the sidebar widget and connects it to the open file dialog method in this class.
        :return: None
        """
        if self.sidebar_widget.can_load_data:
            self.sidebar_widget.get_load_data_button().clicked.connect(lambda: self.open_file_dialog())

    def get_image_widget(self) -> QWidget:
        """
        :return: the main widget for the image panel
        """
        return self.image_widget.get_widget()

    def get_control_widget(self) -> QWidget:
        """
        :return: the main widget for the control panel
        """
        return self.control_widget.get_widget()

    def get_sidebar_widget(self) -> QWidget:
        """
        :return: the sidebar widget, which holds the dropdown button
        """
        return self.sidebar_widget.get_widget()

    # toggle functions
    def get_toggle_button(self) -> QPushButton:
        """
        :return: The toggle button inside the sidebar widget
        """
        return self.sidebar_widget.get_toggle_button()

    def toggle_sidebar_on(self) -> None:
        """
        Toggles the module on by calling the method inside the sidebar widget class
        :return: None
        """
        self.sidebar_widget.toggle_module_on()

    def toggle_sidebar_off(self) -> None:
        """
        Toggles the module off by calling the method inside the sidebar widget class
        :return: None
        """
        self.sidebar_widget.toggle_module_off()

    def open_file_dialog(self) -> None:
        """
        Opens the file dialog and tries to load the data in the file manager
        """
        if self.allowed_file_types is None:
            ErrorDialog("this module cannot open files since it has no allowed file types")
            return
        # set up a filter for the file dialog with the allowed file types
        file_types_filter = " ".join([f"*.{file_type}" for file_type in self.allowed_file_types])
        formatted_filter = f"Allowed Files ({file_types_filter})"
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        # open the dialog
        filepath, _ = QFileDialog.getOpenFileName(self.get_sidebar_widget(), "Open File", "", formatted_filter,
                                                  options=options)
        if filepath != "":  # returns an empty filepath if the dialog was closed
            self.load_data(filepath)

    def load_data(self, filepath, is_volume=False) -> None:
        """
        load data into the DataManager and if successful, add it to the widgets in the ui.
        :param filepath: the path to the file
        :param is_volume: Whether the filepath points to a directory containing DICOM files for a volume
        :return: None
        """
        # try to load the selected file in the data manager
        if is_volume:
            filename = self.data_manager.open_dicom_directory(filepath)
            pass
        else:
            filename = self.data_manager.load_data(filepath)
        if filename is not None:
            self.add_file_to_widgets(filename, is_volume)

    def add_file_to_widgets(self, filename, is_volume=False) -> None:
        """
        Adds file to the widgets in the ui.
        :param filename: The name that will be displayed in the widgets
        :param is_volume: Whether the filepath points to a directory containing DICOM files for a volume
        :return: None
        """
        # If this function was called from outside of this class, and the module cannot load data, there should not be
        # added files to the widgets:
        if not self.can_load_data:
            ErrorDialog("this module cannot load data")
            return

        if filename is not None:
            # add the data to the control widget
            if is_volume:
                self.control_widget.add_directory(filename)
            else:
                self.control_widget.add_data(filename)

            # create a new datacard for the sidebar and connect its delete button
            data_card = self.sidebar_widget.add_datacard(filename)
            delete_button = data_card.get_delete_button()
            delete_button.clicked.connect(lambda: self.remove_file(data_card))
        else:
            ErrorDialog("failed to load data")

    def plot_data(self, image_widget: AbstractImageWidget, filename) -> None:
        """
        Plots data from the file to the provided image widget.
        :param image_widget: The image widget that should display the data
        :param filename: the name of the file that holds the data
        :return:
        """
        if filename == "":
            ErrorDialog("please load a file")
        else:
            data = self.data_manager.get_data_object_by_filename(filename)
            if data is not None:
                image_widget.plot(data)

    def remove_file(self, datacard: DataCard) -> None:
        """
        Remove a file from the ui and Datamanager. This method is a callback for the delete button inside the data card
        :param datacard: The data card that holds the delete button and the file name
        :return: None
        """
        filename = datacard.get_filename()
        self.data_manager.remove_data_by_filename(filename)
        self.control_widget.remove_data_by_filename(filename)
        self.image_widget.remove_from_plot(filename)
        self.sidebar_widget.remove_datacard(datacard)
