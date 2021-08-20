from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_core_components as dcc
import dash_html_components as html
from tnp_dash_library.Enums.TNPENums import StorageType


class DataStorage(TNPControl):
    def __init__(self, _id: str, variable_name: str, initial_data=None,
                 storage_type: StorageType = StorageType.MEMORY):
        self.id = _id
        self.storage_type = storage_type
        self.var_name = variable_name
        self.value = initial_data
        super().__init__(name=self.id)

    def layout(self, params=None):

        if self.storage_type == StorageType.MEMORY:
            storage = 'memory'
        elif self.storage_type == StorageType.SESSION:
            storage = 'session'
        else:
            storage = 'local'

        return dcc.Store(id=self.var_name, data=self.value, storage_type=storage)

    def store_value(self, app):
        return
