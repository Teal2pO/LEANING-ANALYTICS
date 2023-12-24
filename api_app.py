#90% complete 07/03/2023
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine #, text as sql_text

from flask import request, jsonify, Flask
# from flask_ngrok import run_with_ngrok

#from TEAL_packages.general_tools import *
from mg_methods.db_manipulation import *
from mg_methods.github_access import *
from mg_methods.lms_functions import *
from mg_methods.hvp_editor_functions import *
from app_fns.api_service import *

from serverConfig import *



#Moodle Webservice Access setup
ENDPOINT="/webservice/rest/server.php"
moodleWebserviceAccessParams={'KEY':KEY,'URL':siteURL,'ENDPOINT':ENDPOINT}
engineMoodle = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(user, password,host, dbname)) #.connect()
connectionMoodle=engineMoodle.connect()
connectionMoodle.close()

#Inititializing the classes
mgDB=mugas_DB_functions(engineMoodle)
mgGH=TEALGitHub()
hvp=hvp_interactive_video(moodleWebserviceAccessParams,engineMoodle)
mgLRM=api_functions(mgDB,mgGH,moodleWebserviceAccessParams,GHAparams,engineMoodle)

method_names['get_methods_list']=mgLRM.get_methods_list
method_names['get_methods_list_without_arguments']=mgLRM.get_methods_list_without_arguments
method_names['get_method_signature']=mgLRM.get_method_signature
method_names['get_bulk_action_arguments_list']=mgLRM.get_bulk_action_arguments_list
method_names['call_moodle_webservice']=mgLRM.call_moodle_webservice
method_names['get_sql_request']=mgLRM.get_sql_request
method_names['get_fig_menus']=mgLRM.get_fig_menus

#Add to API methods the web_API
#ChatGPT
method_names['call_chatgpt_API']=mgLRM.call_chatgpt_API

#Moodle quiz
method_names['create_moodle_quiz']=mgLRM.create_moodle_quiz
method_names['ai_generated_general_MCQ_quiz']=mgLRM.ai_generated_general_MCQ_quiz
#HVP Methods
method_names['create_hvp_module']=mgLRM.create_hvp_module
method_names['update_hvp_module']=mgLRM.update_hvp_module
method_names['get_hvp_interactions']=mgLRM.get_hvp_interactions
method_names['create_hvp_MCQ_quiz']=mgLRM.create_hvp_MCQ_quiz
method_names['create_hvp_SW_quiz']=mgLRM.create_hvp_SW_quiz
method_names['ai_generated_language_hvp_MCQ_quiz']=mgLRM.ai_generated_language_hvp_MCQ_quiz
method_names['ai_generated_general_hvp_MCQ_quiz']=mgLRM.ai_generated_general_hvp_MCQ_quiz

##Github manipulation
method_names['get_GitHub_organization_repos']=mgGH.get_GitHub_organization_repos
method_names['get_repo_info']=mgGH.get_repo_info
method_names['create_calendar_events']=mgLRM.create_calendar_events
method_names['change_edit_mode']=mgLRM.change_edit_mode

#The core xAPI
method_names['core_xapi_statement_post']=mgLRM.core_xapi_statement_post

##Competencies
method_names['create_scales']=mgLRM.create_scales
method_names['create_competency_frameworks']=mgLRM.create_competency_frameworks
method_names['create_competencies']=mgLRM.create_competencies
method_names['add_competencies_to_course']=mgLRM.add_competencies_to_course
method_names['add_module_competencies']=mgLRM.add_module_competencies
method_names['get_modules_competencies']=mgLRM.get_modules_competencies
method_names['get_modules_by_competencies']=mgLRM.get_modules_by_competencies
method_names['get_courses_by_competencies']=mgLRM.get_courses_by_competencies
method_names['get_competencies_by_frameworkids']=mgLRM.get_competencies_by_frameworkids
method_names['get_competencies_by_frameworkid_list']=mgLRM.get_competencies_by_frameworkid_list
method_names['get_competency_frameworks']=mgLRM.get_competency_frameworks
method_names['get_competency_frameworks_list']=mgLRM.get_competency_frameworks_list
method_names['get_modules_users_information_by_competencies']=mgLRM.get_modules_users_information_by_competencies
method_names['get_assignment_users_information_by_competencies']=mgLRM.get_assignment_users_information_by_competencies
method_names['get_users_module_competencies']=mgLRM.get_users_module_competencies

