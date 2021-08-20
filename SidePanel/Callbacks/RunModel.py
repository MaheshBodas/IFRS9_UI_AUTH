from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import SidePanel.Callbacks.RunModel_helper as rh
from datetime import datetime
import Utility.Unzip as uz
import uuid
from rq.exceptions import NoSuchJobError
from rq.job import Job
import os
import redis
from rq import Worker, Queue, Connection
import dash
TEST = True


redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)


def run_model(app):
    if TEST:
        @app.callback([Output('run-alert', 'is_open'),
                       Output('run-alert', 'children'),
                       Output('run-alert-green', 'is_open'),
                       Output('run-alert-green', 'children'),
                       Output('model_data', 'data'),
                       Output('run-model', 'children'),
                       Output('audit-log', 'value')],
                      [Input('run-model', 'n_clicks')],
                      [State('config-data', 'data'),
                       State('scenario_checklist', 'value'),
                       State({'type': 'reporting-date', 'index': 0}, 'value'),
                       State('user-name', 'data'),
                       State('audit-log', 'value')
                       ])
        def run_model_cb(n_clicks, data, regions, reporting_date, username, log):
            if n_clicks is None:
                raise PreventUpdate
            else:
                return _run_model(reporting_date, data, regions, username, log, True)

    else:

        @app.callback(
            Output("submitted-store", "data"),
            [Input('run-model', 'n_clicks')],
            [State('config-data', 'data'),
             State('scenario_checklist', 'value'),
             State({'type': 'reporting-date', 'index': 0}, 'value'),
             State('user-name', 'data'),
             State('audit-log', 'value')
             ],
        )
        def submit(n_clicks, data, regions, reporting_date, username, log):
            """
            Submit a job to the queue, log the id in submitted-store
            """
            if n_clicks:
                id_ = str(uuid.uuid4())

                # queue the task
                queue = Queue(connection=conn)
                queue.enqueue(_run_model, reporting_date, data, regions, username, log, False, job_id=id_)

                # log process id in dcc.Store
                return {"id": id_}

            return {}

        @app.callback(Output('run-alert', 'is_open'),
                      Output('run-alert', 'children'),
                      Output('run-alert-green', 'is_open'),
                      Output('run-alert-green', 'children'),
                      Output('audit-log', 'value'),
                      Input('model_data', 'data'),
                      State('user-name', 'data'),
                      State('audit-log', 'value'),
                      State({'type': 'reporting-date', 'index': 0}, 'value'),
                      State('scenario_checklist', 'value'))
        def complete_run(model_data, username, log, reporting_date, regions):
            if model_data is None:
                raise PreventUpdate

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if log is None:
                updated_log = now + ", " + username + ": Model run with reporting date " + reporting_date \
                              + ", with regions " + str(regions)
            else:
                updated_log = log + "\n" + now + ", " + username + ": Model run with reporting date " + reporting_date \
                              + ", with regions " + str(regions)

            if model_data == "Error":
                return True, "Model Run Error", False, "",  updated_log
            else:
                return False, "", False, "Model run completed",  updated_log

        @app.callback(
            [
                Output('model_data', 'data'),
                Output("progress", "value"),
                Output("run-model-log", "children"),
                Output("collapse", "is_open"),
                Output("finished-store", "data"),
            ],
            [Input("interval", "n_intervals")],
            [State("submitted-store", "data"),
             State('user-name', 'data'),
             State('audit-log', 'value')
             ],
        )
        def retrieve_output(n, submitted, username, log):
            """
            Periodically check the most recently submitted job to see if it has
            completed.
            """
            if n and submitted:
                try:
                    job = Job.fetch(submitted["id"], connection=conn)
                    if job.get_status() == "finished":

                        # job is finished, return result, and store id
                        print("------------------JOB COMPLETED-------------------")
                        return job.result, 100, "", False, {"id": submitted["id"]},

                    # job is still running, get progress and update progress bar

                    progress = job.meta.get("progress", 0)
                    model_log = job.meta.get("status", "")
                    print("-------------------------JOB RUNNING " + submitted["id"] + "------------------")
                    print("-------------------------PROGRESS " + str(progress) + "%------------------")
                    return dash.no_update, progress, model_log, True, dash.no_update

                except NoSuchJobError:
                    # something went wrong, display a simple error message
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if log is None:
                        updated_log = now + ", " + username + ": Model run error"
                    else:
                        updated_log = log + "\n" + now + ", " + username + ": Model run error"

                    return "Error", 0, "", False, dash.no_update

            # nothing submitted yet, return nothing.
            return None, 0, "", False, {}

        @app.callback(
            Output("interval", "disabled"),
            Output("run-model", "disabled"),
            [Input("submitted-store", "data"),
             Input("finished-store", "data")],
        )
        def disable_interval(submitted, finished):
            if submitted:
                if finished and submitted["id"] == finished["id"]:

                    print("-------------------------FINISHED RUNNING " + submitted["id"] + "------------------")
                    # most recently submitted job has finished, no need for interval
                    return True, False
                # most recent job has not yet finished, keep interval going
                print("-------------------------STILL RUNNING " + submitted["id"] + "------------------")
                return False, True
            # no jobs submitted yet, disable interval
            return True, False


def _run_model(reporting_date, data, regions, username, log, all=True):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start = datetime.now().strftime("%H:%M:%S")
    try:

        if reporting_date is None:
            reporting_date = datetime.today().strftime('%d/%m/%Y')
        else:
            datetime_object = datetime.strptime(reporting_date, '%Y-%m-%d')
            reporting_date = datetime_object.strftime('%d/%m/%Y')

        return_data, run_time = rh.run_pd_models(uz.uncompress(data), regions, reporting_date)

        if log is None:
            updated_log = now + ", " + username + ": Model run with reporting date " + reporting_date \
                          + ", with regions " + str(regions)
        else:
            updated_log = log + "\n" + now + ", " + username + ": Model run with reporting date " + reporting_date \
                          + ", with regions " + str(regions)

        if all:
            return False, "", True, "Model run completed", return_data, "Run", updated_log
        else:
            return return_data

    except Exception as e:

        if log is None:
            updated_log = now + ", " + username + ": Model run error: " + str(e)
        else:
            updated_log = log + "\n" + now + ", " + username + ": Model run error: " + str(e)

        if all:
            return True, "Model Error " + str(e), False, "", "Error", "Run", updated_log
        else:
            return "Error"
