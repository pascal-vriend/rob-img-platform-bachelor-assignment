from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QHBoxLayout, QLabel, \
    QColorDialog, QSlider

from GUI.control_widgets.abstract_control_widget import AbstractControlWidget


class VTKControlWidget(AbstractControlWidget):

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
        self.setup_basis(module_name="VTK")
        ###############################################################################################################
        # left content
        ###############################################################################################################

        # plot widget
        self.plot_widget = QWidget(self.left_content)
        self.plot_widget_layout = QHBoxLayout(self.plot_widget)
        self.plot_widget_layout.setContentsMargins(0, 0, 0, 0)
        #   combobox
        self.choose_data = QComboBox(self.plot_widget)
        self.choose_data.setStyleSheet(self.field_style)
        self.combobox_size_policy.setHeightForWidth(self.choose_data.sizePolicy().hasHeightForWidth())
        self.choose_data.setSizePolicy(self.combobox_size_policy)
        self.plot_widget_layout.addWidget(self.choose_data)
        #   erase button
        self.erase_button = QPushButton(self.plot_widget)
        self.erase_icon = QIcon()
        self.erase_icon.addFile(u"GUI/icons/eraser_white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.erase_button.setIcon(self.erase_icon)
        self.erase_button.setStyleSheet(self.button_style)
        self.plot_widget_layout.addWidget(self.erase_button, 0, Qt.AlignRight)
        #   plot button
        self.plot_button = QPushButton(self.plot_widget)
        self.plot_button.setText("plot")
        self.plot_button.setStyleSheet(self.button_style)
        self.plot_widget_layout.addWidget(self.plot_button, 0, Qt.AlignRight)
        self.left_layout.addWidget(self.plot_widget)

        # opacity widget
        self.opacity_widget = QWidget(self.left_content)
        self.opacity_layout = QHBoxLayout(self.opacity_widget)
        self.opacity_layout.setSpacing(6)
        self.opacity_layout.setContentsMargins(0, 0, 0, 0)
        #   slider
        self.opacity_slider = QSlider(Qt.Horizontal, self.opacity_widget)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        self.opacity_layout.addWidget(self.opacity_slider)
        #   Qlabel
        self.opacity_label = QLabel(self.opacity_widget)
        self.opacity_label.setText("100%")
        self.opacity_label.setStyleSheet("color: #ffffff")
        self.opacity_layout.addWidget(self.opacity_label)
        self.left_layout.addWidget(self.opacity_widget)
        #   set opacity button
        self.opacity_button = QPushButton(self.opacity_widget)
        self.opacity_button.setText("set opacity")
        self.opacity_button.setStyleSheet(self.button_style)
        self.opacity_layout.addWidget(self.opacity_button, 0, Qt.AlignRight)
        self.left_layout.addWidget(self.opacity_widget)
        # mesh color widget
        self.color_widget = QWidget(self.left_content)
        self.color_layout = QHBoxLayout(self.color_widget)
        self.color_layout.setSpacing(6)
        self.color_layout.setContentsMargins(0, 0, 0, 0)
        #   pick color button:
        self.color_button = QPushButton(self.color_widget)
        self.color_button.setStyleSheet('background-color: #ffffff')
        self.color_button.clicked.connect(self.showColorDialog)
        self.color_layout.addWidget(self.color_button)
        #   set color button
        self.set_color_button = QPushButton(self.color_widget)
        self.set_color_button.setStyleSheet(self.button_style)
        self.set_color_button.setText("set mesh color")
        self.color_layout.addWidget(self.set_color_button, 0, Qt.AlignRight)
        self.left_layout.addWidget(self.color_widget)

        # reset camera button
        self.reset_camera_button = QPushButton(self.opacity_widget)
        self.reset_camera_button.setText("reset camera")
        self.reset_camera_button.setStyleSheet(self.button_style)
        self.left_layout.addWidget(self.reset_camera_button)

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
        # open dicom dialog
        self.open_dicom_dialog = QPushButton(self.right_content)
        self.open_dicom_dialog.setText("load dicom volume")
        self.open_dicom_dialog.setStyleSheet(self.button_style)
        self.right_layout.addWidget(self.open_dicom_dialog, 0, Qt.AlignTop)
        # combobox for volumes
        self.dicom_combobox = QComboBox(self.right_content)
        self.dicom_combobox.setStyleSheet(self.field_style)
        self.combobox_size_policy.setHeightForWidth(self.dicom_combobox.sizePolicy().hasHeightForWidth())
        self.dicom_combobox.setSizePolicy(self.combobox_size_policy)
        self.right_layout.addWidget(self.dicom_combobox, 0, Qt.AlignTop)

        # plot widget
        self.plot_volume_widget = QWidget(self.right_content)
        self.plot_volume_layout = QHBoxLayout(self.plot_volume_widget)
        self.plot_volume_layout.setContentsMargins(0, 0, 0, 0)
        #   plot dicom volume button
        self.plot_volume_button = QPushButton(self.plot_volume_widget)
        self.plot_volume_button.setText("plot")
        self.plot_volume_button.setStyleSheet(self.button_style)
        self.plot_volume_layout.addWidget(self.plot_volume_button)
        #   erase volume button
        self.erase_volume_button = QPushButton(self.plot_volume_widget)
        self.erase_volume_button.setIcon(self.erase_icon)
        self.erase_volume_button.setStyleSheet(self.button_style)
        self.plot_volume_layout.addWidget(self.erase_volume_button)
        # add the widget
        self.right_layout.addWidget(self.plot_volume_widget, 0, Qt.AlignTop)
        self.content_layout.addWidget(self.right_content, 0, Qt.AlignLeft)

    def showColorDialog(self) -> None:
        """
        Opens the color picking window and sets the picked value to self.mesh_color
        :return: None
        """
        color = QColorDialog.getColor()

        if color.isValid():
            self.color_button.setStyleSheet('background-color: %s;' % color.name())
            self.mesh_color = color.name()

    def add_data(self, filename: str) -> None:
        """
        adds data to the choose data combobox
        :param filename: the filename that will be displayed in the box
        :return: None
        """
        self.get_choose_data_combo().addItem(filename)

    def add_directory(self, directory:str) -> None:
        """
        adds a directory to the volume section for DICOM volumes
        :param directory: the path to the directory
        :return: None
        """
        self.dicom_combobox.addItem(directory)

    def remove_data_by_filename(self, filename: str) -> None:
        """
        remove data from the combo boxes
        :param filename: the name of the file that will be removed from the combo boxes
        :return: None
        """
        choose_data_box = self.get_choose_data_combo()
        index = choose_data_box.findText(filename)
        if index != -1:  # If the string is found in the combobox
            choose_data_box.removeItem(index)

        dicom_volume_box = self.dicom_combobox
        index = dicom_volume_box.findText(filename)
        if index != -1:  # If the string is found in the combobox
            dicom_volume_box.removeItem(index)

    def get_mesh_color(self) -> str:
        """
        :return: The current picked mesh color as a string in hex representation.
        """
        return self.mesh_color

    # Button getters
    def get_erase_button(self) -> QPushButton:
        """
        :return: the erase button used to remove normal plots
        """
        return self.erase_button

    def get_erase_volume_button(self) -> QPushButton:
        """
        :return: the erase button used to remove DICOM volumes
        """
        return self.erase_volume_button

    def get_plot_volume_button(self) -> QPushButton:
        """
        :return: the button for plotting DICOM files
        """
        return self.plot_volume_button

    def get_plot_button(self) -> QPushButton:
        """
        :return: the plot button used to plot all other data than DICOM volumes
        """
        return self.plot_button

    def get_opacity_button(self) -> QPushButton:
        """
        :return: the button to set the opacity of a mesh
        """
        return self.opacity_button

    def get_set_color_button(self) -> QPushButton:
        """
        :return: the button for setting the color of a mesh
        """
        return self.set_color_button

    def get_reset_camera_button(self) -> QPushButton:
        """
        :return: the button for resetting the camera angle
        """
        return self.reset_camera_button

    def get_clear_button(self) -> QPushButton:
        """
        :return: the button to clear the canvas
        """
        return self.clear_button

    def get_open_dicom_directory_button(self) -> QPushButton:
        """
        :return: the button to open the directory selector dialog
        """
        return self.open_dicom_dialog

    # QComboBox getter
    def get_choose_data_combo(self):
        """
        :return: the combo box containing all files that are not directories to a DICOM volume
        """
        return self.choose_data

    def get_dicom_combo(self):
        """
        :return: the combo box containing directories for a DICOM volume
        """
        return self.dicom_combobox

    # Qslider getter
    def get_opacity_slider(self):
        """
        :return: the slider that has the opacity setting
        """
        return self.opacity_slider

    # label getter
    def get_opacity_label(self):
        """
        :return: the label that displays the current value of the opacity slider
        """
        return self.opacity_label