##Scheduler
method_names['get_course_scheduler_events_full_info']=mgLRM.get_course_scheduler_events_full_info
method_names['get_scheduler_events_full_info_by_modules']=mgLRM.get_scheduler_events_full_info_by_modules
method_names['get_course_scheduler_events_full_info_by_role_by_userids']=mgLRM.get_course_scheduler_events_full_info_by_role_by_userids

##Moodle category 
method_names['create_course_category']=mgLRM.create_course_category
method_names['create_course_categories_bulk']=mgLRM.create_course_categories_bulk
method_names['create_course_categories']=mgLRM.create_course_categories
method_names['delete_course_categories']=mgLRM.delete_course_categories
method_names['edit_course_categories']=mgLRM.edit_course_categories
method_names['get_dashboard']=mgLRM.get_dashboard
method_names['get_mycourses_link']=mgLRM.get_mycourses_link
method_names['get_category_list']=mgLRM.get_category_list
method_names['get_categories_get_categorynames_list']=mgLRM.get_categories_get_categorynames_list
method_names['get_user_role_get_categorynames_list']=mgLRM.get_user_role_get_categorynames_list
method_names['manage_category_cohorts']=mgLRM.manage_category_cohorts
method_names['manage_category_roles']=mgLRM.manage_category_roles
method_names['view_course_category']=mgLRM.view_course_category
 
