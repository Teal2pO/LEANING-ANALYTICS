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
        html.Div(id="A_home"),
        # dcc.Input(id='url1', value='http://127.0.0.1:5000/input?method=get_category_list&data={}', type='text'),
        # Enter method

        dbc.Navbar([

            dbc.Container([

                dbc.Row([
                    dbc.Col([
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink(
                                "Home", href="#A_home", external_link=True)),
                            dbc.NavItem(dbc.NavLink(
                                "Upload", href="#A_upload", external_link=True)),
                            dbc.NavItem(dbc.DropdownMenu(
                                children=[
                                    # dbc.DropdownMenuItem("kbasd",header=True),
                                    dbc.DropdownMenuItem(
                                        "Method Selection", href="#A_M_selection", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Bulk actions", href="#A_B_actions", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Select: Category/Course/Section/Module", href="#A_S_catogory", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "View: Category/Course/Section/Module", href="#A_V_catogory", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Create/Edit/Delete Categories", href="#A_CED_catogory", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "View/Create/Edit/Delete/Enrol-Users - Courses", href="#A_V_users", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "View/Edit/Create - Sections", href="#A_V_sections", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "View/Edit/Create - Assignments and Schedules", href="#A_V_assignments", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Create hvp Quiz", href="#A_C_hvp", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Assign Course Activity Roles", href="#A_A_course", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Competency Management", href="#A_C_management", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "User Management", href="#A_U_management", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "User Interaction Monitoring", href="#A_U_monitoring", external_link=True),
                                    dbc.DropdownMenuItem(
                                        "Outcome Attainment Monitoring", href="#A_O_monitoring", external_link=True),
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
            ]),
        ],
            sticky="top",
            # color="grey",
            # color='rgba(240, 240, 240, 1)',
            color='rgba(45, 45, 45, 1)',
            dark="true",
        ),
        html.Div([



            html.H1("TEAL LMS Admin", style={"font-size": "3.0em", "text-align": "center",
                    "font-weight": "bold", "color": "rgba(244,118,38,255)", "font-family": "Times, serif"}),
            html.Br(),
            #################################################
            # Click to begin
            ################################################
            html.Br(),
            dbc.Button("Click to begin", color="warning",
                       id='click-to-begin-btn', n_clicks=0),
            html.Div(id="A_upload"),
            html.Br(),
            html.Br(),


            ##############################################################################
            # Upload Section
            ########################################################################
            html.Div([
                html.H2("Upload Section", style={"text-align": "center"}),
                html.Br(),
                UI_fileUpload('csv-upload-2'),
                html.Div(id='csv-upload-2-div-output'),
                dcc.Store(id='upload-2-df-store'),
                html.Br(),
                html.Br(),
                html.Div(id="A_M_selection"),
            ], style=mainSectionBoxStyle),
            html.Br(),



            #################################################
            # Test API Call Section
            ################################################


            ############################################
            # Choose method
            ############################################
            html.Div([

                html.H2("Method Selection", style={"text-align": "center"}),
                html.H4('Choose the method'),

                html.Div([
                    html.Div([
                        dcc.Dropdown(id='methods-list-dropdown',
                                     value='Top', style={'width': '100%'}),
                    ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        dbc.Button("Get the method arguments", color="primary", id='get-method-arguments-btn',
                                   n_clicks=0, style={"margin-left": "10px", "width": "30%"}),

                    ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),
                ]),

                html.Br(),
                html.Div(id='API-method-arguments-table'),
                html.Br(),
                html.H4('Enter Method Data'),

                html.Div([
                    html.Div([
                        dcc.Input(id='input-data', value='{}',
                                  type='text', style={'width': '100%'}),
                    ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        dbc.Button("Execute API Call", color="primary", id='execute-api-call-btn',
                                   n_clicks=0, style={"margin-left": "10px", "width": "60%"}),

                    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        dbc.Button("Download csv", color="success",
                                   id='down-load-API-response-button-id', n_clicks=0),
                        dcc.Download(id='down-load-API-response-id'),
                    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),
                ]),


                html.Br(),
                html.Div([html.Div(id='API-response-table'),
                          dcc.Store(id='API-response-store'),
                          html.Div(id="A_B_actions"),
                          ]),

            ], style=mainSectionBoxStyle),

            #################################################
            # Bulk actions
            #################################################
            html.Br(),

            html.Div([
                html.H2("Bulk actions", style={"text-align": "center"}),
                html.Br(),
                ################################################
                # Calling Bulk API methods
                ################################################
                html.Div([
                    html.H4('Choose the method'),

                    html.Div([
                        dcc.Dropdown(
                            [], '', id='bulk-methods-dropdown', style={'width': '100%'}),
                    ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        dbc.Button("Download template", color="primary", id='down-load-bulk-method-template-button-id',
                                   n_clicks=0, style={'margin-left': '10px', 'margin-right': '10px'}),
                        dcc.Download(id='down-load-bulk-method-template-id'),
                        dbc.Button("Upload csv and click", color="primary",
                                   id='execute-bulk-api-call-btn', n_clicks=0),
                    ], style={'width': '55%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        html.Div([
                            dbc.Button("Download csv", color="success",
                                       id='down-load-API-bulk-response-button-id', n_clicks=0),
                            dcc.Download(id='down-load-API-bulk-response-id'),
                        ], style={'text-align': 'right'}),
                    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),


                ]),


                html.Br(),
                html.Div(id='API-bulk-response-table'),
                dcc.Store(id='API-bulk-response-store2'),

                html.Br(),
                html.Div(id="A_S_catogory"),
            ], style=mainSectionBoxStyle),

            ##############################################################################
            # Select Category/course/Section/Module
            ########################################################################
            html.Br(),
            html.Div([
                html.H2("Select: Category/Course/Section/Module",
                        style={"text-align": "center"}),
                html.Br(),
                html.Div([
                    html.H4('Choose category'),
                    dcc.Dropdown(id='category-list-dropdown',
                                 value='Top', style={'width': '100%'})
                ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 10}),

                html.Div([
                    html.H4('Choose course'),
                    dcc.Dropdown(
                        [], 'Top', id='category-course-dropdown', style={'width': '100%'})
                ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 10}),

                html.Div([
                    html.H4('Choose section'),
                    dcc.Dropdown(
                        [], 'Top', id='course-sections-dropdown', style={'width': '100%'})
                ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 10}),

                html.Div([
                    html.H4('Choose activity'),
                    dcc.Dropdown(
                        [], 'Top', id='course-modules-dropdown', style={'width': '100%'})
                ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 10}),

                html.Br(),
                html.Br(),
                html.Div(id="A_V_catogory"),
            ], style=mainSectionBoxStyle),
            ################################################################################################
            ##############################################################################
            # View Category/course/Section/Module
            ########################################################################
            html.Br(),
            html.Div([
                html.H2("View: Category/Course/Section/Module",
                        style={"text-align": "center"}),
                html.Br(),
                ##############################################
                # Show categories
                ##############################################

                html.Div([
                    dbc.Button("Show categories", color="primary",
                               id='get-category-information-btn', n_clicks=0, style={'width': '30%'}),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        dbc.Button("Download csv", color="success",
                                   id='down-load-category-information-response-button-id', n_clicks=0),
                        dcc.Download(
                            id='down-load-category-information-response-id'),
                    ], style={"text-align": "right"}),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div(id='category-information-response-table'),
                dcc.Store(id='category-information-response-store'),
                ##############################################
                # Show courses
                ##############################################
                html.Br(),

                html.Div([
                    dbc.Button("Show category courses", color="primary",
                               id='get-course-information-btn', n_clicks=0, style={'width': '30%'}),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        html.Div([
                            dbc.Button("Download csv", color="success",
                                       id='down-load-course-information-response-button-id', n_clicks=0),
                            dcc.Download(id='down-load-course-information-response-id')]),
                    ], style={"text-align": "right"}),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),


                html.Div(id='course-information-response-table'),
                dcc.Store(id='course-information-response-store'),
                ##############################################
                # Show sections
                ##############################################
                html.Br(),

                html.Div([
                    dbc.Button("Show course sections", color="primary",
                               id='get-sections-information-btn', n_clicks=0, style={'width': '30%'}),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        html.Div([dbc.Button("Download csv", color="success", id='down-load-sections-information-response-button-id', n_clicks=0),
                                  dcc.Download(id='down-load-sections-information-response-id')]),
                    ], style={"text-align": "right"}),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div(id='sections-information-response-table'),
                dcc.Store(id='sections-information-response-store'),

                ##############################################
                # Show modules
                ##############################################
                html.Br(),

                html.Div([
                    dbc.Button("Show course activities", color="primary",
                               id='get-course-assignments-list-btn', n_clicks=0, style={'width': '30%'}),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        html.Div([
                            dbc.Button("Download csv", color="success",
                                       id='down-load-modules-information-response-button-id', n_clicks=0),
                            dcc.Download(id='down-load-modules-information-response-id')]),
                    ], style={"text-align": "right"}),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div(id='course-modules-info-response-table'),
                dcc.Store(id='course-modules-info-response-store'),
                html.Div(id="A_CED_catogory"),
            ], style=mainSectionBoxStyle),
            ####################################################################################################
            # course Categories
            ####################################################################################################
            html.Br(),

            html.Div([
                html.H2("Create/Edit/Delete Categories",
                        style={"text-align": "center"}),
                html.Br(),
                ############################################
                # Edit/Create Categories - Moodle
                ############################################
                # html.Div([html.A('🔗 Click to edit categories',id='view-cat-url', target="_blank")]),
                html.Br(),
                html.Div([
                    html.Iframe(id='view-cat-url',
                                style={"height": "1067px", "width": "100%"})
                ]),
                html.Br(),

                html.Div([
                    dbc.Button("Download template", color="primary",
                               id='down-load-create-categories-method-template-button-id', n_clicks=0, style={'margin-right': '10px'}),
                    dcc.Download(
                        id='down-load-create-categories-method-template-id'),
                    dbc.Button("Upload csv and click", color="primary",
                               id='create-categories-btn', n_clicks=0),
                ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    dbc.Button("Download csv", color="success",
                               id='down-load-create-categories-response-button-id', n_clicks=0),
                    dcc.Download(id='down-load-create-categories-response-id'),

                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),


                html.Div(id='create-categories-response-table'),
                dcc.Store(id='create-categories-response-store'),


                html.Br(),
                html.Div(id="A_V_users"),

            ], style=mainSectionBoxStyle),
            ###################################################################
            # courses in category
            ###################################################################
            html.Br(),
            html.Div([
                html.H2("View/Create/Edit/Delete/Enrol-Users - Courses",
                        style={"text-align": "center"}),
                html.Br(),
                ########################################
                # Edit/Create/Enroll course
                ########################################
                html.Br(),
                # html.Button('Edit course metadata', id='edit-course-btn', n_clicks=0),
                html.Div([html.A('🔗 Edit course metadata', id='edit-course-url', target="_blank")
                          ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
                html.Div([html.A('🔗 Click to edit assigned roles', id='enrol-users-url', target="_blank")
                          ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
                html.Br(),
                html.Br(),
                html.Br(),

                html.Div([
                    dbc.Button("Download template", color="primary",
                               id='down-load-create-courses-method-template-button-id', n_clicks=0, style={'margin-right': '10px'}),
                    dcc.Download(
                        id='down-load-create-courses-method-template-id'),
                    dbc.Button("Upload csv and click", color="primary",
                               id='create-course-btn', n_clicks=0),
                ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    # html.Button('Download created courses table as csv',id='down-load-create-courses-response-button-id'),
                    dbc.Button("Download csv", color="success",
                               id='down-load-create-courses-response-button-id', n_clicks=0),
                    dcc.Download(id='down-load-create-courses-response-id'),

                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),



                html.Div(id='create-courses-response-table'),
                dcc.Store(id='create-courses-response-store'),



                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                # html.Button('Get system users and roles', id='get-roles-users-list-btn', n_clicks=0),

                html.Div([
                    html.H5('Choose role'),
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
                html.Div([
                    html.H5('Choose user'),
                ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'}),


                html.Div([
                    # html.H5('Choose role'),
                    dcc.Dropdown(id='roles-list-dropdown',
                                 style={'width': '250px'})
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    # html.H5('Choose user'),
                    dcc.Dropdown(id='user-list-4-roles-dropdown',
                                 style={'width': '250px'}, multi=True),
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    # html.Button('Enrol user in course', id='enrol-users-course-role-btn', n_clicks=0),
                    dbc.Button("Enrol user in course", color="primary",
                               id='enrol-users-course-role-btn', n_clicks=0),
                ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Br(),
                html.Div(id='enrol-users-course-role-response-table'),
                html.Br(),
                html.Div(id="A_V_sections"),

            ], style=mainSectionBoxStyle),
            ##########################################################################################
            ###################################################################
            # course Sections
            ####################################################################
            html.Br(),
            html.Div([
                html.H2("View/Edit/Create - Sections",
                        style={"text-align": "center"}),
                html.Br(),
                ########################################
                # Edit section
                ########################################
                html.Br(),
                # html.Button('Edit section', id='edit-course-section-btn', n_clicks=0),
                html.Div([html.A('🔗 Edit section', id='edit-course-section-url', target="_blank")
                          ]),
                # html.Div([
                #    html.Iframe(id='edit-course-section-url',style={"height": "1067px", "width": "100%"})
                # ]),
                html.Br(),
                html.Br(),
                ########################################
                # Create section
                ########################################

                html.Div([
                    # html.Button('Download create sections csv template',id='down-load-create-sections-method-template-button-id'),
                    dbc.Button("Download template", color="primary",
                               id='down-load-create-sections-method-template-button-id', n_clicks=0),
                    dcc.Download(
                        id='down-load-create-sections-method-template-id'),

                    # html.Button('Upload the course csv in the Upload Section for the Admin panel and click the button below and click to create sections', id='create-sections-btn', n_clicks=0),
                    dbc.Button("Upload csv and click", color="primary",
                               id='create-sections-btn', n_clicks=0, style={'margin-left': '10px'}),

                ], style={'width': '65%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width': '45%','display':'inline-block','vertical-align': 'top'}),


                html.Div([
                    html.Div([
                        # html.Button('Download created section table as csv',id='down-load-create-sections-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='down-load-create-sections-response-button-id', n_clicks=0),
                        dcc.Download(
                            id='down-load-create-sections-response-id'),
                    ], style={"text-align": "right"}),
                ], style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div(id='create-sections-response-table'),
                dcc.Store(id='create-sections-response-store'),

                html.Br(),
                html.Br(),
                html.Div(id="A_V_assignments"),

            ], style=mainSectionBoxStyle),
            ###############################################################################################
            ###################################################################
            # Section Modules
            ####################################################################

            html.Br(),
            html.Div([
                html.H2("View/Edit/Create - Assignments and Schedules",
                        style={"text-align": "center"}),
                html.Br(),
                ###################################################################
                # Edit module
                ####################################################################
                html.Br(),
                # html.Button('Edit activity', id='edit-module-btn', n_clicks=0),
                html.Div([html.A('🔗 Click to edit activity', id='edit-module-url', target="_blank")
                          ], style={'width': '19%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 20}),
                html.Div([html.A('🔗 Click to edit activity roles', id='enroll-module-url', target="_blank")
                          ], style={'width': '19%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': 20}),
                html.Br(),
                html.Br(),
                html.Hr(),
                html.H4("‣ Create assignments", style={"color": "black"}),

                ###################################################################
                # Create assginments
                ####################################################################
                html.Div([

                    # html.Button('Download create activities csv template',id='down-load-create-activities-method-template-button-id'),
                    dbc.Button("Download template", color="primary",
                               id='down-load-create-activities-method-template-button-id', n_clicks=0),
                    dcc.Download(
                        id='down-load-create-activities-method-template-id'),

                    # html.Button('Upload the activities csv in the Upload Section and click to create activities', id='create-activities-btn', n_clicks=0),
                    dbc.Button("Upload csv and click", color="primary",
                               id='create-activities-btn', n_clicks=0, style={"margin-left": "10px"}),
                ], style={'width': '65%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([

                # ],style={'width': '45%','display':'inline-block','vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download created activities table as csv',id='down-load-create-activities-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='down-load-create-activities-response-button-id', n_clicks=0),
                        dcc.Download(id='down-load-create-activities-response-id')], style={"text-align": "right"}),

                ], style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top'}),



                html.Div(id='create-activities-response-table'),
                dcc.Store(id='create-activities-response-store'),


                html.Br(),
                html.Br(),
                ###################################################################
                # Create schedules
                ####################################################################
                html.Hr(),
                html.H4("‣ Create schedules", style={"color": "black"}),

                html.Div([
                    # html.Button('Download create schedules csv template',id='down-load-create-schedules-method-template-button-id'),
                    dbc.Button("Download template", color="primary",
                               id='down-load-create-schedules-method-template-button-id', n_clicks=0),
                    dcc.Download(
                        id='down-load-create-schedules-method-template-id'),
                    # html.Button('Upload the schedules csv in the Upload Section and click to create schedules', id='create-schedules-btn', n_clicks=0),
                    dbc.Button("Upload csv and click", color="primary",
                               id='create-schedules-btn', n_clicks=0, style={"margin-left": "10px"}),
                ], style={'width': '65%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width': '45%','display':'inline-block','vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        dbc.Button("Download csv", color="success",
                                   id='down-load-create-schedules-response-button-id', n_clicks=0),
                        dcc.Download(
                            id='down-load-create-schedules-response-id'),
                    ], style={"text-align": "right"}),
                ], style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top'}),



                html.Div(id='create-schedules-response-table'),
                dcc.Store(id='create-schedules-response-store'),
                #   html.Button('Download created schedules table as csv',id='down-load-create-schedules-response-button-id'),



                html.Br(),
                html.Br(),
                html.Div(id="A_C_hvp"),

            ], style=mainSectionBoxStyle),
            ###################################################################################
            ################################################
            # Bulk Create HVP MCQs
            ################################################
            html.Br(),
            html.Div(id="mid", children=[
                html.H2("Create hvp Quiz", style={"text-align": "center"}),
                html.Br(),

                html.Div([
                    html.H2("Create hvp MCQ Quiz", style={
                            "text-align": "left"}),
                    html.Br(),

                    html.Div([
                        html.H5('Choose the hvp MCQ template',
                                style={"width": "80%"}),
                    ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        dcc.Input(id='mcq-hvp-templateid-input-id', type='number',
                                  placeholder='template id', min=1, max=10000, step=1, style={'width': '15%'})
                    ], style={'width': '67%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Br(),
                    html.Br(),

                    html.Div([
                        html.H5('Enter the hvp MCQ Quiz title'),
                    ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),


                    html.Div([
                        dcc.Input(id='mcq-hvp-title-input-id', type='text',
                                  placeholder='Quiz title', style={'width': '80%'})
                        # dcc.Textarea(id='mcq-hvp-title-input-id', placeholder='Quiz title',style={'width':'80%','height':'50px'}),

                    ], style={'width': '67%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Br(),
                    html.Br(),

                    html.Hr(),
                    html.H4("‣ Create from CSV", style={"color": "black"}),

                    html.Div([
                        # html.Button('Download bulk hvp MCQ csv template',id='down-load-bulk-hvp-mcq-template-button-id'),
                        dbc.Button("Download template", color="primary",
                                   id='down-load-bulk-hvp-mcq-template-button-id', n_clicks=0),
                        dcc.Download(id='down-load-bulk-hvp-mcq-template-id'),
                        dbc.Button("Upload csv and click", color="primary",
                                   id='execute-bulk-hvp-mcq-call-btn', n_clicks=0, style={"margin-left": "10px"}),
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),


                    # html.Div([
                    # ],style={'width': '25%','display':'inline-block','vertical-align': 'top'}),

                    html.Div([
                        html.Div([
                            # html.Button('Download csv',id='down-load-bulk-hvp-mcq-response-button-id'),
                            dbc.Button("Download csv", color="success",
                                       id='down-load-bulk-hvp-mcq-response-button-id', n_clicks=0),
                            dcc.Download(
                                id='down-load-bulk-hvp-mcq-response-id'),
                        ], style={"text-align": "right"})
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),


                    html.Br(),
                    # html.H3('API Response',style={"text-align":"center"}),
                    html.Div(id='bulk-hvp-mcq-response-table'),
                    dcc.Store(id='bulk-hvp-mcq-response-store'),

                    html.Br(),
                    html.Br(),
                    html.Hr(),
                    html.H4("‣ AI create", style={"color": "black"}),


                    html.Div([
                        html.H5('Enter the number of questions',
                                style={"width": "80%"}),
                    ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        dcc.Input(id='ai-mcq-question-numbers-input-id', type='number', min=1,
                                  max=5, step=1, placeholder='Number of questions', style={'width': '20%'})
                    ], style={'width': '67%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Br(),
                    html.Br(),

                    html.Div([
                        html.H5('Enter the topic')
                    ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),


                    html.Div([
                        dcc.Textarea(id='ai-mcq-question-Language-input-id',
                                     placeholder='topic: (Ex: English grammar)', style={'width': '80%', 'height': '100px'}),
                    ], style={'width': '67%', 'display': 'inline-block', 'vertical-align': 'top'}),


                    html.Br(),

                    html.Div([
                        dbc.Button("Click to create random hvp MCQ quiz", color="primary",
                                   id='execute-ai-hvp-mcq-call-btn', n_clicks=0),
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
                    html.Br(),
                    # html.Div([
                    #         html.Iframe(id="ai-hvp-mcq-view",style={"height": "1067px", "width": "100%"})
                    #         ]),
                    html.Div(id="ai-hvp-mcq-view"),

                    # html.Br(),
                    # html.Br(),

                    html.Div([
                        dbc.Button("Download csv", color="success",
                                   id='down-load-chatgpt-hvp-mcq-response-button-id', n_clicks=0),
                        dcc.Download(
                            id='down-load-chatgpt-hvp-mcq-response-id')
                    ], style={"text-align": "right"}),

                    html.Br(),

                    html.Div(id='chatgpt-hvp-mcq-response-table'),
                    dcc.Store(id='chatgpt-hvp-mcq-response-store'),

                    html.Br(),

                ], style={'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px', 'padding': '20px', 'border-color': 'darkblue', "background": "rgba(183, 244, 216, .2)"}),  # subsection 1 end


                html.Br(),

                ################################################
                # Bulk Create HVP SWs
                ################################################
                html.Div([

                    html.H2("Create hvp SW Quiz", style={
                            "text-align": "left"}),
                    html.Br(),

                    html.Div([
                        html.H5('Choose the hvp SW template',
                                style={"width": "80%"}),
                    ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        dcc.Input(id='sw-hvp-templateid-input-id', type='number',
                                  placeholder='template id', min=1, max=10000, step=1, style={'width': '20%'})
                    ], style={'width': '67%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Br(),
                    html.Br(),

                    html.Div([
                        html.H5('Enter the hvp MCQ SW title'),
                    ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),


                    html.Div([
                        dcc.Input(id='sw-hvp-title-input-id', type='text',
                                  placeholder='Quiz title', style={'width': '80%'}),
                    ], style={'width': '67%', 'display': 'inline-block', 'vertical-align': 'top'}),



                    html.Br(),
                    html.Br(),



                    html.Div([
                        dbc.Button("Download template", color="primary",
                                   id='down-load-bulk-hvp-sw-template-button-id', n_clicks=0),
                        dcc.Download(id='down-load-bulk-hvp-sw-template-id'),
                        dbc.Button("Upload csv and click", color="primary",
                                   id='execute-bulk-hvp-sw-call-btn', n_clicks=0, style={"margin-left": "10px"}),
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        html.Div([
                            dbc.Button("Download csv", color="success",
                                       id='down-load-bulk-hvp-sw-response-button-id', n_clicks=0),
                            dcc.Download(
                                id='down-load-bulk-hvp-sw-response-id')
                        ], style={"text-align": "right"})
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Br(),
                    # html.H3('API Response',style={"text-align":"center"}),
                    html.Div(id='bulk-hvp-sw-response-table'),
                    dcc.Store(id='bulk-hvp-sw-response-store'),



                ], style={'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px', 'padding': '20px', 'border-color': 'darkblue', "background": "rgba(183, 244, 216, .2)"}),  # subsection 2 end


                html.Div(id="A_A_course"),

            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px', 'border-color': 'darkblue', "background": "rgba(225, 225, 225, .5)"}),
            ###################################################################################


            ###################################################################################
            ################################################
            # Bulk Create Moodle MCQs
            ################################################
            html.Br(),
            html.Div(id="exam-quiz", children=[
                html.H2("Bulk Create Exam Quiz", style={
                        "text-align": "center"}),
                html.Br(),
                html.Div([
                    html.Div([
                        dbc.Button("Download template", color="primary",
                                   id='down-load-bulk-exam-quiz-template-button-id', n_clicks=0),
                        dcc.Download(
                            id='down-load-bulk-exam-quiz-template-id'),
                        dbc.Button("Upload csv and click", color="primary",
                                   id='execute-bulk-exam-quiz-call-btn', n_clicks=0, style={"margin-left": "10px"}),
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                    html.Div([
                        html.Div([
                            dbc.Button("Download xml", color="success",
                                       id='down-load-bulk-exam-quiz-response-button-id', n_clicks=0),
                            dcc.Download(
                                id='down-load-bulk-exam-quiz-response-id'),
                        ], style={"text-align": "right"})
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
                    html.Div(id='exam-quiz-response-table'),
                    dcc.Store(id='exam-quiz-response-store'),
                    html.Br(),
                ], style={'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px', 'padding': '20px', 'border-color': 'darkblue', "background": "rgba(183, 244, 216, .2)"}),  # subsection 1 end
                html.Br(),
                html.Div(id="bulk_moodle_quiz"),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px', 'border-color': 'darkblue', "background": "rgba(225, 225, 225, .5)"}),
            ###################################################################################


            ####################################################################
            # Assign context roles
            ###################################################################
            html.Br(),
            html.Div([
                html.H2("Assign Course Activity Roles",
                        style={"text-align": "center"}),
                html.Br(),
                #######################################
                html.Div([
                    html.H5('Choose role'),
                ], style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.H5('Choose modules'),
                ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.H5('Choose users'),
                ], style={'width': '55%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Br(),

                html.Div([
                    dcc.Dropdown(
                        id='module-enrol-roles-list-dropdown', style={'width': '90%'}),
                ], style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'top'}),



                html.Div([
                    dcc.Dropdown(id='module-enrol-modules-list-dropdown',
                                 style={'width': '90%'}, multi=True),
                ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),



                html.Div([
                    dcc.Dropdown(id='module-enrol-user-list-dropdown',
                                 style={'width': '90%'}, multi=True),
                ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),



                html.Div([
                    html.Div([
                        # html.Button('Enrol user in context', id='enrol-users-context-role-btn', n_clicks=0),
                        dbc.Button("Enrol user in context", color="primary",
                                   id='enrol-users-context-role-btn', n_clicks=0),
                    ], style={"text-align": "right"}),
                ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Br(),
                html.Div(id='enrol-users-context-role-response-table'),
                html.Br(),


                html.Div(id="A_C_management"),

            ], style=mainSectionBoxStyle),
            ###################################################################################
            ####################################################################
            # Creatting/Editing Competencies
            ###################################################################
            html.Br(),
            html.Div([

                html.H2("Competency Management", style={
                        "text-align": "center"}),
                ####################################################################
                ##############################################
                # Show competency frameworks
                ##############################################
                html.Br(),

                html.Div([
                    # html.Button('Show competency frameworks', id='get-competency-frameworks-information-btn', n_clicks=0),
                    dbc.Button("Show competency frameworks", color="primary",
                               id='get-competency-frameworks-information-btn', n_clicks=0),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download competency frameworks information table as csv',id='down-load-competency-frameworks-information-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='down-load-competency-frameworks-information-response-button-id', n_clicks=0),
                        dcc.Download(id='down-load-competency-frameworks-information-response-id')]),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),
                html.Br(),

                html.Div(id='competency-frameworks-information-response-table'),
                dcc.Store(id='competency-frameworks-information-response-store'),

                html.Hr(),
                html.Br(),
                ########################################
                # Create competency frameworks
                ########################################
                html.Div([
                    # html.Button('Download create competency frameworks csv template',id='down-load-create-competency-frameworks-method-template-button-id'),
                    dbc.Button("Download template", color="primary",
                               id='down-load-create-competency-frameworks-method-template-button-id', n_clicks=0),
                    dcc.Download(
                        id='down-load-create-competency-frameworks-method-template-id'),
                    # html.Button('Upload the new competency frameworks csv in the Upload Section and click to Create competency frameworks', id='create-competency-frameworks-btn', n_clicks=0),
                    dbc.Button("Upload csv and click", color="primary",
                               id='create-competency-frameworks-btn', n_clicks=0, style={"margin-left": "10px"}),
                ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width': '30%','display':'inline-block','vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download created competency frameworks table as csv',id='down-load-create-competency-frameworks-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='down-load-create-competency-frameworks-response-button-id', n_clicks=0),
                        dcc.Download(id='down-load-create-competency-frameworks-response-id')]),
                ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),


                html.Br(),

                html.Div([
                    html.Div(id='create-competency-frameworks-response-table'),
                    dcc.Store(id='create-competency-frameworks-response-store'),
                ]),

                html.Hr(),
                html.Br(),

                ############################################
                # Choose competency framework
                ############################################
                html.Div([
                    html.H5('Choose competency framework'),
                    dcc.Dropdown(id='competency-frameworks-list-dropdown',
                                 value='Top', style={'width': '40%'}),
                ]),

                html.Br(),
                html.Br(),
                html.Hr(),
                ##############################################
                # Show competencies in framework
                ##############################################
                html.Br(),
                html.Div([
                    # html.Button('Show competencies in framework', id='get-competencies-information-btn', n_clicks=0),
                    dbc.Button("Show competencies in framework", color="primary",
                               id='get-competencies-information-btn', n_clicks=0),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),


                html.Div([
                    html.Div([
                        # html.Button('Download competencies table as csv',id='down-load-competencies-information-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='down-load-competencies-information-response-button-id', n_clicks=0),
                        dcc.Download(id='down-load-competencies-information-response-id')]),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),

                html.Br(),

                html.Div(id='competencies-information-response-table'),
                dcc.Store(id='competencies-information-response-store'),

                html.Hr(),
                html.Br(),
                ########################################
                # Create competencies
                ########################################
                html.Div([
                    # html.Button('Download create competencies csv template',id='down-load-create-competencies-method-template-button-id'),
                    dbc.Button("Download template", color="primary",
                               id='down-load-create-competencies-method-template-button-id', n_clicks=0),
                    dcc.Download(
                        id='down-load-create-competencies-method-template-id'),
                    # html.Button('Upload the new competencies csv in the Upload Section and click to Create competencies', id='create-competencies-btn', n_clicks=0),
                    dbc.Button("Upload csv and click", color="primary",
                               id='create-competencies-btn', n_clicks=0, style={"margin-left": "10px"}),
                ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width': '30%','display':'inline-block','vertical-align': 'top'}),


                html.Div([
                    html.Div([
                        # html.Button('Download created competencies table as csv',id='down-load-create-competencies-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='down-load-create-competencies-response-button-id', n_clicks=0),
                        dcc.Download(id='down-load-create-competencies-response-id')]),

                ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),




                html.Div(id='create-competencies-response-table'),
                dcc.Store(id='create-competencies-response-store'),

                html.Br(),
                html.Hr(),
                html.Br(),

                ############################################
                # Choose competencies
                ############################################
                ############################################
                # Add competencies to a course
                ############################################
                html.Br(),
                html.H5('Choose competencies to add'),
                html.Br(),

                html.Div([
                    html.Div([
                        # html.Button('Get the list of competencies', id='get-competencies-btn', n_clicks=0),
                        dcc.Dropdown(id='competencies-list-dropdown', value='Top', style={'width': '70%'}, multi=True)]),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    # html.Button('Add competencies to course', id='add-competencies-to-course-btn', n_clicks=0),
                    dbc.Button("Add competencies to course", color="primary",
                               id='add-competencies-to-course-btn', n_clicks=0),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),


                html.Br(),
                html.Div(id='add-competencies-to-course-response-table'),
                html.Br(),
                html.Div(id="A_U_management"),

            ], style=mainSectionBoxStyle),
            ###################################################################################
            ####################################################################
            # User Actions
            ###################################################################
            html.Br(),
            html.Div([
                html.H2("User Management", style={"text-align": "center"}),
                html.Br(),
                ####################################################################
                html.H5("View/Edit/Create - Users"),

                html.Div([
                    # html.Button('View/Edit/Create Users', id='view-add-users-btn', n_clicks=0),
                    dbc.Button("View/Edit/Create Users", color="primary",
                               id='view-add-users-btn', n_clicks=0, style={"width": "20%"}),
                    html.A('🔗 Click to manage users', id='view-add-users-url',
                           target="_blank", style={'margin-left': '10px'}),
                ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width':'60%','display': 'inline-block','vertical-align': 'top'}),


                html.Br(),
                html.Br(),

                html.H5("View/Edit/Create - Cohorts"),
                html.Div([
                    # html.Button('View/Edit/Create Cohorts', id='view-add-cohorts-btn', n_clicks=0),
                    dbc.Button("View/Edit/Create Cohorts", color="primary",
                               id='view-add-cohorts-btn', n_clicks=0, style={"width": "20%"}),
                    html.A('🔗 Click to manage cohorts', id='view-add-cohorts-url',
                           target="_blank", style={'margin-left': '10px'}),

                ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width':'70%','display': 'inline-block','vertical-align': 'top'}),


                html.Br(),
                html.Br(),

                html.H5("Bulk User Actions"),
                html.Div([
                    # html.Button('Click to get bulk user actions', id='bulk-user-actions-btn', n_clicks=0),
                    dbc.Button("Click to get bulk user actions", color="primary",
                               id='bulk-user-actions-btn', n_clicks=0, style={"width": "20%"}),
                    html.A('🔗 Click to visit bulk user actions', id='bulk-user-actions-url',
                           target="_blank", style={'margin-left': '10px'}),
                ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width':'60%','display': 'inline-block','vertical-align': 'top'}),

                html.Br(),
                html.Br(),

                html.H5("Bulk Upload Users"),
                html.Div([
                    # html.Button('Clickt to get bulk user uploads', id='upload-users-btn', n_clicks=0),
                    dbc.Button("Click to get bulk user uploads", color="primary",
                               id='upload-users-btn', n_clicks=0, style={"width": "20%"}),
                    html.A('🔗 Click to visit bulk user actions', id='upload-users-url',
                           target="_blank", style={'margin-left': '10px'}),
                ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}),

                # html.Div([
                # ],style={'width':'60%','display': 'inline-block','vertical-align': 'top'}),
                html.Div(id="A_U_monitoring"),

            ], style=mainSectionBoxStyle),
            ####################################################################
            # User Interactions
            ###################################################################
            html.Br(),
            html.Div([
                html.H2("User Interaction Monitoring",
                        style={"text-align": "center"}),
                html.Br(),
                ###################################################################
                html.Br(),
                html.Div([html.H3('Daily User Module Interaction Figure', style={"text-align": "center"}),
                          dcc.Graph(id='user-daily-module-grades-interactions-fig',
                                    config={"displaylogo": False})
                          ]),
                html.Br(),
                html.Div([html.H3('User Module Interaction Figure', style={"text-align": "center"}),
                          dcc.Graph(id='user-module-grades-interactions-fig',
                                    config={"displaylogo": False})
                          ]),
                html.Br(),
                html.Br(),
                html.Div([

                    html.H3('Course User Grades and Interaction',
                            style={"text-align": "center"}),

                    html.Div([
                        # html.Button('Download Course User Grades and Interaction table as csv',id='download-user-grades-interactions-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='download-user-grades-interactions-button-id', n_clicks=0),
                        dcc.Download(id='download-user-grades-interactions-response-id')], style={"text-align": "right"}),

                    html.Div(id='user-grades-interactions-output'),
                    html.Div(id='user-grades-interactions-store'),
                ]),
                html.Br(),
                #################################
                html.Br(),
                html.Div([html.H3('Course User Clusters Figure', style={"text-align": "center"}),
                          dcc.Graph(id='course-user-clusters-fig',
                                    config={"displaylogo": False})
                          ]),
                html.Br(),
                html.Br(),
                html.Div([html.H3('Course User Clusters Table', style={"text-align": "center"}),
                          html.Div(id='course-user-clusters-output'),
                          dcc.Store(id='course-user-clusters-store')
                          ]),
                html.Br(),


                ###########################
                html.Br(),
                html.Hr(),
                html.Br(),
                html.H3('User Interactions', style={"text-align": "center"}),
                html.Br(),
                html.Div([html.H4('Choose Course User'),
                          dcc.Dropdown(
                              [], 'Top', id='course-users-dropdown', style={'width': '70%'})
                          ]),
                html.Br(),
                ############################
                html.Br(),
                html.Hr(),
                html.Div([html.H3('User Grades Interactions Figure', style={"text-align": "center"}),
                          dcc.Graph(id='user-grades-interactions-fig',
                                    config={"displaylogo": False})
                          ]),
                html.Br(),
                html.Br(),
                html.Br(),

                html.H3('User Grades Interactions Table',
                        style={"text-align": "center"}),

                html.Div([
                    # html.Button('Download User Grades and Interaction table as csv',id='download-grades-interactions-button-id'),
                    dbc.Button("Download csv", color="success",
                               id='download-grades-interactions-button-id', n_clicks=0),
                    dcc.Download(id='download-grades-interactions-response-id')
                ], style={"text-align": "right"}),

                html.Div(id='user-grades-interactions-output-table'),
                dcc.Store(id='user-grades-interactions-output-store'),

                html.Br(),
                html.Br(),
                ###########################
                html.Br(),
                html.Hr(),
                html.H3('User Transitions', style={"text-align": "center"}),
                html.Br(),
                html.Br(),

                html.Div([html.H3('Pick the date range'),
                          dcc.DatePickerRange(
                    id='input-date-picker-range',
                    month_format='D-M-Y-Q',
                    display_format='D-M-Y-Q',
                    min_date_allowed=date(2022, 1, 1),
                    max_date_allowed=date(2023, 12, 31),
                    initial_visible_month=date(2023, 1, 1),
                    end_date=date(2023, 12, 31)
                ),
                    html.Div(id='output-container-date-picker-range')]),
                html.Br(),
                html.Br(),
                html.Div([
                    html.H3('User Activity Transition Figure',
                            style={"text-align": "center"}),
                    dcc.Graph(id='user-activity-transition-fig',
                              config={"displaylogo": False})
                ]),
                html.Br(),
                html.H3('User Activity Transition Table',
                        style={"text-align": "center"}),

                html.Div([
                    html.Div([
                        # html.Button('Download User Activity Transition table as csv',id='download-user-activity-transition-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='download-user-activity-transition-button-id', n_clicks=0),
                        dcc.Download(id='download-user-activity-transition-response-id')])
                ], style={"text-align": "right"}),

                html.Div(id='user-activity-transition-table'),
                dcc.Store(id='user-activity-transition-store'),

                html.Br(),
                html.Br(),
                html.Div(id="A_O_monitoring"),

            ], style=mainSectionBoxStyle),

            ###########################################
            # Competency Attainment
            ###########################################
            html.Br(),
            html.Div([
                html.Div([
                    html.H2("Outcome Attainment Monitoring",
                            style={"text-align": "center"}),
                    # html.Br(),

                    # html.Div([
                    #     html.Div([html.Div([html.H4('Choose filter key'),
                    #                         dcc.Dropdown(id='col-names-list-dropdown',style={'width':'70%','align-items': 'center','justify-content':'center'})
                    #                         ],style={'width': '49%','display':'inline-block','vertical-align': 'middle'}),

                    #               html.Div([html.H4('Choose filter value'),
                    #                         dcc.Dropdown(id='col-values-list-dropdown',multi=True,style={'width':'70%'}),
                    #                         ],style={'width': '49%','display':'inline-block','vertical-align': 'middle'})
                    #             ],style={'padding':20}),
                    # html.Br(),
                    # html.Hr(),
                    html.Br(),
                    dcc.Graph(id='attainment-status-hist-fig',
                              config={"displaylogo": False}),
                    html.Br(),
                    dcc.Graph(id='max-attainment-status-hist-fig',
                              config={"displaylogo": False}),
                    html.Br(),
                    dcc.Graph(id='attainment-status-filtered-output-fig',
                              config={"displaylogo": False})
                ]),
                html.Br(),
                html.Br(),

                #     html.Div([html.H3("Choose Bar Graph Variables",style={"text-align":"center"}),
                #                 html.Div([html.H4("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
                #                 html.Div([html.H4("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
                #                 html.Div([html.H4("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'}),
                #                 html.Div([html.H4("Choose Text-variable:"), dcc.Dropdown(id='text-list-dropdown',style={'width':'90%'})],style={'width': '24%','display':'inline-block','vertical-align': 'middle'})
                #                 ],style={'padding': 10})
                #         ]),
                # html.Br(),
                # html.Div([html.H3("Choose Histogram Variables",style={"text-align":"center"}),
                #                 html.Div([html.H4("Choose x-variable:"), dcc.Dropdown(id='xcol-list-dropdown-hist',style={'width':'80%'})],style={'width': '32%','display':'inline-block','vertical-align': 'middle'}),
                #                 html.Div([html.H4("Choose y-variable:"), dcc.Dropdown(id='ycol-list-dropdown-hist',style={'width':'80%'})],style={'width': '32%','display':'inline-block','vertical-align': 'middle'}),
                #                 html.Div([html.H4("Choose Group-variable:"), dcc.Dropdown(id='gp-list-dropdown-hist',style={'width':'80%'})],style={'width': '32%','display':'inline-block','vertical-align': 'middle'})
                #                 ],style={'padding': 10}),
                html.Br(),
                html.Br(),

                html.Div([
                    # html.Button('Download csv',id='down-load-table-button-id'),
                    dbc.Button("Download csv", color="success",
                               id='down-load-table-button-id', n_clicks=0),
                    dcc.Download(id='download-table-id')], style={"text-align": "right"}),


                html.Br(),
                html.Div(id='filtered-attainment-status-output-table'),
                dcc.Store(id='attainment-status-filtered-output-store'),
                html.Br(),

            ], style=mainSectionBoxStyle),

            html.Br(),

            html.Div([
                ################################################################################################
                # Role Assignment
                ##############################################################################
                # Locally Assigned Roles-Report Section
                ########################################################################
                html.Br(),
                html.H2("Local Role Assignments: Category/Program/Section/Module",
                        style={"text-align": "center"}),
                html.Br(),
                ##############################################
                # Show categories
                ##############################################
                html.Br(),


                html.Div([
                    # html.Button('Show categories', id='lls-get-category-information-btn', n_clicks=0),
                    dbc.Button("Show categories", color="primary",
                               id='lls-get-category-information-btn', n_clicks=0),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download category information table as csv',id='lls-down-load-category-information-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='lls-down-load-category-information-response-button-id', n_clicks=0),
                        dcc.Download(id='lls-down-load-category-information-response-id')]),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),



                html.Div(id='lls-category-information-response-table'),
                dcc.Store(id='lls-category-information-response-store'),
                ##############################################
                # Show courses
                ##############################################
                html.Br(),

                html.Div([
                    # html.Button('Show category programs', id='lls-get-course-information-btn', n_clicks=0),
                    dbc.Button("Show category programs", color="primary",
                               id='lls-get-course-information-btn', n_clicks=0),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download program information table as csv',id='lls-down-load-course-information-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='lls-down-load-course-information-response-button-id', n_clicks=0),
                        dcc.Download(id='lls-down-load-course-information-response-id')]),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),


                html.Div(id='lls-course-information-response-table'),
                dcc.Store(id='lls-course-information-response-store'),
                ##############################################
                # Show sections
                ##############################################
                html.Br(),

                html.Div([
                    # html.Button('Show program sections', id='lls-get-sections-information-btn', n_clicks=0),
                    dbc.Button("Show program sections", color="primary",
                               id='lls-get-sections-information-btn', n_clicks=0),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download section information table as csv',id='lls-down-load-sections-information-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='lls-down-load-sections-information-response-button-id', n_clicks=0),
                        dcc.Download(id='lls-down-load-sections-information-response-id')]),
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),


                html.Div(id='lls-sections-information-response-table'),
                dcc.Store(id='lls-sections-information-response-store'),

                ##############################################
                # Show activities
                ##############################################
                html.Br(),

                html.Div([
                    # html.Button('Show program activities', id='lls-get-course-assignments-list-btn', n_clicks=0),
                    dbc.Button("Show program activities", color="primary",
                               id='lls-get-course-assignments-list-btn', n_clicks=0),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download activity information table as csv',id='lls-down-load-modules-information-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='lls-down-load-modules-information-response-button-id', n_clicks=0),
                        dcc.Download(id='lls-down-load-modules-information-response-id')]),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),

                html.Div(id='lls-course-modules-info-response-table'),
                dcc.Store(id='lls-course-modules-info-response-store'),

                ##############################################
                # Show schedules
                ##############################################
                html.Br(),

                html.Div([
                    # html.Button('Show program schedules', id='lls-get-course-schedules-list-btn', n_clicks=0),
                    dbc.Button("Show program schedules", color="primary",
                               id='lls-get-course-schedules-list-btn', n_clicks=0),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div([
                        # html.Button('Download schedules information table as csv',id='lls-down-load-schedules-information-response-button-id'),
                        dbc.Button("Download csv", color="success",
                                   id='lls-down-load-schedules-information-response-button-id', n_clicks=0),
                        dcc.Download(id='lls-down-load-schedules-information-response-id')]),

                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'right'}),

                html.Div(id='lls-course-schedules-info-response-table'),
                dcc.Store(id='lls-course-schedules-info-response-store'),
            ], style={'display': 'none'}),

            html.Div([
            ]),

        ], style={
            'margin': '15px',
            "background-image": "url('assets/bg2(60).jpg')",
            # "background-repeat": "no-repeat",
            # "background-position": "right top",
            # "background-size": "150px 100px"

        }),
    ])
    return appLayout
