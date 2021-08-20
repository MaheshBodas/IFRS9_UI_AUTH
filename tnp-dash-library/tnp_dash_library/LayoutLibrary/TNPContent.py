from abc import abstractmethod
from dash_oop_components import DashComponent


class TNPContent(DashComponent):

    @abstractmethod
    def __init__(self, content_name):
        super().__init__(name=content_name)

    @abstractmethod
    def content_call_back(self, app):
        return

    @abstractmethod
    def content_layout(self, params=None):
        return

    @abstractmethod
    def register_control(self, control):
        return


class TNPControl(DashComponent):

    @abstractmethod
    def __init__(self, name):
        self.id = name
        super().__init__(name=self.id)

    @abstractmethod
    def store_value(self, app):
        return