##Moodle course functions
method_names['get_roles_all_courses']=mgLRM.get_roles_all_courses
method_names['get_course_assignment_local_roles_full_info']=mgLRM.get_course_assignment_local_roles_full_info
method_names['get_assignment_local_roles_full_info_by_modules']=mgLRM.get_assignment_local_roles_full_info_by_modules
method_names['get_course_assignment_local_roles_full_info_by_role_by_userids']=mgLRM.get_course_assignment_local_roles_full_info_by_role_by_userids
method_names['get_course_modules_local_roles_full_info']=mgLRM.get_course_modules_local_roles_full_info
method_names['get_modules_local_roles_full_info_by_ids']=mgLRM.get_modules_local_roles_full_info_by_ids
method_names['get_category_course_full_information']=mgLRM.get_category_course_full_information
method_names['get_categories_course_full_information']=mgLRM.get_categories_course_full_information
method_names['get_course_modules_full_info']=mgLRM.get_course_modules_full_info
method_names['get_modules_full_info_by_ids']=mgLRM.get_modules_full_info_by_ids
method_names['get_course_modules_by_type']=mgLRM.get_course_modules_by_type
method_names['get_section_modules_by_type']=mgLRM.get_section_modules_by_type
method_names['add_activity_module_2_course_section']=mgLRM.add_activity_module_2_course_section
method_names['create_course']=mgLRM.create_course
method_names['create_courses']=mgLRM.create_courses
method_names['create_courses_in_category']=mgLRM.create_courses_in_category
method_names['create_course_4m_moodle_template']=mgLRM.create_course_4m_moodle_template
method_names['create_course_section']=mgLRM.create_course_section
method_names['create_course_sections']=mgLRM.create_course_sections
method_names['create_course_sections_in_course']=mgLRM.create_course_sections_in_course
method_names['create_course_module']=mgLRM.create_course_module
method_names['create_assignments_in_course_section']=mgLRM.create_assignments_in_course_section
method_names['create_schedules_in_course_section']=mgLRM.create_schedules_in_course_section
method_names['create_assignments']=mgLRM.create_assignments
method_names['create_schedules']=mgLRM.create_schedules
method_names['delete_courses']=mgLRM.delete_courses
method_names['delete_sections']=mgLRM.delete_sections
method_names['delete_modules']=mgLRM.delete_modules
method_names['duplicate_course']=mgLRM.duplicate_course
method_names['duplicate_module']=mgLRM.duplicate_module
method_names['edit_course']=mgLRM.edit_course
method_names['edit_course_section']=mgLRM.edit_course_section
method_names['edit_course_section_visibility']=mgLRM.edit_course_section_visibility
method_names['edit_module']=mgLRM.edit_module
method_names['edit_module_role_assignments']=mgLRM.edit_module_role_assignments
method_names['edit_module_visibility']=mgLRM.edit_module_visibility
method_names['enrol_users_in_course']=mgLRM.enrol_users_in_course
method_names['get_category_contextid']=mgLRM.get_category_contextid
method_names['get_category_info']=mgLRM.get_category_info
method_names['get_category_course_info']=mgLRM.get_category_course_info
method_names['get_category_course_list']=mgLRM.get_category_course_list
method_names['get_categories_course_list']=mgLRM.get_categories_course_list
method_names['get_context_user_roleids']=mgLRM.get_context_user_roleids
method_names['get_context_user_roles']=mgLRM.get_context_user_roles
method_names['get_context_all_users_and_roles']=mgLRM.get_context_all_users_and_roles
method_names['get_context_user_inherited_roles']=mgLRM.get_context_user_inherited_roles
method_names['get_course_contextid']=mgLRM.get_course_contextid
method_names['get_course_modules']=mgLRM.get_course_modules
method_names['get_course_modules_list']=mgLRM.get_course_modules_list
method_names['get_course_module_by_id']=mgLRM.get_course_module_by_id
method_names['get_course_section_from_section_id']=mgLRM.get_course_section_from_section_id
method_names['get_course_sections_list']=mgLRM.get_course_sections_list
method_names['get_courses_sections_list']=mgLRM.get_courses_sections_list
method_names['get_course_sections_info']=mgLRM.get_course_sections_info
method_names['get_course_section_modules']=mgLRM.get_course_section_modules
method_names['get_course_section_modules_list']=mgLRM.get_course_section_modules_list
method_names['get_courses_sections_modules_list']=mgLRM.get_courses_sections_modules_list
method_names['get_courses_users']=mgLRM.get_courses_users
method_names['get_courses_users_list']=mgLRM.get_courses_users_list
method_names['get_course_users_list']=mgLRM.get_course_users_list
method_names['get_section_modules_list_by_type']=mgLRM.get_section_modules_list_by_type
method_names['get_hvp_content_json']=mgLRM.get_hvp_content_json
method_names['get_module_contextid']=mgLRM.get_module_contextid
method_names['get_modules_contextids']=mgLRM.get_modules_contextids
method_names['get_module_contexts_info']=mgLRM.get_module_contexts_info
method_names['get_module_full_info_by_id']=mgLRM.get_module_full_info_by_id
method_names['get_module_section_in_course']=mgLRM.get_module_section_in_course
method_names['get_system_user_rolenames']=mgLRM.get_system_user_rolenames
method_names['get_user_capabilities']=mgLRM.get_user_capabilities
method_names['get_user_contextid']=mgLRM.get_user_contextid
method_names['get_users_modules_by_type_by_role_ids']=mgLRM.get_users_modules_by_type_by_role_ids
method_names['get_users_modules_grades']=mgLRM.get_users_modules_grades
method_names['get_users_assignments_by_roles_by_cutoffdate']=mgLRM.get_users_assignments_by_roles_by_cutoffdate
method_names['move_course_section']=mgLRM.move_course_section
method_names['update_course_section']=mgLRM.update_course_section
method_names['update_course_sections']=mgLRM.update_course_sections
method_names['update_course_module']=mgLRM.update_course_module
method_names['view_course']=mgLRM.view_course
method_names['view_module']=mgLRM.view_module
method_names['view_my_courses_moodle']=mgLRM.view_my_courses_moodle
method_names['get_contextid_from_module_instance']=mgLRM.get_contextid_from_module_instance
method_names['get_module_files']=mgLRM.get_module_files

##Admin functions
method_names['bulk_user_actions']=mgLRM.bulk_user_actions
method_names['upload_users']=mgLRM.upload_users
method_names['view_add_users']=mgLRM.view_add_users
method_names['view_add_cohorts']=mgLRM.view_add_cohorts


