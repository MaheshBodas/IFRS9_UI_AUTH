from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_html_components as html


class TNPContentPanel(TNPControl):

    def __init__(self, _id: str, content: html.Div):
        self.id = _id
        self.content = content
        super().__init__(name=self.id)

    def layout(self, params=None):
        return self.content

    def store_value(self, app):
        pass
