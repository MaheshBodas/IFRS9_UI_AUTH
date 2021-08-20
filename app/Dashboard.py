from tnp_dash_library.LayoutLibrary.EvenGridLayout import EvenGridLayout
from tnp_dash_library.TNPDashboard import TNPDashboard
from Tabs.Scenarios.ScenarioConfiguration import ScenarioConfiguration
from Tabs.Scenarios.DistributionChart import DistributionChart
from Tabs.Scenarios.CIProjection import CIProjection
from Tabs.Scenarios.MacroVariableProjections import MacroProjectionChart
from Tabs.Scenarios.ScenarioTable import ScenarioTable
from tnp_dash_library.LayoutLibrary.SidePanelLayout import SidePanelLayout
from tnp_dash_library.Enums.TNPENums import SidePanelSide
from tnp_dash_library.CompositeWidgetLibrary.ControlPanel import ControlPanel
from SidePanel.SidePanelContent import side_panel_content
from Tabs.Audit.Log import AuditLog
from Tabs.Admin.Admin import Admin
from Tabs.Audit.CalculationProcess import CalculationProcess
from Tabs.PD.TransitionMatrix import TransitionMatrixContent
from Tabs.PD.PiTPDbyGrade import PiTPDContent
from Tabs.PD.PDTermStructuresGrade import PDTermStructuresGradeContent
from Tabs.PD.MacroScalars import MacroScalarsContent
from Tabs.PD.PiTPDbyScenario import PiTPDScenarioContent
from Tabs.PD.PDTermStructures import PDTermStructureContent

API = "https://tnp-api-ifrs9.herokuapp.com/"
# API = "http://127.0.0.1:1000/"


class Dashboard(TNPDashboard):
    def __init__(self, application_name, page_tab_name, authenticate, db_connection, url_base_path, test_role, debug):
        file_upload = ScenarioConfiguration()
        distribution = DistributionChart()
        projection = CIProjection()
        macros = MacroProjectionChart()
        table = ScenarioTable()
        tool_kit_panel = side_panel_content(debug)
        audit_log = AuditLog(debug)
        admin = Admin(debug)
        process = CalculationProcess(debug)
        tm_content = TransitionMatrixContent(debug)
        pit_pd = PiTPDContent(debug)
        pd_ts_g = PDTermStructuresGradeContent(debug)
        pd_ms = MacroScalarsContent(debug)
        pd_scenario = PiTPDScenarioContent(debug)
        pd_ts = PDTermStructureContent(debug)

        control_panel = ControlPanel("", [tool_kit_panel])

        tabs = [
            SidePanelLayout("Scenarios", "ifrs9-scenarios", None, 2, 2,
                            content=[macros, file_upload, distribution, table, projection], widths=None,
                            panel_position=SidePanelSide.RIGHT, side_panel_width=4),
            EvenGridLayout("PD", "pds", None, 2, 3, [tm_content, pd_scenario, pd_ts, pd_ms, pit_pd, pd_ts_g]),
            EvenGridLayout("LGD", "lgd"),
            EvenGridLayout("EAD", "ead"),
            EvenGridLayout("Staging", "staging"),
            EvenGridLayout("Facilities", "facilities"),
            EvenGridLayout("Reporting", "reporting"),
            EvenGridLayout("Projections", "projections"),
            EvenGridLayout("Process", "audit", None, 2, 1, [process, audit_log])]

        super().__init__(application_name, page_tab_name, tabs, authenticate, db_connection, url_base_path, debug,
                         test_role, control_panel)
