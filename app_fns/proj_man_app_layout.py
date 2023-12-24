from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date

# Plotly APP Layout

################################################
# Dont delete href
# html.A(calendar_url, href=calendar_url, target="_blank")
################################################


def UI_fileUpload(upload_id):
    # upload file
    div = html.Div([
        html.P('Please upload csv file below to start',
               style={'font-style': 'italic'}),
        dcc.Upload(
            id=upload_id,
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={
                'width': '98%',
                'height': '80px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
    ])
    return div


def plotly_app_layout():
    appLayout = html.Div([
        html.Br(),
        html.Hr(),
        html.Br(),
        html.Br(),
        html.H1("TEAL2.O Project Monitoring", style={"text-align": "center"}),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.Button('Click to begin', id='click-to-begin-btn', n_clicks=0),
        html.Br(),
        html.Br(),

        html.Div([
            html.Div([html.Div([html.H4('Choose filter key'),
                                dcc.Dropdown(id='col-names-list-dropdown', style={
                                             'width': '60%', 'align-items': 'center', 'justify-content': 'center'})
                                ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),

                      html.Div([html.H4('Choose filter value'),
                                dcc.Dropdown(
                                    id='col-values-list-dropdown', multi=True, style={'width': '60%'}),
                                ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'})
                      ], style={'padding': 20}),
            html.Br(),
            html.Hr(),
            html.Br(),
            html.Div([html.H3("Choose Bar Graph Variables", style={"text-align": "center"}),
                      html.Div([html.H4("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown', style={
                               'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                      html.Div([html.H4("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown', style={
                               'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                      html.Div([html.H4("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown', style={
                               'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                      html.Div([html.H4("Choose Text-variable:"), dcc.Dropdown(id='text-list-dropdown', style={
                               'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'})
                      ], style={'padding': 10})
        ]),
        html.Br(),
        dcc.Graph(id='attainment-status-filtered-output-fig',
                  config={"displaylogo": False}),
        html.Br(),
        html.Hr(),
        html.Br(),

        html.Div([html.H3("Choose Histogram Variables", style={"text-align": "center"}),
                  html.Div([html.H4("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown-hist', style={
                           'width': '80%'})], style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                  html.Div([html.H4("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown-hist', style={
                           'width': '80%'})], style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                  html.Div([html.H4("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown-hist', style={
                           'width': '80%'})], style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'})
                  ], style={'padding': 10}),

        dcc.Graph(id='attainment-status-filtered-output-hist-fig',
                  config={"displaylogo": False}),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.Div(id='filtered-attainment-status-output-table'),
        dcc.Store(id='attainment-status-filtered-output-store'),
        html.Br(),
        html.Br(),
        html.Div([html.Button('Download table as csv',
                 id='down-load-table-button-id'), dcc.Download(id='download-table-id')]),
    ])
    return appLayout
