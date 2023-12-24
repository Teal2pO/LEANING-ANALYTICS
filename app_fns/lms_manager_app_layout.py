from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date
import dash_bootstrap_components as dbc

# Plotly APP Layout
################################################
# Dont delete href
# html.A(calendar_url, href=calendar_url, target="_blank")
################################################

# mainSectionBoxStyle={'borderWidth': '2px','borderStyle': 'solid','borderRadius': '10px','padding':'20px','border-color':'darkblue',"background": "rgba(135, 206, 235, .5)"}
mainSectionBoxStyle = {'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px',
                       'padding': '20px', 'border-color': 'darkblue', "background": "rgba(225, 225, 225, .5)"}


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
                                dbc.NavItem(dbc.NavLink(
                                    "Home", href="#home", external_link=True)),
                                dbc.NavItem(dbc.DropdownMenu(
                                    children=[
                                        # dbc.DropdownMenuItem("Admin panel",href="#adminpanel",external_link=True),
                                        dbc.DropdownMenuItem(
                                            "Select: Category/Course", href="#select", external_link=True),
                                        dbc.DropdownMenuItem(
                                            "Outcome Attainment Monitoring", href="#useroutcomes", external_link=True),
                                        # dbc.DropdownMenuItem("Course User Interaction Monitoring",href="#courseuserinteractions",external_link=True),
                                        # dbc.DropdownMenuItem("User Interaction Monitoring",href="#userinteractions",external_link=True),
                                        # dbc.DropdownMenuItem("AI-Assisted HVP Quiz Creation",href="#quizcreate",external_link=True),
                                        # dbc.DropdownMenuItem("Exam Quiz Creation",href="#examquiz",external_link=True),
                                        # dbc.DropdownMenuItem("Upload section",href="#uploadsection",external_link=True)
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
                                ]),
                        ], justify="end", className="g-0"),
            ])],
            sticky="top",
            # color="grey",
            # color='rgba(240, 240, 240, 1)',
            color='rgba(45, 45, 45, 1)',
            dark="true",
        ),
        html.Div([
            html.H1("TEAL2.O Learning Analytics", style={"font-size": "3.0em", "text-align": "center",
                    "font-weight": "bold", "color": "rgba(244,118,38,255)", "font-family": "Times, serif"}),
            html.Div(id="begin"),
            dcc.Store(id='init-store', data={}),
            ##############################################################################
            # Select Category/Course/Section/Module
            ########################################################################
            # html.Br(),
            # html.Div(id='adminpanel'),
            # html.Div([
            #         dbc.Button("Load admin panel",color="warning",id='click-to-begin-btn', n_clicks=0),
            #         html.Br(),
            #         html.Br(),
            #         html.Div(id='load-admin-panel')
            # ],style=mainSectionBoxStyle),
            ##############################################################################
            # Select Category/Course/Section/Module
            ########################################################################
            html.Br(),
            html.Div(id='select'),
            html.Div([
                # html.H2("Select: Category/Course/Section/Activity",style={"text-align":"center"}),
                html.Br(),
                html.Div([
                    html.H4('Choose category'),
                    dcc.Dropdown(id='category-list-dropdown',
                                 value='Top', style={'width': '100%'})
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 10}),

                html.Div([
                    html.H4('Choose course'),
                    dcc.Dropdown(
                        [], 'Top', id='category-course-dropdown', style={'width': '100%'})
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 10}),

                # html.Div([
                #         html.H4('Choose section'),
                #         dcc.Dropdown([],'Top',id='course-sections-dropdown',style={'width':'100%'})
                # ],style={'width': '25%','display':'inline-block','vertical-align': 'top','padding':10}),

                # html.Div([
                #         html.H4('Choose activity'),
                #         dcc.Dropdown([],'Top',id='course-modules-dropdown',style={'width':'100%'})
                # ],style={'width': '25%','display':'inline-block','vertical-align': 'top','padding':10}),
            ], style=mainSectionBoxStyle),
            ###########################################
            # Competency Attainment
            ###########################################
            html.Br(),
            html.Div(id='useroutcomes'),
            html.Div([
                html.Div([
                    html.H2("Outcome Attainment Monitoring",
                            style={"text-align": "center"}),
                    html.Br(),
                    # html.Div(id='attainment-status-hist-fig'),
                    # html.Br(),
                    html.Div(id='max-attainment-status-hist-fig'),
                    html.Br(),
                    html.Div(
                        id='attainment-status-filtered-output-fig'),
                    html.Br(),
                    html.Div(id='attainment-status-polar-fig'),
                    html.Br(),
                    html.Div(id='attainment-status-parallel-fig')
                ]),
                html.Br(),
                html.Div([
                    dbc.Button("Download csv", color="success",
                               id='down-load-table-button-id', n_clicks=0),
                    dcc.Download(id='download-table-id')
                ], style={"text-align": "right"}),
                html.Br(),
                html.Div(id='filtered-attainment-status-output-table'),
                dcc.Store(id='attainment-status-filtered-output-store'),
            ], style=mainSectionBoxStyle),
            ####################################################################
            # Course User Interactions
            ###################################################################
            html.Br(),
            html.Div(id="courseuserinteractions"),
            html.Div([
                html.H2("Course User Interaction Monitoring",
                        style={"text-align": "center"}),
                html.Br(),
                html.Hr(),
                html.Br(),
                html.Div([html.H3('Daily User Module Interaction Figure', style={"text-align": "center"}),
                          html.Div(
                    id='user-daily-module-grades-interactions-fig')
                ]),
                html.Br(),
                html.Div([html.H3('User Module Interaction Figure', style={"text-align": "center"}),
                          html.Div(
                    id='user-module-grades-interactions-fig')
                ]),
                html.Br(),
                html.Div([
                    html.H3('Course User Grades and Interaction Table',
                            style={"text-align": "center"}),
                    html.Div([
                        dbc.Button("Download csv", color="success",
                                   id='download-user-grades-interactions-button-id', n_clicks=0),
                        dcc.Download(id='download-user-grades-interactions-response-id')], style={"text-align": "right"}),
                    html.Div(id='user-grades-interactions-output'),
                    html.Div(id='user-grades-interactions-store'),
                ]),
                html.Br(),
                # html.Div([html.H3('Course User Clusters Figure',style={"text-align":"center"}),
                #         html.Div(id='course-user-clusters-fig')
                #         ]),
                # html.Br(),
                # html.Div([html.H3('Course User Clusters Table',style={"text-align":"center"}),
                #         html.Div(id='course-user-clusters-output'),
                #         dcc.Store(id='course-user-clusters-store')
                #         ])
            ], style=mainSectionBoxStyle),


            # ####################################################################
            # #Course User Interactions
            # ###################################################################
            #                 html.Br(),
            #                 html.Div(id="userinteractions"),
            #                 html.Div([
            #                         html.H2('User Interactions',style={"text-align":"center"}),
            #                         html.Br(),
            #                         html.Div([html.H4('Choose Course User'),
            #                                 dcc.Dropdown([],'Top',id='course-users-dropdown',style={'width':'70%'})
            #                                 ]),
            #                         html.Br(),
            #                         html.Div([html.H3('User Grades Interactions Figure',style={"text-align":"center"}),
            #                                 html.Div(id='user-grades-interactions-fig')
            #                                 ]),
            #                         html.Br(),
            #                         html.H3('User Grades Interactions Table',style={"text-align":"center"}),
            #                         html.Div([
            #                                 # html.Button('Download User Grades and Interaction table as csv',id='download-grades-interactions-button-id'),
            #                                 dbc.Button("Download csv",color="success",id='download-grades-interactions-button-id', n_clicks=0),
            #                                 dcc.Download(id='download-grades-interactions-response-id')
            #                                 ],style={"text-align":"right"}),
            #                                 html.Div(id='user-grades-interactions-output-table'),
            #                                 dcc.Store(id='user-grades-interactions-output-store'),
            #                         html.Br(),
            #                         html.H3('User Module Transitions',style={"text-align":"center"}),
            #                         html.Br(),

            #                         html.Div([html.H4('Pick the date range'),
            #                                 dcc.DatePickerRange(
            #                                 id='input-date-picker-range',
            #                                 month_format='D-M-Y',
            #                                 display_format='D-M-Y',
            #                                 min_date_allowed=date(2022, 1, 1),
            #                                 max_date_allowed=date(2023, 12, 31),
            #                                 initial_visible_month=date(2023, 1, 1),
            #                                 end_date=date(2023, 12, 31)),
            #                                 html.Div(id='output-container-date-picker-range')]),
            #                         html.Br(),
            #                         html.Div([
            #                                 html.H3('User Activity Transition Figure',style={"text-align":"center"}),
            #                                 html.Div(id='user-activity-transition-fig')
            #                                 ]),
            #                         html.Br(),
            #                                 html.H3('User Activity Transition Table',style={"text-align":"center"}),
            #                         html.Div([
            #                                 html.Div([
            #                                         dbc.Button("Download csv",color="success",id='download-user-activity-transition-button-id', n_clicks=0),
            #                                         dcc.Download(id='download-user-activity-transition-response-id')])
            #                                 ],style={"text-align":"right"}),

            #                         html.Div(id='user-activity-transition-table'),
            #                         dcc.Store(id='user-activity-transition-store'),
            #                 ],style=mainSectionBoxStyle),
            # #################################################
            # #Create HVP MCQs
            # #################################################
            #         html.Br(),
            #         html.Div(id="quizcreate"),
            #         html.Br(),
            #         html.Div([
            #                 html.H2("AI-Assisted HVP Quiz Creation",style={"text-align":"center"}),
            #                 #html.Br(),
            #                 #html.Div([
            #                 # html.Div([
            #                 #         html.H5('Choose the template id'),
            #                 #         ],style={'width': '25%','display':'inline-block','vertical-align': 'top'}),
            #                 #         html.Div([
            #                 #         dcc.Input(id='mcq-hvp-templateid-input-id', type='number', placeholder='template id', min=1, max=10000, step=1, style={'width':'20%'})
            #                 #         ],style={'width': '65%','display':'inline-block','vertical-align': 'top'}),
            #                 # ]),
            #                 html.Br(),
            #                 html.Div([
            #                 html.Div([
            #                         html.H5('Enter the title'),
            #                         ],style={'width': '25%','display':'inline-block','vertical-align': 'top'}),
            #                         html.Div([
            #                                 dcc.Input(id='mcq-hvp-title-input-id', type='text', placeholder='Quiz title',style={'width':'80%'})
            #                         ],style={'width': '65%','display':'inline-block','vertical-align': 'top'}),
            #                 ]),
            #                 # html.Br(),
            #                 # html.Div([
            #                 #         html.Div([
            #                 #         html.H5('Enter the number of questions'),
            #                 #         ],style={'width': '25%','display':'inline-block','vertical-align': 'top'}),
            #                 #         html.Div([
            #                 #                 dcc.Input(id='ai-mcq-question-numbers-input-id', type='number', min=1, max=5, step=1, placeholder='Number of questions',style={'width':'20%'})
            #                 #         ],style={'width': '65%','display':'inline-block','vertical-align': 'top'}),
            #                 # ]),
            #                 html.Br(),
            #                 html.Div([
            #                         html.Div([
            #                         html.H5('Enter the topic')
            #                         ],style={'width': '25%','display':'inline-block','vertical-align': 'top'}),
            #                         html.Div([
            #                                 dcc.Textarea(id='ai-mcq-question-Language-input-id', placeholder='topic: (Ex: English grammar)',style={'width':'80%','height':'100px'}),
            #                         ],style={'width': '65%','display':'inline-block','vertical-align': 'top'}),
            #                 ]),
            #                 html.Br(),
            #                 html.Div([
            #                         dbc.Button("Click to create random hvp MCQ quiz",color="primary",id='execute-ai-hvp-mcq-call-btn', n_clicks=0),
            #                         ],style={'width': '50%','display':'inline-block','vertical-align': 'top'}),
            #                 html.Br(),
            #                 html.Div(id="ai-hvp-mcq-view"),

            #                 html.Div(id='chatgpt-hvp-mcq-response-table'),
            #                 dcc.Store(id='chatgpt-hvp-mcq-response-store'),
            #         ],style={'borderWidth': '2px','borderStyle': 'dashed','borderRadius': '10px','padding':'20px','border-color':'darkblue',"background": "rgba(183, 244, 216, .2)"}
            #         ),#subsection

            # ###################################################################################


            # ################################################
            # #Bulk Create Moodle MCQs
            # ################################################
            #         html.Br(),
            #         html.Div(id="examquiz"),
            # html.Div(id="exam-quiz",children=[
            #         html.H2("Bulk Create Exam Quiz",style={"text-align":"center"}),
            #         html.Br(),
            #         html.Div([
            #         html.Div([
            #                 dbc.Button("Download template",color="primary",id='down-load-bulk-exam-quiz-template-button-id', n_clicks=0),
            #                 dcc.Download(id='down-load-bulk-exam-quiz-template-id'),
            #                 dbc.Button("Upload csv and click",color="primary",id='execute-bulk-exam-quiz-call-btn', n_clicks=0,style={"margin-left":"10px"}),
            #         ],style={'width': '50%','display':'inline-block','vertical-align': 'top'}),

            #         html.Div([
            #                 html.Div([
            #                 dbc.Button("Download xml",color="success",id='down-load-bulk-exam-quiz-response-button-id', n_clicks=0),
            #                 dcc.Download(id='down-load-bulk-exam-quiz-response-id'),
            #                 ],style={"text-align":"right"})
            #         ],style={'width': '50%','display':'inline-block','vertical-align': 'top'}),
            #         html.Div(id='exam-quiz-response-table'),
            #         dcc.Store(id='exam-quiz-response-store'),
            #         html.Br(),
            #         ],style={'borderWidth': '2px','borderStyle': 'dashed','borderRadius': '10px','padding':'20px','border-color':'darkblue',"background": "rgba(183, 244, 216, .2)"}),#subsection 1 end
            #         html.Br(),
            #         html.Div(id="bulk_moodle_quiz"),
            # ],style={'borderWidth': '2px','borderStyle': 'solid','borderRadius': '10px','padding':'20px','border-color':'darkblue',"background": "rgba(225, 225, 225, .5)"}),
            # ###################################################################################
            #         html.Br(),
            #         html.Div([

            #         html.H2("Report Generation",style={"text-align":"center"}),
            #         html.Div([
            #         html.H4('Enter Method'),
            #         html.Div([
            #                 dcc.Input(id='input-method', placeholder='Enter method', type='text',style={'width':'100%'}),
            #         ],style={'width':'40%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Br(),
            #         html.Br(),
            #         html.H4('Enter Method Data'),
            #         html.Div([
            #                 dcc.Textarea(id='input-data', placeholder='Enter method data',style={'width':'100%','height':'100px'}),
            #         ],style={'width':'60%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Div([
            #                 dbc.Button("Execute Method",color="primary",id='execute-api-call-btn', n_clicks=0,style={"margin-left":"10px","width":"60%"}),
            #         ],style={'width':'30%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Br(),
            #         html.Br(),
            #         html.Div([
            #         html.Div([
            #                 dbc.Button("Download csv",color="success",id='down-load-API-response-button-id', n_clicks=0),
            #                 dcc.Download(id='down-load-API-response-id'),
            #         ],style={'width':'30%','display': 'inline-block','vertical-align': 'top','text-align':'right'})
            #         ],style={"text-align":"right"})
            #         ]),


            #         html.Br(),
            #         html.Div([html.Div(id='API-response-table'),
            #         dcc.Store(id='API-response-store'),
            #         html.Div(id="reportsection"),
            #         ]),

            #         ],style=mainSectionBoxStyle),

            # ##############################################################################
            # #Upload Section
            # ########################################################################
            #         html.Br(),
            #         html.Div([
            #         html.H2("Upload Section",style={"text-align":"center"}),
            #         html.Br(),
            #         UI_fileUpload('csv-upload-2'),
            #         html.Div(id='csv-upload-2-div-output'),
            #         dcc.Store(id='upload-2-df-store'),
            #         html.Br(),
            #         html.Br(),
            #         html.Div(id="uploadsection"),
            #         ],style=mainSectionBoxStyle),
            #         html.Br(),


            # ###################################################################################
            # ########################################
            # #Bar Graph
            # ########################################
            #         html.Br(),
            #         html.Div(id="bargraph"),
            #         html.Br(),
            #         html.Div([
            #         html.Div([
            #             html.Div([html.H3("Choose Bar Graph Variables",style={"text-align":"center"}),
            #                     html.Br(),
            #                     html.Div([html.H5("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Choose Text-variable:"), dcc.Dropdown(id='text-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'})
            #                     ],style={'padding': 10})
            #                     ]),
            #         html.Br(),
            #         html.Div([
            #                 dbc.Button("Update Graph",color="primary",id='get-bar-graph-btn', n_clicks=0,style={"margin-left":"10px","width":"60%"}),
            #         ],style={'width':'30%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Br(),
            #         html.Br(),
            #         html.Div(id='bar-graph-div')
            #         ],style=mainSectionBoxStyle),
            #         html.Br(),

            # ########################################
            # #Histo Graph
            # ########################################
            #         html.Br(),
            #         html.Div(id="histograph"),
            #         html.Br(),
            #         html.Div([
            #         html.Div([
            #             html.Div([html.H3("Choose Histogram Variables",style={"text-align":"center"}),
            #                     html.Br(),
            #                     html.Div([html.H5("Choose x-variable:"), dcc.Dropdown(id='hist-xcol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     #html.Div([html.H5("Choose y-variable:"), dcc.Dropdown(id='hist-ycol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Choose Group-variable:"), dcc.Dropdown(id='hist-gp-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     ],style={'padding': 10})
            #                     ]),
            #         html.Br(),
            #         html.Div([
            #                 dbc.Button("Update graph",color="primary",id='get-hist-graph-btn', n_clicks=0,style={"margin-left":"10px","width":"60%"}),
            #         ],style={'width':'30%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Br(),
            #         html.Br(),
            #         html.Div(id='hist-graph-div')
            #         ],style=mainSectionBoxStyle),
            #         html.Br(),

            # ########################################
            # #Scatter plot
            # ########################################
            #         html.Br(),
            #         html.Div(id="scattergraph"),
            #         html.Br(),
            #         html.Div([
            #         html.Div([
            #             html.Div([html.H3("Choose Scatter Plot Variables",style={"text-align":"center"}),
            #                     html.Br(),
            #                     html.Div([html.H5("Choose x-variable:"), dcc.Dropdown(id='scatter-xcol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Choose y-variable:"), dcc.Dropdown(id='scatter-ycol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Choose Group-variable:"), dcc.Dropdown(id='scatter-gp-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Choose Size-variable:"), dcc.Dropdown(id='scatter-size-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     ],style={'padding': 10})
            #                     ]),
            #         html.Br(),
            #         html.Div([
            #                 dbc.Button("Update graph",color="primary",id='get-scatter-graph-btn', n_clicks=0,style={"margin-left":"10px","width":"60%"}),
            #         ],style={'width':'30%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Br(),
            #         html.Br(),
            #         html.Div(id='scatter-graph-div')
            #         ],style=mainSectionBoxStyle),
            #         html.Br(),

            # ########################################
            # #Parallel plot
            # ########################################
            #         html.Br(),
            #         html.Div(id="parallelgraph"),
            #         html.Br(),
            #         html.Div([
            #         html.Div([
            #             html.Div([html.H3("Choose Parallel Plot Variables",style={"text-align":"center"}),
            #                     html.Br(),
            #                     html.Div([html.H5("Choose dimensions"), dcc.Dropdown(id='parallel-xcol-list-dropdown',style={'width':'100%'},multi=True)],style={'width': '80%','display':'inline-block','vertical-align': 'middle'}),
            #                     ],style={'padding': 10})
            #                     ]),
            #         html.Br(),
            #         html.Div([
            #                 dbc.Button("Update graph",color="primary",id='get-parallel-graph-btn', n_clicks=0,style={"margin-left":"10px","width":"60%"}),
            #         ],style={'width':'30%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Br(),
            #         html.Br(),
            #         html.Div(id='parallel-graph-div')
            #         ],style=mainSectionBoxStyle),
            #         html.Br(),

            # ########################################
            # #Pie Chart
            # ########################################
            #         html.Br(),
            #         html.Div(id="piegraph"),
            #         html.Br(),
            #         html.Div([
            #         html.Div([
            #             html.Div([html.H3("Choose Pie Chart Variables",style={"text-align":"center"}),
            #                     html.Br(),
            #                     html.Div([html.H5("Values"), dcc.Dropdown(id='pie-xcol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Names"), dcc.Dropdown(id='pie-ycol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     html.Div([html.H5("Hover text"), dcc.Dropdown(id='pie-hovertext-list-dropdown',style={'width':'90%'},multi=True)],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #                     ],style={'padding': 10})
            #                     ]),
            #         html.Br(),
            #         html.Div([
            #                 dbc.Button("Update graph",color="primary",id='get-pie-graph-btn', n_clicks=0,style={"margin-left":"10px","width":"60%"}),
            #         ],style={'width':'30%','display': 'inline-block','vertical-align': 'top'}),
            #         html.Br(),
            #         html.Br(),
            #         html.Div(id='pie-graph-div')
            #         ],style=mainSectionBoxStyle),
            #         html.Br(),
            ########################################
            # Old Graph - dont delete
            ########################################
            # html.Br(),
            # html.Div(id="bargraph"),
            # html.Br(),
            # html.Div([
            # html.Div([
            #     html.Div([html.H3("Choose graph variables",style={"text-align":"center"}),
            #             html.Br(),
            #             html.Div([html.H5("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #             html.Div([html.H5("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #             html.Div([html.H5("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
            #             html.Div([html.H5("Choose Text-variable:"), dcc.Dropdown(id='text-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'})
            #             ],style={'padding': 10})
            #             ]),
            # html.Br(),
            # html.Div([
            #         dbc.Button("Get graphs",color="primary",id='get-graphs-btn', n_clicks=0,style={"margin-left":"10px","width":"60%"}),
            # ],style={'width':'30%','display': 'inline-block','vertical-align': 'top'}),
            # html.Br(),
            # html.Br(),
            # html.Div(id='bar-graph-div'),
            # # dcc.Graph(id='bar-graph-fig',
            # #           config={
            # #               "displaylogo": False#'modeBarButtonsToRemove': ['pan2d','lasso2d']
            # #               }),
            # html.Br(),
            # dcc.Graph(id='hist-graph-fig',
            #         config={
            #         "displaylogo": False#'modeBarButtonsToRemove': ['pan2d','lasso2d']
            #         }),
            # html.Br(),
            # dcc.Graph(id='pie-graph-fig',
            #         config={
            #         "displaylogo": False#'modeBarButtonsToRemove': ['pan2d','lasso2d']
            #         }),
            # html.Br(),
            # dcc.Graph(id='parallel-graph-fig',
            #         config={
            #         "displaylogo": False#'modeBarButtonsToRemove': ['pan2d','lasso2d']
            #         }),
            # html.Br(),
            # dcc.Graph(id='scatter-graph-fig',
            #         config={
            #         "displaylogo": False#'modeBarButtonsToRemove': ['pan2d','lasso2d']
            #         }),
            # ],style=mainSectionBoxStyle),
            # html.Br(),
            #############################################
            # Footer
            ###########################################
            html.Div([
            ]),

        ], style={'margin': '15px', "background-image": "url('assets/bg2(60).jpg')"}),
    ])
    return appLayout
