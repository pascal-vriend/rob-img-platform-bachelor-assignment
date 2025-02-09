from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkUnstructuredGrid, vtkImageData, vtkStructuredGrid, \
    vtkPiecewiseFunction
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkDataSetMapper, vtkImageActor, vtkActor, vtkVolumeProperty, \
    vtkColorTransferFunction, vtkVolume
from vtk import vtkRenderer
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper

from data_manager import Data

from GUI.image_widgets.abstract_image_widget import AbstractImageWidget
from PySide2.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from GUI.popups import ErrorDialog


class VTKImageWidget(AbstractImageWidget):
    """
    Image widget for the vtk module
    """
    def __init__(self):
        super().__init__()
        self.loaded_actors = {}
        self.current_opacity_setting: float = 1
        self.initUI()

    def initUI(self) -> None:
        """
        set up the main visuals for the widget and create the canvas, renderer and interactor.
        :return: None
        """
        colors = vtkNamedColors()
        # Create VTK render window widget
        self.main = QWidget()
        self.main_layout = QVBoxLayout(self.main)
        self.main.setContentsMargins(0, 0, 0, 42)  # 42 to account for the matplotlib toolbar at the bottom
        self.canvas = QVTKRenderWindowInteractor()
        self.canvas.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        self.main_layout.addWidget(self.canvas)
        # Initialize the VTK rendering window
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(colors.GetColor3d('DimGray'))
        self.canvas.GetRenderWindow().AddRenderer(self.renderer)
        # Initialize interactor
        self.interactor = self.canvas.GetRenderWindow().GetInteractor()
        self.interactor.Initialize()
        self.interactor.Start()

        # Store the initial camera parameters
        self.initial_camera_position = self.renderer.GetActiveCamera().GetPosition()
        self.initial_camera_focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        self.initial_camera_view_up = self.renderer.GetActiveCamera().GetViewUp()

    def get_widget(self):
        """
        :return: the main widget
        """
        return self.main

    def plot(self, data_object: Data) -> None:
        """
        plots the data in the data object, by first looking at the data type and then creating the correct mapper and actor.
        :param data_object: the data object containing the data and the filename
        :return: None
        """
        data = data_object.data
        filename = data_object.filename
        if self.is_plotted(filename):
            return
        if isinstance(data, vtkPolyData):
            mapper = vtkPolyDataMapper()
        elif isinstance(data, (vtkUnstructuredGrid, vtkStructuredGrid)):
            mapper = vtkDataSetMapper()
        elif isinstance(data, vtkImageData):
            actor = vtkImageActor()
            actor.GetMapper().SetInputData(data)
            self.renderer.AddActor(actor)
            self.renderer.ResetCamera()
            self.canvas.GetRenderWindow().Render()
            self.add_to_actors(actor, filename)
            return
        else:
            ErrorDialog(f"Unsupported data type: {type(data)}")
            return

        mapper.SetInputData(data)
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetOpacity(self.current_opacity_setting)
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.render()
        self.add_to_actors(actor, filename)

    def is_plotted(self, filename) -> bool:
        """
        check whether the file is already plotted.
        :param filename: the file to be checked
        :return: true if plotted, else false.
        """
        return filename in self.loaded_actors

    def add_to_actors(self, actor, filename: str) -> None:
        """
        add a actor together with the file it came from to the actor list.
        :param actor: the actor
        :param filename: the file
        :return: None
        """
        self.loaded_actors[filename] = actor

    def reset_camera(self) -> None:
        """
        resets the camera orientation to the original oriëntation
        :return: None
        """
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(self.initial_camera_position)
        camera.SetFocalPoint(self.initial_camera_focal_point)
        camera.SetViewUp(self.initial_camera_view_up)
        self.renderer.ResetCamera()
        self.render()
        self.renderer.ResetCamera()
        self.render()

    def set_mesh_color(self, filename: str, color: str) -> None:
        """
        sets the color of a mesh, by filename.
        :param filename: the name of the file that the mesh came from
        :param color: the color in hex format
        :return: None
        """
        # Check if the filename exists in the dictionary
        if not self.is_plotted(filename):
            ErrorDialog("please select a file and plot the data ")
            return

        # Get the actor corresponding to the filename
        actor = self.loaded_actors[filename]

        # Check if the actor represents a mesh
        if not isinstance(actor.GetMapper().GetInput(), (vtkPolyData, vtkUnstructuredGrid)):
            ErrorDialog(f"Actor with filename '{filename}' does not represent a mesh and cannot be colored.")
            return

        # Parse hexadecimal color to RGB values
        hex_color = color.lstrip('#')
        try:
            if len(hex_color) == 3:  # Shorthand notation, e.g., #fff
                rgb_color = tuple(int(hex_color[i] * 2, 16) / 255.0 for i in (0, 1, 2))
            elif len(hex_color) == 6:  # Full-length notation, e.g., #ffffff
                rgb_color = tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
            else:
                raise ValueError("Invalid hexadecimal color format.")
        except ValueError:
            ErrorDialog(f"Invalid hexadecimal color: {hex_color}")
            return

        # Set the color of the actor
        actor.GetProperty().SetColor(rgb_color)

        # Update the rendering
        self.render()

    def plot_volume(self, volume, filename: str) -> None:
        """
        plots a DICOM volume
        :param volume: the volumetric data
        :param filename: the filename associated with the volume
        :return: None
        """
        if self.is_plotted(filename):
            return

        # Create a volume mapper
        volume_mapper = vtkSmartVolumeMapper()
        volume_mapper.SetInputData(volume)

        # Create a volume property
        volume_property = vtkVolumeProperty()
        volume_property.ShadeOn()
        volume_property.SetInterpolationTypeToLinear()

        # Create an opacity transfer function
        opacity_transfer_function = vtkPiecewiseFunction()
        min_scalar, max_scalar = volume.GetScalarRange()
        opacity_transfer_function.AddPoint(min_scalar, 0.0)  # Fully transparent at min_scalar
        opacity_transfer_function.AddPoint(min_scalar + (max_scalar - min_scalar) * 0.25,0.1)  # Slightly visible at 25% of the range
        opacity_transfer_function.AddPoint(min_scalar + (max_scalar - min_scalar) * 0.5,0.3)   # More visible at 50% of the range
        opacity_transfer_function.AddPoint(min_scalar + (max_scalar - min_scalar) * 0.75,0.6)  # More opaque at 75% of the range
        opacity_transfer_function.AddPoint(max_scalar, 0.85)  # Mostly opaque at max_scalar
        volume_property.SetScalarOpacity(opacity_transfer_function)

        # Create a color transfer function
        color_transfer_function = vtkColorTransferFunction()
        color_transfer_function.AddRGBPoint(min_scalar, 0.0, 0.0, 0.0)  # Air, Black
        color_transfer_function.AddRGBPoint(min_scalar + (max_scalar - min_scalar) * 0.2, 0.55, 0.25,0.15)  # Low-density tissue, Dark brownish-red
        color_transfer_function.AddRGBPoint(min_scalar + (max_scalar - min_scalar) * 0.4, 0.75, 0.5,0.4)  # Soft tissue, Pinkish
        color_transfer_function.AddRGBPoint(min_scalar + (max_scalar - min_scalar) * 0.6, 0.9, 0.75,0.6)  # Higher-density tissue, Light pink
        color_transfer_function.AddRGBPoint(max_scalar, 1.0, 1.0, 1.0)  # Bone, White
        volume_property.SetColor(color_transfer_function)

        # Create the volume
        volume_actor = vtkVolume()
        volume_actor.SetMapper(volume_mapper)
        volume_actor.SetProperty(volume_property)

        # Add the volume to the renderer
        self.renderer.AddVolume(volume_actor)
        self.renderer.ResetCamera()
        self.canvas.GetRenderWindow().Render()

        self.add_to_actors(volume_actor, filename)

    def set_mesh_opacity(self, filename: str, opacity: float) -> None:
        """
        sets the opacity of a mesh
        :param filename: the filename associated with the mesh
        :param opacity: the opacity setting, which is a floating point number between 0 and 1
        :return: None
        """
        self.current_opacity_setting = opacity
        # Check if the filename exists in the dictionary
        if not self.is_plotted(filename):
            return
        # Get the actor corresponding to the filename
        actor = self.loaded_actors[filename]
        actor.GetProperty().SetOpacity(opacity)
        self.render()

    def remove_from_plot(self, filename: str) -> None:
        """
        removes an actor from the plot by filename
        :param filename: the file containing data that should be removed from the plot
        :return: None
        """
        # Check if the filename exists in the dictionary
        if not self.is_plotted(filename):
            return

        # Get the actor corresponding to the filename
        actor = self.loaded_actors[filename]

        # Remove the actor from the renderer
        self.renderer.RemoveActor(actor)

        # Update the rendering
        self.render()

        # Remove the actor from the dictionary
        del self.loaded_actors[filename]

    def render(self) -> None:
        """
        (re)renders the window
        :return: None
        """
        self.canvas.GetRenderWindow().Render()

    def clear(self) -> None:
        """
        clears all actors from the canvas
        :return: None
        """
        self.loaded_actors.clear()
        self.renderer.RemoveAllViewProps()
        self.canvas.GetRenderWindow().Render()
