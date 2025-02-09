from PySide2.QtCore import (QMetaObject, QSize, Qt)
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *

from GUI.settings import SettingsDialog


# modules
from modules.abstract_module import AbstractModule
from modules.vtk_module import VTKModule
from modules.matplotlib_module import MatPlotLibModule
from modules.connection_module import ConnectionModule
# data manager
from data_manager import DataManager


class UiMainWindow(object):
    def __init__(self) -> None:
        self.data_manager = DataManager()
        self.vtk = VTKModule(self.data_manager)
        self.mpl = MatPlotLibModule(self.data_manager)
        self.con = ConnectionModule(self.data_manager, self.mpl.image_widget)
        self.modules: list[AbstractModule] = [self.vtk, self.mpl, self.con]

    ###############################################################################################################
    ###############################################################################################################
    #                                                                                                             #
    #                                           SETUP FUNCTIONS                                                   #
    #                                                                                                             #
    ###############################################################################################################
    ###############################################################################################################

    def setupUi(self, MainWindow) -> None:
        """
        Sets up the main window of the GUI. The GUI consists of a left side that is the sidebar menu and
        a right side that has the image widget and the control widget.
        :param MainWindow: the main window that will be displayed.
        :return: None
        """
        ###############################################################################################################
        # main window widget
        ###############################################################################################################
        MainWindow.resize(913, 605)
        window_icon = QIcon()
        window_icon.addFile(u"GUI/icons/app_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(window_icon)
        self.centralwidget = QWidget(MainWindow)
        self.main_layout = QGridLayout(self.centralwidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        ###############################################################################################################
        # right side
        ###############################################################################################################
        self.rightMenu = QWidget(self.centralwidget)
        self.right_menu_layout = QVBoxLayout(self.rightMenu)
        self.right_menu_layout.setSpacing(0)
        self.right_menu_layout.setContentsMargins(0, 0, 0, 0)
        # image widget on right side
        self.setup_image_widget()
        # control widget on right side
        self.setup_control_widget()
        ###############################################################################################################
        # left menu widget
        ###############################################################################################################
        self.setup_sidebar()
        self.rightMenu.setStyleSheet(u"background-color:#3a3b3d")
        ###############################################################################################################
        # add all widgets to the main window
        ###############################################################################################################
        self.main_layout.addWidget(self.leftMenu, 0, 0, 1, 1)
        self.main_layout.addWidget(self.rightMenu, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle(u"IntraVision")
        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi
    def setup_sidebar(self) -> None:
        """
        sets up the visuals of the sidebar and loads the sidebar widgets for each module in the ui.
        :return: None
        """
        self.leftMenu = QWidget(self.centralwidget)
        self.leftMenu.setMaximumSize(QSize(200, 16777215))
        self.leftMenu.setStyleSheet(u"background-color: #242527")
        self.left_menu_layout = QVBoxLayout(self.leftMenu)
        self.left_menu_layout.setSpacing(5)
        self.left_menu_layout.setContentsMargins(0, 20, 0, 0)

        for module in self.modules:
            # add each module to the sidebar
            self.left_menu_layout.addWidget(module.get_sidebar_widget(), 0, Qt.AlignTop)
            # connect each button to call back that controls the image and control widget
            module.get_toggle_button().clicked.connect(self.set_toggle_callback(module))

        # add a spacer that pushes modules to the top.
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.left_menu_layout.addItem(self.verticalSpacer)

        #settings button
        icon = QIcon()
        icon.addFile(u"GUI/icons/settings_white.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settings_button = QPushButton(icon, "", self.leftMenu)
        self.settings_button.setStyleSheet("background-color: #3a3b3d")
        self.settings_button.clicked.connect(self.set_settings_callback())
        self.left_menu_layout.addWidget(self.settings_button, 0, Qt.AlignLeft)

    def setup_image_widget(self) -> None:
        """
        sets up the main container for the image widgets
        :return: None
        """
        self.image_widget = QWidget(self.rightMenu)
        self.image_widget_layout = QHBoxLayout(self.image_widget)
        self.image_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.image_widget_layout.setSpacing(0)
        self.image_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.right_menu_layout.addWidget(self.image_widget)

    def setup_control_widget(self) -> None:
        """
        sets up the main container for the control widget
        :return: None
        """
        self.control_widget = QWidget(self.rightMenu)
        self.control_widget_layout = QHBoxLayout(self.control_widget)
        self.right_menu_layout.addWidget(self.control_widget)

    ###############################################################################################################
    ###############################################################################################################
    #                                                                                                             #
    #                                           NORMAL FUNCTIONS                                                  #
    #                                                                                                             #
    ###############################################################################################################
    ###############################################################################################################

    def set_settings_callback(self):
        """
        callback for opening the settings dialog
        :return: None
        """
        return lambda: self.open_settings_dialog()

    def open_settings_dialog(self) -> None:
        """
        creates the settings dialog and executes it
        :return: None
        """
        self.settings_dialog = SettingsDialog()
        self.settings_dialog.exec_()

    def set_toggle_callback(self, module: AbstractModule):
        """
        callback for toggling a module on or off.
        :param module: the module to be toggled
        :return: None
        """
        return lambda: self.toggle_module(module)

    def toggle_module(self, module: AbstractModule) -> None:
        """
        Toggles a module either on or off, depending on the current state.
        :param module: The module to be toggled
        :return: None
        """
        if module.has_image_widget:
            self.toggle_image_widget(module)
        if module.has_control_panel:
            self.toggle_control_widget(module)
        self.toggle_sidebar_widget(module)
        module.is_active = not module.is_active

    def toggle_image_widget(self, module: AbstractModule) -> None:
        """
        toggles the image widget of the module on or off, depending on the state
        :param module: the module of which the image widget should be toggled.
        :return: None
        """
        image_widget = module.get_image_widget()
        if module.is_active:
            self.image_widget.layout().removeWidget(image_widget)
            image_widget.hide()
        else:
            self.image_widget.layout().addWidget(image_widget)
            image_widget.show()

    @staticmethod
    def toggle_sidebar_widget(module: AbstractModule) -> None:
        """
        toggles the sidebar widget by calling the proper methods based on the current state.
        :param module: The module of which the sidebar widget should be toggled
        :return: None
        """
        if module.is_active:
            module.toggle_sidebar_off()
        else:
            module.toggle_sidebar_on()

    def toggle_control_widget(self, module: AbstractModule) -> None:
        """
        toggles the control widget of the module on or off, depending on the state
        :param module: the module of which the control widget should be toggled.
        :return: None
        """
        control_widget = module.get_control_widget()
        if module.is_active:
            self.control_widget.layout().removeWidget(control_widget)
            control_widget.hide()
        else:
            self.control_widget.layout().addWidget(control_widget)
            control_widget.show()

    def stop_threads_upon_close(self) -> None:
        """
        calls the stop thread method in the connection module on closing the application.
        :return: None
        """
        self.con.stop_thread()

