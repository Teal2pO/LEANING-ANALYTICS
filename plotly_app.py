import base64
import io

import json
import pandas as pd
import plotly.graph_objects as go
#from jupyter_dash import JupyterDash

import requests

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app_fns.plotly_callback import *
from app_fns.app_functions import *
from app_fns.app_layout import *

from serverConfig import *
import dash_bootstrap_components as dbc

#Create the app
#app = Dash(__name__) #for local server
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__,suppress_callback_exceptions=True,url_base_pathname='/{}/adminpanel/'.format(moodlename)) #,external_stylesheets=external_stylesheets)
app = Dash(__name__,external_stylesheets=[dbc.themes.CERULEAN],suppress_callback_exceptions=True,url_base_pathname='/{}/adminpanel/'.format(moodlename)) #,external_stylesheets=external_stylesheets)

server=app.server
app.title='Admin'

mgAPPfns=the_app_functions()

appLayout=plotly_app_layout()

###########################
#Test API Call Section
###########################
callback_get_methods_btn=(Output('methods-list-dropdown', 'options'),Input('click-to-begin-btn', 'n_clicks'))
get_methods_btn=plotly_call_back()
get_methods_btn.get_inputs_give_outputs(app,callback_get_methods_btn,**{'callbackfunction':mgAPPfns.get_methods_list_without_arguments,'fnParams':{'webserviceurl':webserviceurl}})

