from typing import Union, List
import os
import pandas as pd
import vtk
from GUI.popups import ErrorDialog


class DataManager:
    """
    This class functions as a universal data loader. It will create Data objects that contain the file name/directory
    together with the data itself.
    """

    def __init__(self) -> None:
        self.loaded_data: List[Data] = []

    def load_data(self, path: str) -> Union[str, None]:
        """
        Loads data into the data manager.
        :param path: the path to the data file
        :return: the name of the file if the data was loaded successfully. If an exception occurred, None is returned
        """
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext in ['.csv', '.txt']:
                data = self.read_csv(path)
            elif ext in ['.xls', '.xlsx']:
                data = self.read_excel(path)
            else:
                data = self.read_vtk_file(path, ext)

            filename = os.path.basename(path)
            new_filename = self.add_data(filename, data)
            return new_filename
        except Exception as e:
            ErrorDialog(f"Error loading {path}: {e}")
            return

    def add_data(self, filename: str, data: Union[pd.DataFrame, vtk.vtkDataObject]) -> str:
        """
        creates a Data object and appends it to the list of loaded data.
        :param filename: the filename of the file that will be added
        :param data: the data that got read from the file, in either vtk or panda format
        :return: the filename if it did not exist yet, or filename_copy_number if there was already data present with
        that file name
        """
        # Check if a file with the same name is already loaded
        copy_number = 0
        new_filename = filename
        while self.get_data_object_by_filename(new_filename) is not None:
            copy_number += 1
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_({copy_number}){ext}"
        # create the data object
        data_object = Data(new_filename, data)
        # add it to the list of loaded data
        self.loaded_data.append(data_object)
        return new_filename

    def get_data_object_by_filename(self, filename: str) -> Union['Data', None]:
        """
        Returns the data of a file, by file name
        :param filename: the name of the file
        :return: the data of that file if it exists, else None is returned
        """
        for data_object in self.loaded_data:
            if data_object.filename == filename:
                return data_object
        return None

    def set_data_by_filename(self, filename: str, data: Union[pd.DataFrame, vtk.vtkDataObject]) -> bool:
        """
        Sets the data of a file by file name.
        :param filename: the file that should be changed
        :param data: the new data
        :return: true if successful, false if no file with the filename was found
        """
        for data_object in self.loaded_data:
            if data_object.filename == filename:
                data_object.data = data
                return True
        return False

    def remove_data_by_filename(self, filename: str) -> bool:
        """
        removes data from the data manager by filename.
        :param filename: the name of the file that should be deleted
        :return: true if successful, false if no file with the filename was found
        """
        for data_object in self.loaded_data:
            if data_object.filename == filename:
                self.loaded_data.remove(data_object)
                del data_object
                return True
        return False

    def open_dicom_directory(self, path: str) -> str:
        """
        Opens a directory and loads it into a DICOM Image reader. It then will be added to the loaded data list.
        :param path: the path to the directory
        :return: the name of the directory, possibly with a copy number if the directory was already loaded.
        """
        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(path)
        reader.Update()
        data = reader.GetOutput()
        return self.add_data(path, data)

    # Different kinds of file readers
    @staticmethod
    def read_csv(filepath: str) -> pd.DataFrame:
        """Reads a CSV file and returns a DataFrame."""
        return pd.read_csv(filepath)

    @staticmethod
    def read_excel(filepath: str) -> pd.DataFrame:
        """Reads an Excel file and returns a DataFrame."""
        return pd.read_excel(filepath)

    @staticmethod
    def read_vtk_file(filepath: str, ext: str) -> Union[vtk.vtkDataObject, None]:
        try:
            """Reads a VTK file and returns a VTK data object."""
            if ext == ".vtk":
                reader = vtk.vtkGenericDataObjectReader()
            elif ext == ".vtu":
                reader = vtk.vtkXMLUnstructuredGridReader()
            elif ext == ".vtp":
                reader = vtk.vtkXMLPolyDataReader()
            elif ext == ".vti":
                reader = vtk.vtkXMLImageDataReader()
            elif ext == ".stl":
                reader = vtk.vtkSTLReader()
            elif ext == ".obj":
                reader = vtk.vtkOBJReader()
            elif ext == ".ply":
                reader = vtk.vtkPLYReader()
            elif ext in [".jpg", ".jpeg"]:
                reader = vtk.vtkJPEGReader()
            elif ext == ".png":
                reader = vtk.vtkPNGReader()
            elif ext == ".tiff" or ext == ".tif":
                reader = vtk.vtkTIFFReader()
            elif ext == ".dicom" or ext == ".dcm":
                reader = vtk.vtkDICOMImageReader()
            elif ext in [".nii", ".nii.gz"]:
                reader = vtk.vtkNIFTIImageReader()
            elif ext == ".mhd":
                reader = vtk.vtkMetaImageReader()
            else:
                ErrorDialog("Unsupported file format: {}".format(ext))
                return

            reader.SetFileName(filepath)
            reader.Update()
            return reader.GetOutput()
        except Exception as e:
            ErrorDialog(f"Error reading VTK file: {e}")


class Data:
    """
    Represents data that will be loaded.
    A list of instances of this class will be present in the DataManager.
    """

    def __init__(self, filename: str, data: Union[pd.DataFrame, vtk.vtkDataObject]):
        self.filename = filename
        self.data = data

