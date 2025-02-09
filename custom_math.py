from typing import Union

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
from pandas import DataFrame

from GUI.popups import ErrorDialog
from GUI.settings import PlotSettingsDialog


def convolve_data(vector1: np.ndarray, vector2: np.ndarray) -> Union[DataFrame, None]:
    """
    Computes the convolution of two one-dimensional vectors with each other.
    :param vector1: the first data set
    :param vector2: the second data set
    :return: None if the data sets were incompatible, else a DataFrame with the result.
    """
    # Ensure that the input vectors are one-dimensional numpy arrays
    if vector1.ndim != 1 or vector2.ndim != 1:
        ErrorDialog("Both input vectors must be one-dimensional arrays.")
        return

    # Perform convolution
    convolved_array = np.convolve(vector1, vector2, mode='full')

    # Create an x-axis based on the new range of the result
    x_axis = np.arange(len(convolved_array))

    # Convert the convolved result to a pandas DataFrame
    convolved_df = pd.DataFrame({'x': x_axis, 'convolution': convolved_array})

    return convolved_df


def limit_data(data: DataFrame, min_value: float, max_value: float) -> DataFrame:
    """
    limits a dataset by a minimal and maximal value.
    :param data: A pandas DataFrame containing the data to be limited
    :param min_value:
    :param max_value:
    :return: the new DataFrame with the limited y values
    """
    col = fetch_column_from_user(data)
    y_data = df_column_to_numpy(data, col)
    limited_vector = np.clip(y_data, min_value, max_value)
    data.iloc[:, col] = limited_vector
    return data


def butter_filter(data: np.ndarray, filter_type: str, cutoff: Union[list, tuple, float], fs: float,
                  order: int = 5) -> np.ndarray:
    """
    Filters data using the predefined settings from the dialog and returns it as a numpy array
    :param data: The data to be filtered
    :param filter_type: the filter type, for example: low-pass, band-pass, etc.
    :param cutoff: the cutoff of the filter
    :param fs: the sampling frequency of the data
    :param order: the order of the filter, 5 by default
    :return: the filtered data
    """
    nyquist = 0.5 * fs
    normalized_cutoff = [c / nyquist for c in cutoff] if isinstance(cutoff, (list, tuple)) else cutoff / nyquist
    b, a = butter(order, normalized_cutoff, btype=filter_type)
    y = filtfilt(b, a, data)
    return y


def filter_data(data: pd.DataFrame, filter_type: str, cutoff: Union[list, tuple, float], fs: float,
                order: int = 5) -> pd.DataFrame:
    """
    filter the data using the provided settings
    :param data: The DataFrame
    :param filter_type: the filter type, for example: low-pass, band-pass, etc.
    :param cutoff: the cutoff of the filter
    :param fs: the sampling frequency of the data
    :param order: the order of the filter, 5 by default
    :return: the new data frame with the filter applied to the y data
    """
    col = fetch_column_from_user(data)
    y_data = df_column_to_numpy(data, col)

    filtered_vector = butter_filter(y_data, filter_type, cutoff, fs, order)
    data.iloc[:, col] = filtered_vector
    return data


def df_column_to_numpy(df: DataFrame, column_index: int) -> np.ndarray:
    """
    Extract a column from a DataFrame and convert it to a numpy array.
    :param df: The input pandas DataFrame.
    :param column_index: The index of the column to extract
    :return: The extracted column as a numpy array.
    """
    return df.iloc[:, column_index].values


def fetch_column_from_user(data) -> int:
    # check whether data has more than 1 column
    plot_labels = data.columns
    column_count = len(plot_labels)
    selected_col = 1
    # if more than 1 colum for y data, let the user choose
    if column_count < 2:
        selected_col = -1
    if column_count > 2:
        dialog = PlotSettingsDialog(plot_labels[1:])
        result = dialog.exec()
        if result == dialog.Accepted:
            selected_col = data.columns.get_loc(dialog.get_selected_option())
    return selected_col