callback_test_clkbtn=(Output('API-method-arguments-table', 'children'),Input('get-method-arguments-btn', 'n_clicks'),State('methods-list-dropdown', 'value'))
test_clkbtn=plotly_call_back()
test_clkbtn.get_inputs_give_outputs(app,callback_test_clkbtn,**{'callbackfunction':mgAPPfns.show_method_arguments,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_clkbtn=(Output('API-response-table', 'children'),Output('API-response-store', 'data'),Input('execute-api-call-btn', 'n_clicks'),State('methods-list-dropdown', 'value'),State('input-data', 'value'))
clkbtn=plotly_call_back()
clkbtn.get_inputs_give_outputs(app,callback_clkbtn,**{'callbackfunction':mgAPPfns.call_web_service_return_table,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_response=(Output('down-load-API-response-id','data'),Input('down-load-API-response-button-id', 'n_clicks'),Input('API-response-store', 'data'))
dowload_API_response=plotly_call_back()
dowload_API_response.get_inputs_give_outputs(app,callback_dowload_API_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

######################################################
#csv upload and store Section 4 Admin Panel
######################################################
callback_csvupload2=(Output('csv-upload-2-div-output','children'),Output('upload-2-df-store','data'),Input('csv-upload-2','contents'))
csvupload2=plotly_call_back()
csvupload2.get_inputs_give_outputs(app,callback_csvupload2,**{'callbackfunction':mgAPPfns.csv_upload_div_return_and_store,'fnParams':{}})

###########################
#csv upload and bulk API actions
###########################
callback_get_bulk_methods_btn=(Output('bulk-methods-dropdown', 'options'),Input('click-to-begin-btn', 'n_clicks'))
get_bulk_methods_btn=plotly_call_back()
get_bulk_methods_btn.get_inputs_give_outputs(app,callback_get_bulk_methods_btn,**{'callbackfunction':mgAPPfns.get_bulk_action_arguments_list,'fnParams':{'webserviceurl':webserviceurl}})

callback_dowload_bulk_template=(Output('down-load-bulk-method-template-id','data'),Input('down-load-bulk-method-template-button-id', 'n_clicks'),State('bulk-methods-dropdown', 'value'))
dowload_bulk_template=plotly_call_back()
dowload_bulk_template.get_inputs_give_outputs(app,callback_dowload_bulk_template,**{'callbackfunction':mgAPPfns.download_bulk_action_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_bulk_API=(Output('API-bulk-response-table','children'),Output('API-bulk-response-store2','data'),Input('execute-bulk-api-call-btn', 'n_clicks'),State('bulk-methods-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_bulk_API=plotly_call_back()
csvupload_bulk_API.get_inputs_give_outputs(app,callback_csvupload_bulk_API,**{'callbackfunction':mgAPPfns.get_4m_store_and_callweb_API,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_bulk_response=(Output('down-load-API-bulk-response-id','data'),Input('down-load-API-bulk-response-button-id', 'n_clicks'),Input('API-bulk-response-store2', 'data'))
dowload_API_bulk_response=plotly_call_back()
dowload_API_bulk_response.get_inputs_give_outputs(app,callback_dowload_API_bulk_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})



######################################################
#Category/Course/Section/Modules Selection Section
######################################################
##################################
#Choose category
#################################
callback_get_cats_btn=(Output('category-list-dropdown', 'options'),Input('click-to-begin-btn', 'n_clicks'))
get_cats_btn=plotly_call_back()
get_cats_btn.get_inputs_give_outputs(app,callback_get_cats_btn,**{'callbackfunction':mgAPPfns.get_category_list,'fnParams':{'webserviceurl':webserviceurl}})
########################################
#Choose Course
########################################
callback_get_cat_courses=(Output('category-course-dropdown', 'options'),Input('category-list-dropdown','value'))
get_cat_courses=plotly_call_back()
get_cat_courses.get_inputs_give_outputs(app,callback_get_cat_courses,**{'callbackfunction':mgAPPfns.get_category_course_list,'fnParams':{'webserviceurl':webserviceurl}})
########################################
#Choose section
########################################
callback_get_course_sections=(Output('course-sections-dropdown', 'options'),Input('category-course-dropdown','value'))
get_course_sections=plotly_call_back()
get_course_sections.get_inputs_give_outputs(app,callback_get_course_sections,**{'callbackfunction':mgAPPfns.get_course_sections_list,'fnParams':{'webserviceurl':webserviceurl}})
###################################################################
#Choose module
#################################################################### 
callback_get_course_modules=(Output('course-modules-dropdown', 'options'),Input('category-course-dropdown','value'),Input('course-sections-dropdown','value'))
get_course_modules=plotly_call_back()
get_course_modules.get_inputs_give_outputs(app,callback_get_course_modules,**{'callbackfunction':mgAPPfns.get_course_section_modules_list,'fnParams':{'webserviceurl':webserviceurl}})


########################################################################################

##############################################################################
#View Category/Course/Section/Module for the Admin panel
########################################################################
##################################
#View category
#################################
callback_category_infor_table=(Output('category-information-response-table','children'),Output('category-information-response-store','data'),Input('get-category-information-btn', 'n_clicks'))
category_infor_table=plotly_call_back()
category_infor_table.get_inputs_give_outputs(app,callback_category_infor_table,**{'callbackfunction':mgAPPfns.get_category_info,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_down_load_category_information=(Output('down-load-category-information-response-id','data'),Input('down-load-category-information-response-button-id', 'n_clicks'),Input('category-information-response-store', 'data'))
down_load_category_information=plotly_call_back()
down_load_category_information.get_inputs_give_outputs(app,callback_down_load_category_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#View category courses
#################################
callback_course_infor_table=(Output('course-information-response-table','children'),Output('course-information-response-store','data'),Input('get-course-information-btn', 'n_clicks'),State('category-list-dropdown', 'value'))
course_infor_table=plotly_call_back()
course_infor_table.get_inputs_give_outputs(app,callback_course_infor_table,**{'callbackfunction':mgAPPfns.get_category_course_info,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_down_load_course_information=(Output('down-load-course-information-response-id','data'),Input('down-load-course-information-response-button-id', 'n_clicks'),Input('course-information-response-store', 'data'))
down_load_course_information=plotly_call_back()
down_load_course_information.get_inputs_give_outputs(app,callback_down_load_course_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#View course sections
#################################
callback_sections_infor_table=(Output('sections-information-response-table','children'),Output('sections-information-response-store','data'),Input('get-sections-information-btn', 'n_clicks'),State('category-course-dropdown', 'value'))
sections_infor_table=plotly_call_back()
sections_infor_table.get_inputs_give_outputs(app,callback_sections_infor_table,**{'callbackfunction':mgAPPfns.get_course_sections_info,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_down_load_sections_information=(Output('down-load-sections-information-response-id','data'),Input('down-load-sections-information-response-button-id', 'n_clicks'),Input('sections-information-response-store', 'data'))
down_load_sections_information=plotly_call_back()
down_load_sections_information.get_inputs_give_outputs(app,callback_down_load_sections_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#View course modules
#################################
callback_module_infor_table=(Output('course-modules-info-response-table','children'),Output('course-modules-info-response-store','data'),Input('get-course-assignments-list-btn', 'n_clicks'),State('category-course-dropdown', 'value'))
module_infor_table=plotly_call_back()
module_infor_table.get_inputs_give_outputs(app,callback_module_infor_table,**{'callbackfunction':mgAPPfns.get_course_modules_list,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_down_load_modules_information=(Output('down-load-modules-information-response-id','data'),Input('down-load-modules-information-response-button-id', 'n_clicks'),Input('course-modules-info-response-store', 'data'))
down_load_modules_information=plotly_call_back()
down_load_modules_information.get_inputs_give_outputs(app,callback_down_load_modules_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

###################################################################################
############################################
#Edit category - Moodle
############################################click-to-begin-btn

callback_view_cat=(Output('view-cat-url','src'),Input('click-to-begin-btn', 'n_clicks')) #,Input('category-list-dropdown', 'value'),Input('click-to-begin-btn', 'n_clicks')
view_cat=plotly_call_back()
view_cat.get_inputs_give_outputs(app,callback_view_cat,**{'callbackfunction':mgAPPfns.edit_course_categories,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

########################################
#Create categories
########################################
callback_dowload_create_categories_template=(Output('down-load-create-categories-method-template-id','data'),Input('down-load-create-categories-method-template-button-id', 'n_clicks'))
dowload_create_categories_template=plotly_call_back()
dowload_create_categories_template.get_inputs_give_outputs(app,callback_dowload_create_categories_template,**{'callbackfunction':mgAPPfns.download_create_categories_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_1_admin_API=(Output('create-categories-response-table','children'),Output('create-categories-response-store','data'),Input('create-categories-btn', 'n_clicks'),State('upload-2-df-store', 'data'))
csvupload_1_admin_API=plotly_call_back()
csvupload_1_admin_API.get_inputs_give_outputs(app,callback_csvupload_1_admin_API,**{'callbackfunction':mgAPPfns.create_categories,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_1_admin_response=(Output('down-load-create-categories-response-id','data'),Input('down-load-create-categories-response-button-id', 'n_clicks'),Input('create-categories-response-store', 'data'))
dowload_API_1_admin_response=plotly_call_back()
dowload_API_1_admin_response.get_inputs_give_outputs(app,callback_dowload_API_1_admin_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

###############################################################################################
########################################
#Edit course
########################################
callback_edit_course=(Output('edit-course-url','href'),Input('category-course-dropdown','value')) #,Input('edit-course-btn', 'n_clicks')
edit_course=plotly_call_back()
edit_course.get_inputs_give_outputs(app,callback_edit_course,**{'callbackfunction':mgAPPfns.edit_course,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

########################################
#Enroll course users
########################################
callback_enrol_users=(Output('enrol-users-url','href'),Input('category-course-dropdown','value')) #,Input('enrol-users-btn', 'n_clicks')
enrol_users=plotly_call_back()
enrol_users.get_inputs_give_outputs(app,callback_enrol_users,**{'callbackfunction':mgAPPfns.enrol_users_in_course,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_get_roles_users_list=(Output('roles-list-dropdown', 'options'),Output('user-list-4-roles-dropdown', 'options'),Input('click-to-begin-btn', 'n_clicks')) #Input('get-roles-users-list-btn', 'n_clicks')
get_roles_users_list=plotly_call_back()
get_roles_users_list.get_inputs_give_outputs(app,callback_get_roles_users_list,**{'callbackfunction':mgAPPfns.get_users_and_roles_list,'fnParams':{'webserviceurl':webserviceurl}})

callback_enrol_users_in_course_in_role=(Output('enrol-users-course-role-response-table','children'),Input('category-course-dropdown', 'value'),State('roles-list-dropdown', 'value'),State('user-list-4-roles-dropdown', 'value'))
enrol_users_in_course_in_role_clk=plotly_call_back()
enrol_users_in_course_in_role_clk.get_inputs_give_outputs(app,callback_enrol_users_in_course_in_role,**{'callbackfunction':mgAPPfns.enrol_users_in_course_in_role,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

########################################
#Create courses
########################################
callback_dowload_create_course_template=(Output('down-load-create-courses-method-template-id','data'),Input('down-load-create-courses-method-template-button-id', 'n_clicks'))
dowload_create_course_template=plotly_call_back()
dowload_create_course_template.get_inputs_give_outputs(app,callback_dowload_create_course_template,**{'callbackfunction':mgAPPfns.download_create_course_in_category_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_2_admin_API=(Output('create-courses-response-table','children'),Output('create-courses-response-store','data'),Input('create-course-btn', 'n_clicks'),State('category-list-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_2_admin_API=plotly_call_back()
csvupload_2_admin_API.get_inputs_give_outputs(app,callback_csvupload_2_admin_API,**{'callbackfunction':mgAPPfns.create_courses_in_category,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_2_admin_response=(Output('down-load-create-courses-response-id','data'),Input('down-load-create-courses-response-button-id', 'n_clicks'),Input('create-courses-response-store', 'data'))
dowload_API_2_admin_response=plotly_call_back()
dowload_API_2_admin_response.get_inputs_give_outputs(app,callback_dowload_API_2_admin_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

################################################################################################
########################################
#Edit section
########################################
callback_edit_course_sections=(Output('edit-course-section-url','href'),Input('course-sections-dropdown','value'))
edit_course_sections=plotly_call_back()
edit_course_sections.get_inputs_give_outputs(app,callback_edit_course_sections,**{'callbackfunction':mgAPPfns.edit_course_section,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

########################################
#Create Section
########################################
callback_dowload_create_section_template=(Output('down-load-create-sections-method-template-id','data'),Input('down-load-create-sections-method-template-button-id', 'n_clicks'))
dowload_create_section_template=plotly_call_back()
dowload_create_section_template.get_inputs_give_outputs(app,callback_dowload_create_section_template,**{'callbackfunction':mgAPPfns.download_create_sections_in_course_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_3_admin_API=(Output('create-sections-response-table','children'),Output('create-sections-response-store','data'),Input('create-sections-btn', 'n_clicks'),State('category-course-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_3_admin_API=plotly_call_back()
csvupload_3_admin_API.get_inputs_give_outputs(app,callback_csvupload_3_admin_API,**{'callbackfunction':mgAPPfns.create_sections_in_course,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_3_admin_response=(Output('down-load-create-sections-response-id','data'),Input('down-load-create-sections-response-button-id', 'n_clicks'),Input('create-sections-response-store', 'data'))
dowload_API_3_admin_response=plotly_call_back()
dowload_API_3_admin_response.get_inputs_give_outputs(app,callback_dowload_API_3_admin_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

#############################################################################################
###################################################################
#Edit module
#################################################################### 
callback_edit_module=(Output('edit-module-url','href'),Input('course-modules-dropdown','value'))
edit_module=plotly_call_back()
edit_module.get_inputs_give_outputs(app,callback_edit_module,**{'callbackfunction':mgAPPfns.edit_module,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

###################################################################
#Enroll users in module
#################################################################### 
callback_enroll_module=(Output('enroll-module-url','href'),Input('course-modules-dropdown','value'))
enroll_module=plotly_call_back()
enroll_module.get_inputs_give_outputs(app,callback_enroll_module,**{'callbackfunction':mgAPPfns.edit_module_role_assignments,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


###################################################################
#Create assignments
####################################################################
callback_dowload_create_activities_template=(Output('down-load-create-activities-method-template-id','data'),Input('down-load-create-activities-method-template-button-id', 'n_clicks'))
dowload_create_activities_template=plotly_call_back()
dowload_create_activities_template.get_inputs_give_outputs(app,callback_dowload_create_activities_template,**{'callbackfunction':mgAPPfns.download_create_activities_in_section_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_4_admin_API=(Output('create-activities-response-table','children'),Output('create-activities-response-store','data'),Input('create-activities-btn', 'n_clicks'),State('category-course-dropdown','value'),State('course-sections-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_4_admin_API=plotly_call_back()
csvupload_4_admin_API.get_inputs_give_outputs(app,callback_csvupload_4_admin_API,**{'callbackfunction':mgAPPfns.create_assignments_in_course_section,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_4_admin_response=(Output('down-load-create-activities-response-id','data'),Input('down-load-create-activities-response-button-id', 'n_clicks'),Input('create-activities-response-store', 'data'))
dowload_API_4_admin_response=plotly_call_back()
dowload_API_4_admin_response.get_inputs_give_outputs(app,callback_dowload_API_4_admin_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

###################################################################
#Create schedules
####################################################################
callback_dowload_create_schedules_template=(Output('down-load-create-schedules-method-template-id','data'),Input('down-load-create-schedules-method-template-button-id', 'n_clicks'))
dowload_create_schedules_template=plotly_call_back()
dowload_create_schedules_template.get_inputs_give_outputs(app,callback_dowload_create_schedules_template,**{'callbackfunction':mgAPPfns.download_create_schedules_in_section_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_5_admin_API=(Output('create-schedules-response-table','children'),Output('create-schedules-response-store','data'),Input('create-schedules-btn', 'n_clicks'),State('category-course-dropdown','value'),State('course-sections-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_5_admin_API=plotly_call_back()
csvupload_5_admin_API.get_inputs_give_outputs(app,callback_csvupload_5_admin_API,**{'callbackfunction':mgAPPfns.create_schedules_in_course_section,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_5_admin_response=(Output('down-load-create-schedules-response-id','data'),Input('down-load-create-schedules-response-button-id', 'n_clicks'),Input('create-schedules-response-store', 'data'))
dowload_API_5_admin_response=plotly_call_back()
dowload_API_5_admin_response.get_inputs_give_outputs(app,callback_dowload_API_5_admin_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

###########################
#csv upload and bulk create hvp MCQ quiz
###########################
callback_dowload_bulk_hvp_mcq_template=(Output('down-load-bulk-hvp-mcq-template-id','data'),Input('down-load-bulk-hvp-mcq-template-button-id', 'n_clicks'))
dowload_bulk_hvp_mcq_template=plotly_call_back()
dowload_bulk_hvp_mcq_template.get_inputs_give_outputs(app,callback_dowload_bulk_hvp_mcq_template,**{'callbackfunction':mgAPPfns.download_bulk_hvp_mcq_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_bulk_hvp_mcq=(Output('bulk-hvp-mcq-response-table','children'),Output('bulk-hvp-mcq-response-store','data'),Input('execute-bulk-hvp-mcq-call-btn', 'n_clicks'),State('mcq-hvp-templateid-input-id', 'value'),State('mcq-hvp-title-input-id', 'value'),State('category-course-dropdown', 'value'),State('course-sections-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_bulk_hvp_mcq=plotly_call_back()
csvupload_bulk_hvp_mcq.get_inputs_give_outputs(app,callback_csvupload_bulk_hvp_mcq,**{'callbackfunction':mgAPPfns.get_4m_store_and_call_create_hvp_MCQ_quiz,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_hvp_mcq_response=(Output('down-load-bulk-hvp-mcq-response-id','data'),Input('down-load-bulk-hvp-mcq-response-button-id', 'n_clicks'),Input('bulk-hvp-mcq-response-store', 'data'))
dowload_hvp_mcq_response=plotly_call_back()
dowload_hvp_mcq_response.get_inputs_give_outputs(app,callback_dowload_hvp_mcq_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_chatgpt_hvp_mcq=(Output('chatgpt-hvp-mcq-response-table','children'),Output('chatgpt-hvp-mcq-response-store','data'),Output('ai-hvp-mcq-view','children'),Input('execute-ai-hvp-mcq-call-btn', 'n_clicks'),State('ai-mcq-question-numbers-input-id', 'value'),State('ai-mcq-question-Language-input-id', 'value'),State('mcq-hvp-templateid-input-id', 'value'),State('mcq-hvp-title-input-id', 'value'),State('category-course-dropdown', 'value'),State('course-sections-dropdown', 'value'))
chatgpt_hvp_mcq=plotly_call_back()
chatgpt_hvp_mcq.get_inputs_give_outputs(app,callback_chatgpt_hvp_mcq,**{'callbackfunction':mgAPPfns.chatgpt_create_hvp_MCQ_quiz,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_chatgpt_hvp_mcq_response=(Output('down-load-chatgpt-hvp-mcq-response-id','data'),Input('down-load-chatgpt-hvp-mcq-response-button-id', 'n_clicks'),Input('chatgpt-hvp-mcq-response-store', 'data'))
dowload_chatgpt_hvp_mcq_response=plotly_call_back()
dowload_chatgpt_hvp_mcq_response.get_inputs_give_outputs(app,callback_dowload_chatgpt_hvp_mcq_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

###########################
#csv upload and bulk create hvp SW quiz
###########################
callback_dowload_bulk_hvp_sw_template=(Output('down-load-bulk-hvp-sw-template-id','data'),Input('down-load-bulk-hvp-sw-template-button-id', 'n_clicks'))
dowload_bulk_hvp_sw_template=plotly_call_back()
dowload_bulk_hvp_sw_template.get_inputs_give_outputs(app,callback_dowload_bulk_hvp_sw_template,**{'callbackfunction':mgAPPfns.download_bulk_hvp_sw_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_bulk_hvp_sw=(Output('bulk-hvp-sw-response-table','children'),Output('bulk-hvp-sw-response-store','data'),Input('execute-bulk-hvp-sw-call-btn', 'n_clicks'),State('sw-hvp-templateid-input-id', 'value'),State('sw-hvp-title-input-id', 'value'),State('category-course-dropdown', 'value'),State('course-sections-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_bulk_hvp_sw=plotly_call_back()
csvupload_bulk_hvp_sw.get_inputs_give_outputs(app,callback_csvupload_bulk_hvp_sw,**{'callbackfunction':mgAPPfns.get_4m_store_and_call_create_hvp_SW_quiz,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_hvp_sw_response=(Output('down-load-bulk-hvp-sw-response-id','data'),Input('down-load-bulk-hvp-sw-response-button-id', 'n_clicks'),Input('bulk-hvp-sw-response-store', 'data'))
dowload_hvp_sw_response=plotly_call_back()
dowload_hvp_sw_response.get_inputs_give_outputs(app,callback_dowload_hvp_sw_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

###########################
#csv upload and bulk create moodle quiz
###########################
callback_dowload_bulk_exam_quiz_template=(Output('down-load-bulk-exam-quiz-template-id','data'),Input('down-load-bulk-exam-quiz-template-button-id', 'n_clicks'))
dowload_bulk_exam_quiz_template=plotly_call_back()
dowload_bulk_exam_quiz_template.get_inputs_give_outputs(app,callback_dowload_bulk_exam_quiz_template,**{'callbackfunction':mgAPPfns.download_bulk_exam_quiz_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_bulk_exam_quiz=(Output('exam-quiz-response-table','children'),Output('exam-quiz-response-store','data'),Input('execute-bulk-exam-quiz-call-btn', 'n_clicks'),State('upload-2-df-store', 'data'))
csvupload_bulk_exam_quiz=plotly_call_back()
csvupload_bulk_exam_quiz.get_inputs_give_outputs(app,callback_csvupload_bulk_exam_quiz,**{'callbackfunction':mgAPPfns.get_4m_store_and_call_create_exam_quiz,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_bulk_exam_quiz=(Output('down-load-bulk-exam-quiz-response-id','data'),Input('down-load-bulk-exam-quiz-response-button-id', 'n_clicks'),State('exam-quiz-response-store', 'data'))
dowload_bulk_exam_quiz=plotly_call_back()
dowload_bulk_exam_quiz.get_inputs_give_outputs(app,callback_dowload_bulk_exam_quiz,**{'callbackfunction':mgAPPfns.download_xml,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


##################################################################################
#Assign context roles
##################################################################################
# callback_get_module_cats_btn=(Output('module-categories-list-dropdown', 'options'),Input('get-module-categories-list-btn', 'n_clicks'))
# get_module_cats_btn=plotly_call_back()
# get_module_cats_btn.get_inputs_give_outputs(app,callback_get_module_cats_btn,**{'callbackfunction':mgAPPfns.get_category_list,'fnParams':{'webserviceurl':webserviceurl}})

# callback_get_module_role_cat_courses=(Output('module-category-courses-list-dropdown', 'options'),Input('get-module-courses-list-btn', 'n_clicks'),State('module-categories-list-dropdown','value'))
# get_module_role_cat_courses=plotly_call_back()
# get_module_role_cat_courses.get_inputs_give_outputs(app,callback_get_module_role_cat_courses,**{'callbackfunction':mgAPPfns.get_category_course_list,'fnParams':{'webserviceurl':webserviceurl}})

#category-list-dropdown
#course-sections-dropdown

callback_get_assign_module_roles_menus=(Output('module-enrol-roles-list-dropdown', 'options'),Output('module-enrol-modules-list-dropdown', 'options'),Output('module-enrol-user-list-dropdown', 'options'),Input('category-course-dropdown','value'))
get_assign_module_roles_menus=plotly_call_back()
get_assign_module_roles_menus.get_inputs_give_outputs(app,callback_get_assign_module_roles_menus,**{'callbackfunction':mgAPPfns.get_roles_course_contexts_users_list,'fnParams':{'webserviceurl':webserviceurl}})

callback_assign_users_context_role=(Output('enrol-users-context-role-response-table','children'),Input('enrol-users-context-role-btn', 'n_clicks'),State('module-enrol-roles-list-dropdown', 'value'),State('module-enrol-modules-list-dropdown', 'value'),State('module-enrol-user-list-dropdown', 'value'))
assign_users_context_role_clk=plotly_call_back()
assign_users_context_role_clk.get_inputs_give_outputs(app,callback_assign_users_context_role,**{'callbackfunction':mgAPPfns.assign_users_module_role,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


####################################################################  
##################################
#View competency frameworks
#################################
callback_frameworks_information_infor_table=(Output('competency-frameworks-information-response-table','children'),Output('competency-frameworks-information-response-store','data'),Input('get-competency-frameworks-information-btn', 'n_clicks'))
frameworks_information_infor_table=plotly_call_back()
frameworks_information_infor_table.get_inputs_give_outputs(app,callback_frameworks_information_infor_table,**{'callbackfunction':mgAPPfns.get_competency_frameworks,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_down_load_frameworks_information_information=(Output('down-load-competency-frameworks-information-response-id','data'),Input('down-load-competency-frameworks-information-response-button-id', 'n_clicks'),Input('competency-frameworks-information-response-store', 'data'))
down_load_frameworks_information_information=plotly_call_back()
down_load_frameworks_information_information.get_inputs_give_outputs(app,callback_down_load_frameworks_information_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})



########################################
#Create competency frameworks
########################################
callback_dowload_create_competency_frameworks_template=(Output('down-load-create-competency-frameworks-method-template-id','data'),Input('down-load-create-competency-frameworks-method-template-button-id', 'n_clicks'))
dowload_create_competency_frameworks_template=plotly_call_back()
dowload_create_competency_frameworks_template.get_inputs_give_outputs(app,callback_dowload_create_competency_frameworks_template,**{'callbackfunction':mgAPPfns.download_create_competency_frameworks_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_cf_admin_API=(Output('create-competency-frameworks-response-table','children'),Output('create-competency-frameworks-response-store','data'),Input('create-competency-frameworks-btn', 'n_clicks'),State('category-list-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_cf_admin_API=plotly_call_back()
csvupload_cf_admin_API.get_inputs_give_outputs(app,callback_csvupload_cf_admin_API,**{'callbackfunction':mgAPPfns.create_competency_frameworks_in_category,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_cf_admin_response=(Output('down-load-create-competency-frameworks-response-id','data'),Input('down-load-create-competency-frameworks-response-button-id', 'n_clicks'),Input('create-competency-frameworks-response-store', 'data'))
dowload_API_cf_admin_response=plotly_call_back()
dowload_API_cf_admin_response.get_inputs_give_outputs(app,callback_dowload_API_cf_admin_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#Choose competency framework
#################################
callback_competency_frameworks_cats_btn=(Output('competency-frameworks-list-dropdown', 'options'),Input('click-to-begin-btn', 'n_clicks'))
competency_frameworks_cats_btn=plotly_call_back()
competency_frameworks_cats_btn.get_inputs_give_outputs(app,callback_competency_frameworks_cats_btn,**{'callbackfunction':mgAPPfns.get_competency_frameworks_list,'fnParams':{'webserviceurl':webserviceurl}})


##################################
#View competencies in framework
#################################
callback_competencies_information_table=(Output('competencies-information-response-table','children'),Output('competencies-information-response-store','data'),Input('get-competencies-information-btn', 'n_clicks'),State('competency-frameworks-list-dropdown', 'value'))
competencies_information_table=plotly_call_back()
competencies_information_table.get_inputs_give_outputs(app,callback_competencies_information_table,**{'callbackfunction':mgAPPfns.get_competencies_by_frameworkids,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_down_load_competencies_information=(Output('down-load-competencies-information-response-id','data'),Input('down-load-competencies-information-response-button-id', 'n_clicks'),Input('competencies-information-response-store', 'data'))
down_load_competencies_information=plotly_call_back()
down_load_competencies_information.get_inputs_give_outputs(app,callback_down_load_competencies_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


########################################
#Create competencies
########################################
callback_dowload_create_competencies_template=(Output('down-load-create-competencies-method-template-id','data'),Input('down-load-create-competencies-method-template-button-id', 'n_clicks'))
dowload_create_competencies_template=plotly_call_back()
dowload_create_competencies_template.get_inputs_give_outputs(app,callback_dowload_create_competencies_template,**{'callbackfunction':mgAPPfns.download_create_competencies_template,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_csvupload_comp_admin_API=(Output('create-competencies-response-table','children'),Output('create-competencies-response-store','data'),Input('create-competencies-btn', 'n_clicks'),State('competency-frameworks-list-dropdown', 'value'),State('upload-2-df-store', 'data'))
csvupload_comp_admin_API=plotly_call_back()
csvupload_comp_admin_API.get_inputs_give_outputs(app,callback_csvupload_comp_admin_API,**{'callbackfunction':mgAPPfns.create_competencies_in_framework,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_API_comp_admin_response=(Output('down-load-create-competencies-response-id','data'),Input('down-load-create-competencies-response-button-id', 'n_clicks'),Input('create-competencies-response-store', 'data'))
dowload_API_comp_admin_response=plotly_call_back()
dowload_API_comp_admin_response.get_inputs_give_outputs(app,callback_dowload_API_comp_admin_response,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


##################################
#Choose competencies
#################################
callback_competencies_cats_btn=(Output('competencies-list-dropdown', 'options'),Input('competency-frameworks-list-dropdown', 'value'))
competencies_cats_btn=plotly_call_back()
competencies_cats_btn.get_inputs_give_outputs(app,callback_competencies_cats_btn,**{'callbackfunction':mgAPPfns.get_competencies_by_frameworkid_list,'fnParams':{'webserviceurl':webserviceurl}})

##################################
#Add competencies to course
#################################
callback_add_competencies_to_course=(Output('add-competencies-to-course-response-table','children'),Input('add-competencies-to-course-btn', 'n_clicks'),State('category-course-dropdown', 'value'),State('competencies-list-dropdown', 'value'))
add_competencies_to_course=plotly_call_back()
add_competencies_to_course.get_inputs_give_outputs(app,callback_add_competencies_to_course,**{'callbackfunction':mgAPPfns.add_competencies_to_course,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


################################################################################
######################################################################
#User Actions
####################################################################
callback_view_add_users=(Output('view-add-users-url','href'),Input('view-add-users-btn', 'n_clicks'))
view_add_users=plotly_call_back()
view_add_users.get_inputs_give_outputs(app,callback_view_add_users,**{'callbackfunction':mgAPPfns.view_add_users,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_view_add_cohorts=(Output('view-add-cohorts-url','href'),Input('view-add-cohorts-btn', 'n_clicks'))
view_add_cohorts=plotly_call_back()
view_add_cohorts.get_inputs_give_outputs(app,callback_view_add_cohorts,**{'callbackfunction':mgAPPfns.view_add_cohorts,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_bulk_user_actions=(Output('bulk-user-actions-url','href'),Input('bulk-user-actions-btn', 'n_clicks'))
bulk_user_actions=plotly_call_back()
bulk_user_actions.get_inputs_give_outputs(app,callback_bulk_user_actions,**{'callbackfunction':mgAPPfns.bulk_user_actions,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_upload_users=(Output('upload-users-url','href'),Input('upload-users-btn', 'n_clicks'))
upload_users=plotly_call_back()
upload_users.get_inputs_give_outputs(app,callback_upload_users,**{'callbackfunction':mgAPPfns.upload_users,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##########################################################################
#Project Management
#########################################################################

#callback_get_cols_btn=(Output('col-names-list-dropdown','options'),Input('click-to-begin-btn', 'n_clicks'))
#get_cols_btn=plotly_call_back()
#get_cols_btn.get_inputs_give_outputs(app,callback_get_cols_btn,**{'callbackfunction':mgAPPfns.get_col_names2,'fnParams':{'webserviceurl':webserviceurl}})

# callback_get_label_btn=(Output('col-values-list-dropdown','options'),Input('col-names-list-dropdown','value'))
# get_label_btn=plotly_call_back()
# get_label_btn.get_inputs_give_outputs(app,callback_get_label_btn,**{'callbackfunction':mgAPPfns.get_given_col_labels,'fnParams':{'webserviceurl':webserviceurl}})

# callback_get_filter_btn=(Output('filtered-attainment-status-output-table','children'),Output('attainment-status-filtered-output-store','data'),Input('col-names-list-dropdown','value'),Input('col-values-list-dropdown','value'))
# get_filter_btn=plotly_call_back()
# get_filter_btn.get_inputs_give_outputs(app,callback_get_filter_btn,**{'callbackfunction':mgAPPfns.get_filtered_framework_assignments,'fnParams':{'webserviceurl':webserviceurl}})

# callback_get_attainment_btn=(Output('xcol-list-dropdown','options'),Output('ycol-list-dropdown','options'),Output('gp-list-dropdown','options'),Output('text-list-dropdown','options'),Input('click-to-begin-btn', 'n_clicks'))
# get_attainment_btn=plotly_call_back()
# get_attainment_btn.get_inputs_give_outputs(app,callback_get_attainment_btn,**{'callbackfunction':mgAPPfns.get_attainment_info_fig_menus,'fnParams':{'webserviceurl':webserviceurl}})

# callback_get_attainment_level_btn=(Output('xcol-list-dropdown-hist','options'),Output('ycol-list-dropdown-hist','options'),Output('gp-list-dropdown-hist','options'),Input('click-to-begin-btn', 'n_clicks'))
# get_attainment_level_btn=plotly_call_back()
# get_attainment_level_btn.get_inputs_give_outputs(app,callback_get_attainment_level_btn,**{'callbackfunction':mgAPPfns.get_attainment_levels_fig_menus,'fnParams':{'webserviceurl':webserviceurl}})

# callback_attainment_level=(Output('attainment-status-filtered-output-hist-fig','figure'),Input('click-to-begin-btn', 'n_clicks'),Input('attainment-status-filtered-output-store', 'data'),Input('xcol-list-dropdown-hist','value'),Input('ycol-list-dropdown-hist','value'),Input('gp-list-dropdown-hist','value'))
# test_attainment_level=plotly_call_back()
# test_attainment_level.get_inputs_give_outputs(app,callback_attainment_level,**{'callbackfunction':mgAPPfns.get_attainment_levels_fig,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

# callback_dowload_table=(Output('download-table-id','data'),Input('down-load-table-button-id', 'n_clicks'),State('attainment-status-filtered-output-store', 'data'))
# dowload_table=plotly_call_back()
# dowload_table.get_inputs_give_outputs(app,callback_dowload_table,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##########################################################################
#Competency Attianment
#########################################################################
# callback_get_cols_btn=(Output('col-names-list-dropdown','options'),Input('click-to-begin-btn', 'n_clicks'),Input('category-list-dropdown','value'))
# get_cols_btn=plotly_call_back()
# get_cols_btn.get_inputs_give_outputs(app,callback_get_cols_btn,**{'callbackfunction':mgAPPfns.get_category_courses_competency_attainment_filter_columns,'fnParams':{'webserviceurl':webserviceurl}})

# callback_get_label_btn=(Output('col-values-list-dropdown','options'),Input('col-names-list-dropdown','value'),State('category-list-dropdown','value'))
# get_label_btn=plotly_call_back()
# get_label_btn.get_inputs_give_outputs(app,callback_get_label_btn,**{'callbackfunction':mgAPPfns.get_course_competency_attainment_given_col_labels,'fnParams':{'webserviceurl':webserviceurl}})

callback_get_filter_btn=(Output('filtered-attainment-status-output-table','children'),Output('attainment-status-filtered-output-store','data'),Output('attainment-status-hist-fig','figure'),Output('max-attainment-status-hist-fig','figure'),Output('attainment-status-filtered-output-fig','figure'),Input('click-to-begin-btn', 'n_clicks'),Input('category-list-dropdown','value'))
get_filter_btn=plotly_call_back()
get_filter_btn.get_inputs_give_outputs(app,callback_get_filter_btn,**{'callbackfunction':mgAPPfns.get_category_course_competency_attainment,'fnParams':{'webserviceurl':webserviceurl}})

# callback_get_attainment_btn=(Output('xcol-list-dropdown','options'),Output('ycol-list-dropdown','options'),Output('gp-list-dropdown','options'),Output('text-list-dropdown','options'),Input('click-to-begin-btn', 'n_clicks'),Input('attainment-status-filtered-output-store', 'data'))
# get_attainment_btn=plotly_call_back()
# get_attainment_btn.get_inputs_give_outputs(app,callback_get_attainment_btn,**{'callbackfunction':mgAPPfns.get_course_attainment_info_fig_menus,'fnParams':{'webserviceurl':webserviceurl}})

# callback_attainment_status=(Output('attainment-status-filtered-output-fig','figure'),Input('click-to-begin-btn', 'n_clicks'),Input('attainment-status-filtered-output-store', 'data'),Input('xcol-list-dropdown','value'),Input('ycol-list-dropdown','value'),Input('gp-list-dropdown','value'),Input('text-list-dropdown','value'))
# test_attainment_status=plotly_call_back()
# test_attainment_status.get_inputs_give_outputs(app,callback_attainment_status,**{'callbackfunction':mgAPPfns.get_attainment_info_fig,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

# callback_get_attainment_level_btn=(Output('xcol-list-dropdown-hist','options'),Output('ycol-list-dropdown-hist','options'),Output('gp-list-dropdown-hist','options'),Input('click-to-begin-btn', 'n_clicks'),Input('attainment-status-filtered-output-store', 'data'))
# get_attainment_level_btn=plotly_call_back()
# get_attainment_level_btn.get_inputs_give_outputs(app,callback_get_attainment_level_btn,**{'callbackfunction':mgAPPfns.get_course_attainment_levels_fig_menus,'fnParams':{'webserviceurl':webserviceurl}})

# callback_attainment_level=(Output('attainment-status-filtered-output-hist-fig','figure'),Input('click-to-begin-btn', 'n_clicks'),Input('attainment-status-filtered-output-store', 'data'),Input('xcol-list-dropdown-hist','value'),Input('ycol-list-dropdown-hist','value'),Input('gp-list-dropdown-hist','value'))
# test_attainment_level=plotly_call_back()
# test_attainment_level.get_inputs_give_outputs(app,callback_attainment_level,**{'callbackfunction':mgAPPfns.get_attainment_levels_fig,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_table=(Output('download-table-id','data'),Input('down-load-table-button-id', 'n_clicks'),State('attainment-status-filtered-output-store', 'data'))
dowload_table=plotly_call_back()
dowload_table.get_inputs_give_outputs(app,callback_dowload_table,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


##########################################################################
#User Interactions
#########################################################################


#Outputs
callback_get_course_grades_interaction=(Output('user-daily-module-grades-interactions-fig','figure'),Output('user-module-grades-interactions-fig','figure'),Output('user-grades-interactions-output','children'),Output('user-grades-interactions-store','data'),Input('category-course-dropdown',"value"))
get_course_grades_interaction=plotly_call_back()
get_course_grades_interaction.get_inputs_give_outputs(app,callback_get_course_grades_interaction,**{'callbackfunction':mgAPPfns.get_modules_users_grades_dedications_by_courses,'fnParams':{'webserviceurl':webserviceurl}})

callback_dowload_course_grades_table=(Output('download-user-grades-interactions-response-id','data'),Input('download-user-grades-interactions-button-id', 'n_clicks'),State('user-grades-interactions-store', 'data'))
dowload_course_grades_table=plotly_call_back()
dowload_course_grades_table.get_inputs_give_outputs(app,callback_dowload_course_grades_table,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})


##########################
callback_get_course_user_clusters=(Output('course-user-clusters-output','children'),Output('course-user-clusters-store','data'),Input('category-course-dropdown',"value"))
get_course_user_clusters=plotly_call_back()
get_course_user_clusters.get_inputs_give_outputs(app,callback_get_course_user_clusters,**{'callbackfunction':mgAPPfns.get_course_user_clusters,'fnParams':{'webserviceurl':webserviceurl}})

callback_get_course_user_clusters_fig=(Output('course-user-clusters-fig','figure'),Input('course-user-clusters-store','data'))
get_course_user_clusters_fig=plotly_call_back()
get_course_user_clusters_fig.get_inputs_give_outputs(app,callback_get_course_user_clusters_fig,**{'callbackfunction':mgAPPfns.get_course_user_clusters_fig3d,'fnParams':{'webserviceurl':webserviceurl}})

########################
callback_get_users_btn=(Output('course-users-dropdown', 'options'),Input('category-course-dropdown',"value"))
get_users_btn=plotly_call_back()
get_users_btn.get_inputs_give_outputs(app,callback_get_users_btn,**{'callbackfunction':mgAPPfns.get_course_users_list,'fnParams':{'webserviceurl':webserviceurl}})


callback_get_module_interaction=(Output('user-grades-interactions-fig','figure'),Output('user-grades-interactions-output-table','children'),Output('user-grades-interactions-output-store','data'),Input('course-users-dropdown',"value"))
get_module_interaction=plotly_call_back()
get_module_interaction.get_inputs_give_outputs(app,callback_get_module_interaction,**{'callbackfunction':mgAPPfns.get_modules_user_grades_dedications_by_users,'fnParams':{'webserviceurl':webserviceurl}})

callback_dowload_user_grades_table=(Output('download-grades-interactions-response-id','data'),Input('download-grades-interactions-button-id', 'n_clicks'),State('user-grades-interactions-output-store', 'data'))
dowload_user_grades_table=plotly_call_back()
dowload_user_grades_table.get_inputs_give_outputs(app,callback_dowload_user_grades_table,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

#######################################

callback_user_activity_transition_fig=(Output('user-activity-transition-fig','figure'),Input('course-users-dropdown',"value"),Input('input-date-picker-range', 'start_date'),Input('input-date-picker-range', 'end_date'))
user_activity_transition_btn=plotly_call_back()
user_activity_transition_btn.get_inputs_give_outputs(app,callback_user_activity_transition_fig,**{'callbackfunction':mgAPPfns.get_user_context_events_fig,'fnParams':{'webserviceurl':webserviceurl}})

callback_test_time=(Output('user-activity-transition-table','children'),Output('user-activity-transition-store','data'),Input('course-users-dropdown',"value"),Input('input-date-picker-range', 'start_date'),Input('input-date-picker-range', 'end_date'))
test_time=plotly_call_back()
test_time.get_inputs_give_outputs(app,callback_test_time,**{'callbackfunction':mgAPPfns.get_user_context_events,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

callback_dowload_user_transitions_table=(Output('download-user-activity-transition-response-id','data'),Input('download-user-activity-transition-button-id', 'n_clicks'),State('user-activity-transition-store', 'data'))
dowload_user_transitions_table=plotly_call_back()
dowload_user_transitions_table.get_inputs_give_outputs(app,callback_dowload_user_transitions_table,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

########################################################################################
#Local Role-Assignments
##############################################################################
#View Category/Program/Section/Module for the Admin panel
########################################################################
##################################
#View category
#################################
lls_callback_category_infor_table=(Output('lls-category-information-response-table','children'),Output('lls-category-information-response-store','data'),Input('lls-get-category-information-btn', 'n_clicks'))
lls_category_infor_table=plotly_call_back()
lls_category_infor_table.get_inputs_give_outputs(app,lls_callback_category_infor_table,**{'callbackfunction':mgAPPfns.get_category_info,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

lls_callback_down_load_category_information=(Output('lls-down-load-category-information-response-id','data'),Input('lls-down-load-category-information-response-button-id', 'n_clicks'),Input('lls-category-information-response-store', 'data'))
lls_down_load_category_information=plotly_call_back()
lls_down_load_category_information.get_inputs_give_outputs(app,lls_callback_down_load_category_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#View category courses
#################################
lls_callback_course_infor_table=(Output('lls-course-information-response-table','children'),Output('lls-course-information-response-store','data'),Input('lls-get-course-information-btn', 'n_clicks'),State('category-list-dropdown', 'value'))
lls_course_infor_table=plotly_call_back()
lls_course_infor_table.get_inputs_give_outputs(app,lls_callback_course_infor_table,**{'callbackfunction':mgAPPfns.get_category_course_info,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

lls_callback_down_load_course_information=(Output('lls-down-load-course-information-response-id','data'),Input('lls-down-load-course-information-response-button-id', 'n_clicks'),Input('lls-course-information-response-store', 'data'))
lls_down_load_course_information=plotly_call_back()
lls_down_load_course_information.get_inputs_give_outputs(app,lls_callback_down_load_course_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#View course sections
#################################
lls_callback_sections_infor_table=(Output('lls-sections-information-response-table','children'),Output('lls-sections-information-response-store','data'),Input('lls-get-sections-information-btn', 'n_clicks'),State('category-course-dropdown', 'value'))
lls_sections_infor_table=plotly_call_back()
lls_sections_infor_table.get_inputs_give_outputs(app,lls_callback_sections_infor_table,**{'callbackfunction':mgAPPfns.get_course_sections_info,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

lls_callback_down_load_sections_information=(Output('lls-down-load-sections-information-response-id','data'),Input('lls-down-load-sections-information-response-button-id', 'n_clicks'),Input('lls-sections-information-response-store', 'data'))
lls_down_load_sections_information=plotly_call_back()
lls_down_load_sections_information.get_inputs_give_outputs(app,lls_callback_down_load_sections_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#View course assignments
#################################
lls_callback_module_infor_table=(Output('lls-course-modules-info-response-table','children'),Output('lls-course-modules-info-response-store','data'),Input('lls-get-course-assignments-list-btn', 'n_clicks'),State('category-course-dropdown', 'value'))
lls_module_infor_table=plotly_call_back()
lls_module_infor_table.get_inputs_give_outputs(app,lls_callback_module_infor_table,**{'callbackfunction':mgAPPfns.get_course_assignments_list,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

lls_callback_down_load_modules_information=(Output('lls-down-load-modules-information-response-id','data'),Input('lls-down-load-modules-information-response-button-id', 'n_clicks'),Input('lls-course-modules-info-response-store', 'data'))
lls_down_load_modules_information=plotly_call_back()
lls_down_load_modules_information.get_inputs_give_outputs(app,lls_callback_down_load_modules_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

##################################
#View course schedules
#################################
lls_callback_schedules_infor_table=(Output('lls-course-schedules-info-response-table','children'),Output('lls-course-schedules-info-response-store','data'),Input('lls-get-course-schedules-list-btn', 'n_clicks'),State('category-course-dropdown', 'value'))
lls_schedules_infor_table=plotly_call_back()
lls_schedules_infor_table.get_inputs_give_outputs(app,lls_callback_schedules_infor_table,**{'callbackfunction':mgAPPfns.get_course_schedules_list,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

lls_callback_down_load_schedules_information=(Output('lls-down-load-schedules-information-response-id','data'),Input('lls-down-load-schedules-information-response-button-id', 'n_clicks'),Input('lls-course-schedules-info-response-store', 'data'))
lls_down_load_schedules_information=plotly_call_back()
lls_down_load_schedules_information.get_inputs_give_outputs(app,lls_callback_down_load_schedules_information,**{'callbackfunction':mgAPPfns.download_csv,'fnParams':{'webserviceurl':webserviceurl, 'siteurl':siteURL}})

# ##########################################################################
# #HVP-Interactions
# ###########################################################################

# callback_add_hvp=(Output('view-hvp-url','href'),Input('add-video-btn', 'n_clicks'),Input('lmsm-course-modules-dropdown',"value"),Input('video-url-value','value'))
# add_hvp=plotly_call_back()
# add_hvp.get_inputs_give_outputs(app,callback_add_hvp,**{'callbackfunction':mgAPPfns.add_hvp_interactions,'fnParams':{'webserviceurl':webserviceurl}})
# ##########################################################################

#Run the app
app.layout = html.Div(appLayout)
if __name__ == '__main__':
    app.run_server(debug=True)


