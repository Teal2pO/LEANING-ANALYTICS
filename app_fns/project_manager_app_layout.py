from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date
import dash_bootstrap_components as dbc

mainSectionBoxStyle = {'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px',
                       'padding': '20px', 'border-color': 'darkblue', "background": "rgba(225, 225, 225, .5)"}

# Plotly APP Layout


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
        html.Div(id="home"),

        dbc.Navbar([

            dbc.Container([

                dbc.Row([
                    dbc.Col([
                        dbc.Nav([
                            # dbc.NavItem(dbc.NavLink("Home", href="#A_home",external_link=True)),
                            dbc.NavItem(dbc.NavLink(
                                "Home", href="#home", external_link=True)),
                            dbc.NavItem(dbc.DropdownMenu(
                                children=[
                                    # dbc.DropdownMenuItem("kbasd",header=True),
                                    dbc.DropdownMenuItem(
                                        "Choose filters", href="#filter", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Graph", href="#graph", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Download", href="#download", external_link=True),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="More",
                            )),

                        ],
                            navbar=True,
                        ),
                    ]),
                ], justify="end", className="g-0"),

                dbc.Row([
                    dbc.Col([
                        html.Img(src=('assets/logo.png'),
                                 style={'height': '30px'}),
                        #       dbc.NavbarBrand("teal LMS Admin",className="ms-2",style={"text-align":"center","font-weight": "bold","color":"black","font-family": "Times, serif"}),
                    ]),
                ], justify="end", className="g-0"),
            ]),
        ],
            sticky="top",
            # color="grey",
            # color='rgba(240, 240, 240, 1)',
            color='rgba(45, 45, 45, 1)',
            dark="true",
        ),

        dcc.Store(id='init-store', data={}),
        html.Div([
            # Main Div
            #########################
            html.Div(id="begin"),
            html.H1("Teal Project Monitoring", style={"font-size": "3.0em", "text-align": "center",
                    "font-weight": "bold", "color": "rgba(244,118,38,255)", "font-family": "Times, serif"}),
            #################################################
            # Click to begin
            ################################################
            # dbc.Button("Click to begin",color="warning",id='click-to-begin-btn', n_clicks=0),
            html.Div(id="filter"),
            html.Br(),
            ############################################
            # Choose Filter key
            ############################################
            html.Div([
                html.Div([html.Div([html.H5('Choose filter key'),
                                    dcc.Dropdown(id='col-names-list-dropdown', style={
                                                 'width': '60%', 'align-items': 'center', 'justify-content': 'center'})
                                    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),

                          html.Div([html.H5('Choose filter value'),
                                    dcc.Dropdown(
                                        id='col-values-list-dropdown', multi=True, style={'width': '60%'}),
                                    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'})
                          ], style={'padding': 20}),

            ], style=mainSectionBoxStyle),
            html.Div(id="graph"),
            html.Br(),
            ########################################
            # Bar Graph
            ########################################
            html.Div([
                html.Div([
                    html.Div([html.H3("Choose Graph Variables", style={"text-align": "center"}),
                              html.Br(),
                              html.Div([html.H5("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown', style={
                                       'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                              html.Div([html.H5("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown', style={
                                  'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                              html.Div([html.H5("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown', style={
                                  'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                              html.Div([html.H5("Choose Text-variable:"), dcc.Dropdown(id='text-list-dropdown', style={
                                  'width': '90%'})], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'})
                              ], style={'padding': 10})
                ]),
                html.Br(),
                dcc.Graph(id='attainment-status-filtered-output-fig',
                          config={
                              # 'modeBarButtonsToRemove': ['pan2d','lasso2d']
                              "displaylogo": False
                          }),
            ], style=mainSectionBoxStyle),
            html.Br(),
            html.Div(id="download"),
            # html.Div([
            # html.Div(id="histogram"),
            # html.Div([html.H3("Choose Histogram Variables",style={"text-align":"center"}),
            #                 html.Div([html.H4("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown-hist',style={'width':'80%'})],style={'width': '32%','display':'inline-block','vertical-align': 'middle'}),
            #                 html.Div([html.H4("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown-hist',style={'width':'80%'})],style={'width': '32%','display':'inline-block','vertical-align': 'middle'}),
            #                 html.Div([html.H4("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown-hist',style={'width':'80%'})],style={'width': '32%','display':'inline-block','vertical-align': 'middle'})
            #                 ],style={'padding': 10}),
            # dcc.Graph(id='attainment-status-filtered-output-hist-fig',config={"displaylogo": False}),
            # ],style=mainSectionBoxStyle),
            # html.Br(),

            html.Div([
                html.Div([
                    # html.Button('Download table as csv',id='down-load-table-button-id'),
                    dbc.Button("Download csv", color="success",
                               id='down-load-table-button-id'),
                    dcc.Download(id='download-table-id')
                ], style={'text-align': 'right'}),
                html.Br(),
                html.Div(id='filtered-attainment-status-output-table'),
                dcc.Store(id='attainment-status-filtered-output-store'),
            ], style=mainSectionBoxStyle),
            html.Br(),

        ], style={
            'margin': '15px',
            "background-image": "url('assets/bg2(60).jpg')",
            # "background-repeat": "no-repeat",
            # "background-position": "right top",
            # "background-size": "150px 100px"

        }),
    ])
    return appLayout
