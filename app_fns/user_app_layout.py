from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date
import dash_bootstrap_components as dbc

#Plotly APP Layout
################################################
#Dont delete href
#html.A(calendar_url, href=calendar_url, target="_blank")
################################################

# mainSectionBoxStyle={'borderWidth': '2px','borderStyle': 'solid','borderRadius': '10px','padding':'20px','border-color':'darkblue',"background": "rgba(135, 206, 235, .5)"}
mainSectionBoxStyle={'borderWidth': '2px','borderStyle': 'solid','borderRadius': '10px','padding':'20px','border-color':'darkblue',"background": "rgba(225, 225, 225, .5)"}


def UI_fileUpload(upload_id):
    #upload file
    div=html.Div([
    html.P('Please upload csv file below to start',style={'font-style':'italic'}),
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
    appLayout=html.Div([
        html.Div(id="A_home"),  
        # dcc.Input(id='url1', value='http://127.0.0.1:5000/input?method=get_category_list&data={}', type='text'),
        # Enter method

        # dbc.Navbar([

        #  dbc.Container([

        #                 dbc.Row([
        #                         dbc.Col([
        #                                 dbc.Nav([
        #                                      dbc.NavItem(dbc.NavLink("Home", href="#home",external_link=True)),
        #                                 ],
        #                                 navbar=True,
        #                                 ),
        #                         ]),
        #                 ],justify="end",className="g-0"),  

                        
        #                 dbc.Row([
        #                         dbc.Col([
        #                               html.Img(src=('assets/logo.png'),style={'height':'30px'}),  
        #                         ]),
        #                 ],justify="end",className="g-0"),
        # ]),
        # ],
        # sticky="top",
        # # color="grey",
        # # color='rgba(240, 240, 240, 1)',
        # color='rgba(45, 45, 45, 1)',
        # dark="true",
        # ),    

        #html.Div([
        #]),
        #html.Br(),
#################################################
#Click to begin
################################################ 
        #html.Br(),
        #dbc.Button("Login",color="warning",id='click-to-begin-btn', n_clicks=0),     
        html.Div(id="home"),
################################################################################################
##############################################################################
#View Category/course/Section/Module
########################################################################
        dcc.Store(id='init-store', data={}),
        html.Div([
            html.Iframe(id='view-cat-url',style={"height": "1067px", "width": "100%"})
        ]),

        html.Br(),

        html.Div([
        ]),

        ],style={
                'margin':'15px',
                "background-image":"url('assets/bg2(60).jpg')",
                # "background-repeat": "no-repeat",
                # "background-position": "right top",
                # "background-size": "150px 100px"
                
                }),
    return appLayout

