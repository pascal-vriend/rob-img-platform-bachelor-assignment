from data_manager import Data


class AbstractImageWidget:
    """
    Template for an image widget. If any of the methods below is not implemented,
    the newly made ImageWidget class is not sufficient. If needed, universal methods can be added that should be used by
    all ImageWidget classes.
    """
    def __init__(self):
        pass

    def get_widget(self):
        raise NotImplemented

    def plot(self, data: Data):
        raise NotImplemented

    def remove_from_plot(self, filename):
        raise NotImplemented

    def clear(self):
        raise NotImplemented