##Moodle user functions
method_names['get_users_by_field']=mgLRM.get_users_by_field
method_names['create_users']=mgLRM.create_users
method_names['delete_users']=mgLRM.delete_users
method_names['create_user']=mgLRM.create_user
method_names['get_all_users']=mgLRM.get_all_users
method_names['get_user_courses']=mgLRM.get_user_courses
method_names['get_user_info']=mgLRM.get_user_info
method_names['get_user_id_list']=mgLRM.get_user_id_list
method_names['get_user_role_context_get_instances']=mgLRM.get_user_role_context_get_instances

##Moodle user enrollments
method_names['get_role_id_list']=mgLRM.get_role_id_list
method_names['get_user_roles']=mgLRM.get_user_roles
method_names['assign_module_roles']=mgLRM.assign_module_roles
method_names['assign_users_contexts_role_from_instances']=mgLRM.assign_users_contexts_role_from_instances
method_names['assign_users_contexts_role_from_contexts']=mgLRM.assign_users_contexts_role_from_contexts
method_names['unassign_module_roles']=mgLRM.unassign_module_roles
method_names['manual_enrol_cohort_in_course']=mgLRM.manual_enrol_cohort_in_course
method_names['manual_enrol_user_in_course']=mgLRM.manual_enrol_user_in_course
method_names['manual_enrol_users_in_courses']=mgLRM.manual_enrol_users_in_courses
method_names['manual_enrol_system_users_in_courses']=mgLRM.manual_enrol_system_users_in_courses
method_names['manual_enrol_users_in_course_in_role']=mgLRM.manual_enrol_users_in_course_in_role
method_names['manual_unenrol_users_in_courses']=mgLRM.manual_unenrol_users_in_courses
method_names['manual_unenrol_cohort_in_course']=mgLRM.manual_unenrol_cohort_in_course
method_names['manual_unenrol_user_in_course']=mgLRM.manual_unenrol_user_in_course

##Moodle user ineraction monitoring
method_names['get_user_course_activity_completion']=mgLRM.get_user_course_activity_completion
method_names['get_user_module_lms_interaction_graph']=mgLRM.get_user_module_lms_interaction_graph
method_names['get_user_module_lms_daily_interaction_graph']=mgLRM.get_user_module_lms_daily_interaction_graph
method_names['get_user_module_lms_interaction_graph_fig']=mgLRM.get_user_module_lms_interaction_graph_fig
method_names['get_user_module_lms_interaction']=mgLRM.get_user_module_lms_interaction
method_names['get_user_module_lms_interaction_in_a_day']=mgLRM.get_user_module_lms_interaction_in_a_day
method_names['get_user_course_lms_interaction_in_a_day']=mgLRM.get_user_course_lms_interaction_in_a_day
method_names['get_user_lms_interaction_in_a_day']=mgLRM.get_user_lms_interaction_in_a_day
method_names['get_user_course_lms_interaction']=mgLRM.get_user_course_lms_interaction
method_names['get_user_context_events']=mgLRM.get_user_context_events
method_names['get_user_context_connectivity']=mgLRM.get_user_context_connectivity
method_names['get_user_context_connectivity_new']=mgLRM.get_user_context_connectivity_new
method_names['get_user_context_connectivity_figure']=mgLRM.get_user_context_connectivity_figure
method_names['get_users_graph_properties']=mgLRM.get_users_graph_properties
method_names['get_course_users_module_interaction']=mgLRM.get_course_users_module_interaction
method_names['get_users_modules_dedication']=mgLRM.get_users_modules_dedication
method_names['get_grades_dedications_by_users_by_modules']=mgLRM.get_grades_dedications_by_users_by_modules
method_names['get_course_modules_user_grades_dedications_by_users']=mgLRM.get_course_modules_user_grades_dedications_by_users
method_names['get_users_module_contexts_info']=mgLRM.get_users_module_contexts_info
method_names['get_modules_users_dedication']=mgLRM.get_modules_users_dedication
method_names['get_course_user_dedication']=mgLRM.get_course_user_dedication
method_names['get_module_user_dedication']=mgLRM.get_module_user_dedication
method_names['get_course_user_clusters']=mgLRM.get_course_user_clusters
method_names['get_course_user_clusters_figures']=mgLRM.get_course_user_clusters_figures
##Moodle cohort manipulations
method_names['add_cohort_members']=mgLRM.add_cohort_members
method_names['create_category_cohorts']=mgLRM.create_category_cohorts
method_names['create_cohorts']=mgLRM.create_cohorts
method_names['delete_cohort_members']=mgLRM.delete_cohort_members
method_names['get_cohorts']=mgLRM.get_cohorts
method_names['get_cohort_members']=mgLRM.get_cohort_members

