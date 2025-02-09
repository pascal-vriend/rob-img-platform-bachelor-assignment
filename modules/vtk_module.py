from typing import Callable

from PySide2.QtWidgets import QFileDialog

from GUI.popups import ErrorDialog
from modules.abstract_module import AbstractModule
from GUI.control_widgets.VTK_control_widget import VTKControlWidget
from GUI.image_widgets.VTK_image_widget import VTKImageWidget


class VTKModule(AbstractModule):
    """
    Module to display volumetric data.
    """
    def __init__(self, data_manager):
        self.allowed_file_types: list[str] = ["vtk", "vtu", "vtp", "vti", "stl", "obj", "ply", "jpg", "jpeg",
                                              "png", "tif", "dicom", "nii", "nii.gz", "mhd", "DCM"]
        self.module_name: str = "VTK"
        self.data_manager = data_manager
        self.image_widget: VTKImageWidget
        self.control_widget: VTKControlWidget
        super().__init__(self.module_name, self.allowed_file_types)
        self.setup()

    def setup(self) -> None:
        """
        Sets up the widgets and links the button callbacks.
        :return: None
        """
        self.image_widget = VTKImageWidget()
        self.control_widget = VTKControlWidget()

        #add callbacks
        self.control_widget.get_plot_button().clicked.connect(self.set_plot_callback())
        self.control_widget.get_clear_button().clicked.connect(self.set_clear_callback())
        self.control_widget.get_reset_camera_button().clicked.connect(self.set_reset_camera_callback())
        self.control_widget.get_set_color_button().clicked.connect(self.set_mesh_color_callback())
        self.control_widget.get_erase_button().clicked.connect(self.set_erase_callback())
        self.control_widget.get_opacity_button().clicked.connect(self.set_opacity_callback())
        self.control_widget.get_opacity_slider().valueChanged.connect(self.set_slider_callback())
        self.control_widget.get_open_dicom_directory_button().clicked.connect(self.set_open_dicom_directory_callback())
        self.control_widget.get_plot_volume_button().clicked.connect(self.set_plot_volume_callback())
        self.control_widget.get_erase_volume_button().clicked.connect(self.set_erase_volume_callback())

    def set_plot_callback(self) -> Callable[[], None]:
        """
        plots the data by calling plot_data in the super class.
        :return:
        """
        return lambda: self.plot_data(self.image_widget, self.control_widget.get_choose_data_combo().currentText())

    def set_clear_callback(self) -> Callable[[], None]:
        """
        Clears the canvas by calling the clear method in the image widget
        :return:
        """
        return lambda: self.image_widget.clear()

    def set_reset_camera_callback(self) -> Callable[[], None]:
        """
        Resets the camera by calling the reset camera method in the image widget
        :return:
        """
        return lambda: self.image_widget.reset_camera()

    def set_mesh_color_callback(self) -> Callable[[], None]:
        """
        Sets the color of the mesh by calling the set_mesh_color method in the image widget.
        It retrieves the mesh itself from the combo box and the color from the control widget.
        :return:
        """
        return lambda: self.image_widget.set_mesh_color(self.control_widget.get_choose_data_combo().currentText(),
                                                        self.control_widget.get_mesh_color())

    def set_erase_callback(self) -> Callable[[], None]:
        """
        removes a normal mesh from the plot by calling the remove_from_plot method in the image widget.
        it fetches the mesh to remove from the combo box in the control widget.
        :return:
        """
        return lambda: self.image_widget.remove_from_plot(self.control_widget.get_choose_data_combo().currentText())

    def set_opacity_callback(self) -> Callable[[], None]:
        """
        sets the opacity of a mesh by calling the set_opacity method in this class.
        :return:
        """
        return lambda: self.set_opacity()

    def set_slider_callback(self) -> Callable[[], None]:
        """
        displays the current value of the slider besides the slider in the control widget.
        :return:
        """
        return lambda: self.control_widget.get_opacity_label().setText(
                                                            str(self.control_widget.get_opacity_slider().value()) + "%")

    def set_open_dicom_directory_callback(self) -> Callable[[], None]:
        """
        opens the dialog for loading directories by callign the open_dicom_dialog method in this class.
        :return:
        """
        return lambda: self.open_dicom_dialog()

    def set_plot_volume_callback(self) -> Callable[[], None]:
        """
        plots a volume by calling the plot_volume method in this class.
        :return:
        """
        return lambda: self.plot_volume()

    def set_erase_volume_callback(self) -> Callable[[], None]:
        """
        removes a volume from the plot by calling the remove_from_plot method in the image widget.
        it fetches the volume to remove from the dicom combo box.
        :return:
        """
        return lambda: self.image_widget.remove_from_plot(self.control_widget.get_dicom_combo().currentText())

    # normal function

    def set_opacity(self) -> None:
        """
        sets the opacity of a mesh.
        :return:
        """
        opacity = self.control_widget.get_opacity_slider().value()/100
        filename = self.control_widget.get_choose_data_combo().currentText()
        self.image_widget.set_mesh_opacity(filename, opacity)

    def open_dicom_dialog(self) -> None:
        """
        loads a directory into the DataManager
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory = QFileDialog.getExistingDirectory(self.get_sidebar_widget(), "Open Directory", "", options=options)
        if directory:  # returns an empty string if the dialog was closed
            self.load_data(directory, is_volume=True)

    def plot_volume(self) -> None:
        """
        plots a volume by fetching it from the DataManager and calling the plot volume method in the image widget.
        :return:
        """
        file = self.control_widget.get_dicom_combo().currentText()
        if not file:
            ErrorDialog("load a dicom directory and select it")
            return
        data = self.data_manager.get_data_object_by_filename(file).data
        self.image_widget.plot_volume(data, file)
