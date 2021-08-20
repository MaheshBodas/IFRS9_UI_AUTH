# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from app import server
from jinja2 import TemplateNotFound
import app.Dashboard as db
from tnp_dash_library.AppFactory import AppFactory

@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # TBD
        # Detect the current page
        segment = get_segment(request)
        print(segment)
        # return render_template(template, segment=segment)
        # Start changes for the flask_login
        # Start changes for flask_login
        # Detect the current page
        segment = get_segment(request)
        print(segment)

        if segment == 'ifrs9':
            print('I am ifrs9')
            application_name = "IFRS9 ECL Tool"
            tab_name = "TNP | IFRS9 ECL Tool"
            use_database = True
            application_path = "ifrs9"
            dashboard_type = db.Dashboard
            application_id = "IFRS9"
            debugApp = False

            # application = AppFactory.fromDashboardObject(application_name, tab_name, use_database, server,
            #                                              application_path,dashboard_type, application_id, debugApp,
            #                                              "", use_database)
            return redirect(url_for('/'))
            # End changes for flask_login
        else:
            # Serve the file (if exists) from app/templates/FILE.html
            return render_template(template, segment=segment)
        TBD

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


def redirect_ifrs():
    try:
        dest = request.args.get('/ifrs9')
        dest_url = url_for(dest)
        print(dest_url)
    except:
        print('/')
        return redirect('/')
    return redirect(dest_url)

@blueprint.route('/<template>')
@login_required
def route_template1(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Start changes for flask_login
        # Detect the current page
        segment = get_segment(request)
        print(segment)
        strIfrs9 = "ifrs9"
        if strIfrs9 in segment:
            print("Found! ifrs9")
            return
        #     APPLICATION_NAME = "IFRS9 ECL Tool"
        #     TAB_NAME = "TNP | IFRS9 ECL Tool"
        #     USE_DATABASE = True
        #     APPLICATION_PATH = "ifrs9"
        #     DASHBOARD_TYPE = db.Dashboard
        #     APPLICATION_ID = "IFRS9"
        #     DEBUG = False
        #
        #     application = AppFactory.fromDashboardObject(APPLICATION_NAME, TAB_NAME, USE_DATABASE, app.server, APPLICATION_PATH,
        #                                                  DASHBOARD_TYPE, APPLICATION_ID, DEBUG, "", USE_DATABASE)
        else:
            return render_template(template, segment=segment)

        # # Serve the file (if exists) from app/templates/FILE.html
        # return render_template( template, segment=segment )
        # End changes for flask_login

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
