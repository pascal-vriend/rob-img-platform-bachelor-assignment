import json

from modules.abstract_module import AbstractModule
from GUI.image_widgets.MatPlotLib_image_widget import MatPlotLibImageWidget
from GUI.control_widgets.matplotlib_control_widget import MatPlotLibControlWidget
from GUI.popups import ErrorDialog

from data_manager import Data

import custom_math as cm


class MatPlotLibModule(AbstractModule):
    """
    Module to display 2-dimensional data.
    """
    def __init__(self, data_manager):
        self.allowed_file_types: list[str] = ["csv", "xlsx", "txt"]
        self.module_name: str = "MPL"
        self.data_manager = data_manager
        self.image_widget: MatPlotLibImageWidget
        self.control_widget: MatPlotLibControlWidget
        super().__init__(self.module_name, self.allowed_file_types)
        self.setup()

    def setup(self):
        """
        Sets up the widgets and links the button callbacks.
        :return: None
        """
        self.image_widget = MatPlotLibImageWidget()
        self.control_widget = MatPlotLibControlWidget()

        # add callbacks for buttons in the control panel
        self.control_widget.get_title_button().clicked.connect(self.set_title_callback())
        self.control_widget.get_xlabel_button().clicked.connect(self.set_xlabel_callback())
        self.control_widget.get_ylabel_button().clicked.connect(self.set_ylabel_callback())
        self.control_widget.get_plot_button().clicked.connect(self.set_plot_callback())
        self.control_widget.get_clear_button().clicked.connect(self.set_clear_callback())
        self.control_widget.get_convolve_button().clicked.connect(self.set_convolve_callback())
        self.control_widget.get_limit_button().clicked.connect(self.set_limit_callback())
        self.control_widget.get_filter_button().clicked.connect(self.set_filter_callback())
        self.control_widget.get_erase_button().clicked.connect(self.set_erase_callback())

    # callbacks:
    def set_title_callback(self):
        """
        sets the title of the plot by calling the set_figure_title method in the image widget.
        :return:
        """
        return lambda: self.image_widget.set_figure_title(self.control_widget.get_title_edit())

    def set_xlabel_callback(self):
        """
        sets the x label of the plot by calling the set_xlabel method in the image widget.
        :return:
        """
        return lambda: self.image_widget.set_xlabel(self.control_widget.get_xlabel_edit())

    def set_ylabel_callback(self):
        """
        sets the y label of the plot by calling the set_ylabel method in the image widget.
        :return:
        """
        return lambda: self.image_widget.set_ylabel(self.control_widget.get_ylabel_edit())

    def set_plot_callback(self):
        """
        plots data by calling the plot_data method in the super class.
        :return:
        """
        return lambda: self.plot_data(self.image_widget, self.control_widget.get_choose_data_combo().currentText())

    def set_clear_callback(self):
        """
        clears the canvas by calling the clear method in the image widget.
        :return:
        """
        return lambda: self.image_widget.clear()

    def set_convolve_callback(self):
        """
        computes the convolution of two data sets by calling the convolve method in this class.
        :return:
        """
        return lambda: self.convolve()

    def set_limit_callback(self):
        """
        limits the data by calling the limit method in this class.
        :return:
        """
        return lambda: self.limit()

    def set_filter_callback(self):
        """
        filters data by calling the filter method in this class.
        :return:
        """
        return lambda : self.filter()

    def set_erase_callback(self):
        """
        removes data from the plot by calling the remove_from_plot method in the image widget.
        :return:
        """
        return lambda: self.image_widget.remove_from_plot(self.control_widget.get_choose_data_combo().currentText())

    # other functions
    def convolve(self) -> None:
        """
        computes the convolution between two data sets.
        :return:
        """
        # grab the data objects from the combo boxes
        df1 = self.data_manager.get_data_object_by_filename(self.control_widget.get_choose_data_combo().currentText())
        df2 = self.data_manager.get_data_object_by_filename(self.control_widget.get_convolve_data_combo().currentText())

        if df1 is None or df2 is None:
            ErrorDialog("please select two files to convolve with each other")
            return

        # grab the y data from both data objects and convert to numpy vectors
        vector1 = cm.df_column_to_numpy(df1.data, 1)
        vector2 = cm.df_column_to_numpy(df2.data, 1)
        # convolve the vectors
        convolved_data = cm.convolve_data(vector1, vector2)
        # create a new filename for the convolved data
        new_filename = df1.filename + "_convolved_with_" + df2.filename
        # create a new Data instance that can be plotted and add it to data manager
        convolved_data_object = Data(new_filename, convolved_data)
        # add the data object to the filemanager manually
        self.data_manager.add_data(new_filename, convolved_data)
        # load the data to the sidebar and control widgets
        self.add_file_to_widgets(new_filename)
        # plot the convolved data
        self.image_widget.plot(convolved_data_object)

    def limit(self):
        """
        limits data between a minimal and maximal value.
        :return:
        """
        # fetch the data that is selected in the combo box
        df = self.data_manager.get_data_object_by_filename(self.control_widget.get_choose_data_combo().currentText())
        if df is None:
            ErrorDialog("please load a file")
            return
        filename = df.filename
        data = df.data
        # fetch the values for the settings
        try:
            min_value = float(self.control_widget.get_limit_min_edit())
            max_value = float(self.control_widget.get_limit_max_edit())
        except ValueError:
            ErrorDialog("please fill in a valid number")
            return
        # limit the data
        limited_data = cm.limit_data(data, min_value, max_value)
        # change the data inside the DataManager for the selected file
        self.data_manager.set_data_by_filename(df.filename, limited_data)
        # remove the old plot and plot it again to update the values
        if self.image_widget.is_plotted(filename):
            self.image_widget.remove_from_plot(filename)
            self.image_widget.plot(df)

    def filter(self) -> None:
        """
        filters data using a butterworth filter.
        :return:
        """
        # fetch the Dataframe using the selected file in the combo box
        df = self.data_manager.get_data_object_by_filename(self.control_widget.get_choose_data_combo().currentText())
        if df is None:
            ErrorDialog("please load a file")
            return
        filename = df.filename
        data = df.data

        # grab the filter settings from the settings file
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        try:
            filter_type = settings.get("filter-type", "low")            # default filter type = low
            sampling_frequency = float(settings.get("fs", 1000))        # default sampling frequency = 1000
            filter_order = int(settings.get("filter-order", 5))         # default filter order = 5

            if filter_type == "band":
                cutoff_string = settings.get("filter-cutoff", "0.2, 40.0")  # default cutoff = 0.2, 40.0
                cutoff_values = [float(c) for c in cutoff_string.split(",")]
                if len(cutoff_values) != 2:
                    raise ValueError("Bandpass filter requires two cutoff frequencies.")
                lowcut, highcut = cutoff_values
                filter_cutoff = (lowcut, highcut)
            else:
                filter_cutoff = float(settings.get("filter-cutoff", 0.2))  # default cutoff = 0.2
        except ValueError:
            ErrorDialog("please fill in a number for the order, sampling frequency and cutoff")
            return
        # apply the filter to the data
        filtered_data = cm.filter_data(data, filter_type, filter_cutoff, sampling_frequency, filter_order)
        # change the data inside the DataManager for the selected file
        self.data_manager.set_data_by_filename(df.filename, filtered_data)
        # remove the old plot and plot if again to update the values
        if self.image_widget.is_plotted(filename):
            self.image_widget.remove_from_plot(filename)
            self.image_widget.plot(df)

