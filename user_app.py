import base64
import io

import json
import pandas as pd
import plotly.graph_objects as go
# from jupyter_dash import JupyterDash

import requests

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app_fns.plotly_callback import *
from app_fns.app_functions import *
from app_fns.user_app_layout import *

from serverConfig import *
import dash_bootstrap_components as dbc

# Create the app
# app = Dash(__name__) #for local server
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__,suppress_callback_exceptions=True,url_base_pathname='/{}/adminpanel/'.format(moodlename)) #,external_stylesheets=external_stylesheets)
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], suppress_callback_exceptions=True,
           url_base_pathname='/{}/user/'.format(moodlename))  # ,external_stylesheets=external_stylesheets)

server = app.server
app.title = 'User'

mgAPPfns = the_app_functions()

appLayout = plotly_app_layout()

# ,Input('category-list-dropdown', 'value'),Input('click-to-begin-btn', 'n_clicks')
callback_view_cat = (Output('view-cat-url', 'src'),
                     Input('init-store', 'modified_timestamp'))
view_cat = plotly_call_back()
view_cat.get_inputs_give_outputs(app, callback_view_cat, **{'callbackfunction': mgAPPfns.get_mycourses_link, 'fnParams': {
                                 'webserviceurl': webserviceurl, 'siteurl': siteURL}})


# Run the app
app.layout = html.Div(appLayout)
if __name__ == '__main__':
    app.run_server(debug=True)
