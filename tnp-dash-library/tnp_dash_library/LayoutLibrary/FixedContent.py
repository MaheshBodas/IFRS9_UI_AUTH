from tnp_dash_library.LayoutLibrary.content_functions import content_panel
from tnp_dash_library.LayoutLibrary.TNPContent import TNPContent


class FixedContent(TNPContent):
    def __init__(self, component_id, name, layout):
        self._id = component_id
        self.name = name
        self.layout = layout
        super().__init__(component_id)

    def content_layout(self, params=None):
        return content_panel(self._id, self.name, self.layout, False)

    def content_call_back(self, app):
        pass

    def register_control(self, control):
        pass
