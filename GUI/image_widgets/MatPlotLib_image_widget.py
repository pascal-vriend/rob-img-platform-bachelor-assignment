import numpy
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib import animation

from GUI.image_widgets.abstract_image_widget import AbstractImageWidget
from GUI.popups import ErrorDialog
from GUI.settings import PlotSettingsDialog

from data_manager import Data
import custom_math as cm
import matplotlib.style as mplstyle
mplstyle.use('fast')
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from pandas import DataFrame


class MplCanvas(FigureCanvas):
    """
    the canvas utilized by the matplotlib image widget
    """
    def __init__(self, parent, width=4, height=4, dpi=100, ):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)


class MatPlotLibImageWidget(AbstractImageWidget):
    """
    image widget for the matplotlib module.
    """
    def __init__(self):
        super().__init__()
        self.loaded_data_dict = {}
        self.animator = None
        self.animations: list[Animation] = []
        self.setup()

    def setup(self) -> None:
        """
        Sets up the main visuals of the widget including the toolbar.
        Also initiates a MPL canvas and adds a FuncAnimation
        :return: None
        """
        self.main = QWidget()

        layout = QVBoxLayout(self.main)
        self.main.setContentsMargins(0, 0, 0, 0)
        # Create a Matplotlib canvas widget
        self.canvas = MplCanvas(self.main)
        layout.addWidget(self.canvas)
        # add an animation
        self.animator = animation.FuncAnimation(self.canvas.fig, self.animate, cache_frame_data=False, interval=10)

        # Create the navigation toolbar and add it to the layout
        self.toolbar = NavigationToolbar(self.canvas, self.main)
        self.toolbar.setStyleSheet("""
            QLabel, QPushButton, QComboBox, QLineEdit {
                color: #ffffff;
            }
            QToolButton:hover {
                background-color: #4e4f50;
            }
            QToolButton:checked {
                background-color: #4e4f50;
            }
            
        """)

        # 242527
        self.toolbar.setIconSize(QSize(24, 24))
        # Set custom icons for toolbar actions
        for action in self.toolbar.actions():
            if action.text() == 'Home':
                action.setIcon(QIcon("GUI/icons/home_white.svg"))
            elif action.text() == 'Customize':
                action.setIcon(QIcon("GUI/icons/graph_settings_white.png"))
            elif action.text() == 'Subplots':
                action.setIcon(QIcon("GUI/icons/graph_white.png"))
            elif action.text() == 'Save':
                action.setIcon(QIcon("GUI/icons/save_white.svg"))
            elif action.text() == 'Pan':
                action.setIcon(QIcon("GUI/icons/move_white.svg"))
            elif action.text() == 'Zoom':
                action.setIcon(QIcon("GUI/icons/search_white.svg"))
        layout.addWidget(self.toolbar)

    def update_animation_data(self, filename: str, data:DataFrame) -> None:
        """
        updates the data inside the animations and keeps the last 100 values to improve efficiëncy
        :param filename: the filename of the data, which is also the name of the animation.
        :param data: the dataframe containing the newly obtained data from the connection
        :return: None
        """
        x = cm.df_column_to_numpy(data, 0)
        y = cm.df_column_to_numpy(data, 1)
        for animation in self.animations:
            if animation.name == filename:
                animation.x = numpy.append(animation.x, x)[-100:]
                animation.y = numpy.append(animation.y, y)[-100:]
                return
        # if no animation was found, add a new one
        new_animation = Animation(filename, x, y)
        self.animations.append(new_animation)

    def animate(self, i) -> None:
        """
        callback for the FuncAnimator. this method plots the animations by updating the data in of the line.
        :param i:
        :return: None
        """
        all_x = []
        all_y = []

        for ani in self.animations:
            if ani.line:
                ani.line.set_data(ani.x, ani.y)
            else:
                ani.line, = self.canvas.axes.plot(ani.x, ani.y)
            all_x.extend(ani.x)
            all_y.extend(ani.y)

        if all_x and all_y:
            self.rescale_axes()
        self.canvas.draw()

    def plot(self, data_object: Data) -> None:
        """
        plot data from a data_object.
        :param data_object: the data object containing the filename and the dataframe
        :return: None
        """
        data: DataFrame = data_object.data
        filename: str = data_object.filename
        plot_labels = data.columns
        column_count = len(plot_labels)
        # do not plot the same data twice.
        if self.is_plotted(filename) and column_count <= 2:
            return
        try:

            x_label = data.axes[1][0]  # label of the first column
            y_label = None
            # check the amount of data and decide which data to plot
            if column_count <= 1:
                ErrorDialog(f"Error: The DataFrame of {filename} does not have enough columns.")
            elif column_count == 2:
                y_label = data.axes[1][1]  # label of the second column
            else:
                dialog = PlotSettingsDialog(plot_labels[1:])
                result = dialog.exec()
                if result != dialog.Accepted:
                    return
                else:
                    y_label = dialog.get_selected_option()

            # fetch the data points
            x_data = cm.df_column_to_numpy(data, 0)  # always take the first column for x_data
            y_column_index = data.columns.get_loc(y_label)  # get the index of the selected y_label
            y_data = cm.df_column_to_numpy(data, y_column_index)

            line, = self.canvas.axes.plot(x_data, y_data)
            self.add_to_data_dict(line, filename)

            self.set_xlabel(x_label)
            self.set_ylabel(y_label)
            self.rescale_axes()
            self.canvas.draw()
        except IndexError:
            ErrorDialog(f"Error: The DataFrame of {filename} does not have enough columns with data.")
        except TypeError:
            ErrorDialog(f"Error: Invalid data type encountered in {filename}")
        except Exception as e:
            ErrorDialog(f"An unexpected error occurred: {e}")

    def rescale_axes(self) -> None:
        """
        Automatically rescales the axes based on the current lines in the plot.
        :return: None
        """
        self.canvas.axes.relim()
        self.canvas.axes.set_xticks(self.calculate_ticks(self.canvas.axes.get_xlim()))
        self.canvas.axes.autoscale()

    def calculate_ticks(self, xlim):
        """
        Calculate and return appropriate x-axis ticks based on the current limits.
        :param xlim: The current limits of the x-axis.
        :return: List of tick positions.
        """
        min_x, max_x = xlim
        range_x = max_x - min_x
        # Set tick interval based on the range of x
        if range_x <= 10:
            tick_interval = 0.2
        elif range_x <= 100:
            tick_interval = 10
        else:
            tick_interval = int(range_x // 10)
        return numpy.arange(min_x, max_x + tick_interval, tick_interval)

    def add_to_data_dict(self, line, filename) -> None:
        """
        Adds a line to the plotted data dictionary.
        :param line: the line object
        :param filename: the filename that is associated with the plotted line
        :return: None
        """
        if filename in self.loaded_data_dict:
            self.loaded_data_dict[filename].append(line)
        else:
            self.loaded_data_dict[filename] = [line]

    def remove_from_plot(self, filename) -> None:
        """
        remove a line from the plot.
        :param filename: the filename associated with the line
        :return: None
        """

        if self.is_plotted(filename):
            try:
                lines = self.loaded_data_dict.pop(filename)
                for line in lines:
                    line.remove()
                self.rescale_axes()
                self.canvas.draw()
            except KeyError:
                ErrorDialog(f"Could not remove plot with data from '{filename}'.")

    def is_plotted(self, filename):
        """
        check if a file is plotted
        :param filename: the file to be checked
        :return: True if plotted, else False.
        """
        return filename in self.loaded_data_dict

    def clear(self) -> None:
        """
        clear all lines in the plot
        :return: None
        """
        self.canvas.axes.clear()
        self.canvas.draw()

    def set_figure_title(self, title: str) -> None:
        """
        set the title of the figure
        :param title: the title
        :return: None
        """
        self.canvas.axes.set_title(title)
        self.canvas.draw()

    def set_xlabel(self, label: str) -> None:
        """
        sets the x label of the figure
        :param label: the x label
        :return: None
        """
        self.canvas.axes.set_xlabel(label)
        self.canvas.draw()

    def set_ylabel(self, label) -> None:
        """
        sets the y label of the figure
        :param label: the y label
        :return: None
        """
        self.canvas.axes.set_ylabel(label)
        self.canvas.draw()

    def get_widget(self):
        """
        :return: the main widget
        """
        return self.main


class Animation:
    """
    A class that holds all information about an animation such as the data and the name of the animation, which will be
    the same as the device name that send the data in realtime.
    """
    def __init__(self, name:str, x: numpy.ndarray, y: numpy.ndarray):
        self.name = name
        self.x = x
        self.y = y
        self.line = None