##Moodle Group Management
method_names['add_group_members']=mgLRM.add_group_members
method_names['create_course_groups']=mgLRM.create_course_groups
method_names['get_course_groups']=mgLRM.get_course_groups
method_names['get_group_members']=mgLRM.get_group_members

#Grades
method_names['get_modules_users_grades_dedications_competencies']=mgLRM.get_modules_users_grades_dedications_competencies
method_names['get_modules_users_grades_dedications_by_courses']=mgLRM.get_modules_users_grades_dedications_by_courses
method_names['get_modules_users_grades_dedications_by_courses_figures']=mgLRM.get_modules_users_grades_dedications_by_courses_figures
method_names['get_modules_users_dedications_by_courses']=mgLRM.get_modules_users_dedications_by_courses
method_names['get_modules_user_grades_dedications_by_users']=mgLRM.get_modules_user_grades_dedications_by_users
method_names['get_modules_user_grades_dedications_by_users_figures']=mgLRM.get_modules_user_grades_dedications_by_users_figures
method_names['get_module_users_grade']=mgLRM.get_module_users_grade
method_names['get_all_modules_student_grades']=mgLRM.get_all_modules_student_grades
method_names['get_all_modules_student_grades_by_courses']=mgLRM.get_all_modules_student_grades_by_courses
method_names['get_all_modules_student_grades_by_userses']=mgLRM.get_all_modules_student_grades_by_userses
method_names['get_all_student_grades_by_modules']=mgLRM.get_all_student_grades_by_modules
method_names['get_categories_course_modules_student_grades_competency']=mgLRM.get_categories_course_modules_student_grades_competency
method_names['get_categories_course_modules_student_grades_competency_figures']=mgLRM.get_categories_course_modules_student_grades_competency_figures
method_names['get_courses_modules_student_grades_competency']=mgLRM.get_courses_modules_student_grades_competency
method_names['get_all_modules_local_student_grades_competency']=mgLRM.get_all_modules_local_student_grades_competency
method_names['get_all_modules_local_student_grades_competency_full_info']=mgLRM.get_all_modules_local_student_grades_competency_full_info
method_names['get_courses_modules_student_grades_competency_full_info']=mgLRM.get_courses_modules_student_grades_competency_full_info
method_names['get_all_modules_course_student_grades_competency']=mgLRM.get_all_modules_course_student_grades_competency
method_names['update_course_module_grades']=mgLRM.update_course_module_grades
#####Not used

method_names['delete_courses']=mgLRM.delete_courses
method_names['get_course_users']=mgLRM.get_course_users
method_names['get_course_users_by_rolename']=mgLRM.get_course_users_by_rolename
method_names['get_course_module_by_section_by_name']=mgLRM.get_course_module_by_section_by_name
method_names['update_course_category_name']=mgLRM.update_course_category_name

#####################
#LLS-Methods
method_names['get_cobds']=mgLRM.get_cobds
method_names['get_program_users_assignments_schedules_info']=mgLRM.get_program_users_assignments_schedules_info

#Run the app
app = Flask(__name__)
#run_with_ngrok(app) #Comment to run on server
app=web_API(app)
#app.run()

#################
#method_names['get_schedule_events_course']=mgLRM.get_schedule_events_course
# method_names['get_schedule_list']=mgLRM.get_schedule_list
# method_names['get_schedule_events_student']=mgLRM.get_schedule_events_student
# method_names['get_schedule_events_teacher']=mgLRM.get_schedule_events_teacher
# method_names['get_schedule_events_user']=mgLRM.get_schedule_events_user
##DB Manipulation
# method_names['get_table_records_in']=mgLRM.get_table_records_in
# method_names['update_table_record']=mgLRM.update_table_record
# method_names['update_table_record_by_id']=mgLRM.update_table_record_by_id
# method_names['insert_records']=mgLRM.insert_records