from tnp_dash_library.LayoutLibrary.TNPContent import TNPControl
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, MATCH
import dash_treeview_antd
import dash


class TNPTreeView(TNPControl):
    """
    TNP Slider

    Styled slider with label.

    Callback outputs:
     - var_name stores the value of the slider
    """

    def __init__(self, tree_view_id: str, label: html.Div, data: dict, select_multiple: bool = False,
                 checkable: bool = False, debug: bool = False, index=0, className="", **kwargs):
        """
            Parameters
            ----------
            tree_view_id : str
               Unique id of the tree view

            label : str
               The label displayed above the slider

             data : dict
               Dictionary value of tree view - Example:
                    {
                     'title': 'Parent',
                     'key': '0',
                     'children': [{
                         'title': 'Child',
                         'key': '0-0',
                         'children': [
                             {'title': 'Subchild1', 'key': '0-0-1'},
                             {'title': 'Subchild2', 'key': '0-0-2'},
                             {'title': 'Subchild3', 'key': '0-0-3'},
                         ],
                     }]}

            select_multiple : bool, optional
               Give option to select multiple nodes at a time (Default = false)

            checkable :  bool, optional
               Give option to check nodes at a time (Default = false)

            index :  int, optional
               Used to control index of callbacks - use when dynamically creating component  (Default = 0)

            debug: bool, optional
                Prints the stored var_name and value above slider if true to help debugging (default = False)

            **kwargs: optional
                See https://github.com/kapot65/dash-treeview-antd for more details
       """

        self.id = tree_view_id
        self.label = label
        self.select_multiple = select_multiple
        self.checkable = checkable
        self.data = data
        self.kwargs = kwargs
        self.debug = debug
        self.registered = False
        self.index = index
        self.className = className

        super().__init__(name=self.id)

    def layout(self, params=None):

        if self.debug:
            debug_html = html.Div(
                [html.Div("", id={'type': self.id + '-selected', 'index': self.index},
                          hidden=not self.debug, className="debug_variable"),
                 html.Div("", id={'type': self.id + '-checked', 'index': self.index},
                          hidden=not self.debug, className="debug_variable"),
                 ]
            )
        else:
            debug_html = html.Div()

        return html.Div(
            [html.Div(self.label, className='data-options-headings-top'),
             dcc.Store(id={'type': self.id + '-data', 'index': self.index}, data=self.data, storage_type='session'),
             dcc.Store(id={'type': self.id + '-checked-data', 'index': self.index},
                       data=self.data, storage_type='session'),
             debug_html,
             dash_treeview_antd.TreeView(
                 **self.kwargs,
                 id={'type': self.id, 'index': self.index},
                 multiple=self.select_multiple,
                 checkable=self.checkable,
                 data=self.data
             ),
             ],
            style={'width': '100%'}, className=self.className)

    def store_value(self, app):
        if not self.registered:
            self.registered = True

            if self.debug:
                @app.callback(Output({'type': self.id + '-selected', 'index': MATCH}, 'children'),
                                Input({'type': self.id, 'index': MATCH}, 'selected'))
                def _update_variable(selected):
                    if selected is None:
                        raise dash.exceptions.PreventUpdate
                    return self.id + '-data = ' + selected[0]

                if self.checkable:
                    @app.callback(Output({'type': self.id + '-checked', 'index': MATCH}, 'children'),
                                    Input({'type': self.id, 'index': MATCH}, 'checked'))
                    def _display_checked(checked):
                        if checked is None:
                            raise dash.exceptions.PreventUpdate
                        return self.id + '-checked-data = ' + ','.join(checked)

            @app.callback(Output({'type': self.id + '-data', 'index': MATCH}, 'data'),
                            Input({'type': self.id, 'index': MATCH}, 'selected'))
            def _update_variable(selected):
                if selected is None:
                    raise dash.exceptions.PreventUpdate
                return selected

            if self.checkable:
                @app.callback(Output({'type': self.id + '-checked-data', 'index': MATCH}, 'data'),
                                Input({'type': self.id, 'index': MATCH}, 'checked'))
                def _display_checked(checked):
                    if checked is None:
                        raise dash.exceptions.PreventUpdate
                    return checked

    @staticmethod
    def sample_data():
        return {
            'title': 'Parent',
            'key': '0',
            'children': [{
                'title': 'Child',
                'key': '0-0',
                'children': [
                    {'title': 'Subchild1', 'key': '0-0-1'},
                    {'title': 'Subchild2', 'key': '0-0-2'},
                    {'title': 'Subchild3', 'key': '0-0-3'},
                ],
            }]}
