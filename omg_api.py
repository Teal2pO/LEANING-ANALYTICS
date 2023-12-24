#90% complete 07/03/2023
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine #, text as sql_text

from flask import request, jsonify, Flask
# from flask_ngrok import run_with_ngrok

#from TEAL_packages.general_tools import *
from mg_methods.omg_db import *
from app_fns.api_service import *

from serverConfig import *



#Moodle Webservice Access setup
ENDPOINT="/webservice/rest/server.php"
moodleWebserviceAccessParams={'KEY':KEY,'URL':siteURL,'ENDPOINT':ENDPOINT}
engineDB = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(user, password,host, dbname)) #.connect()
connectionDB=engineDB.connect()
connectionDB.close()

#Inititializing the classes

mgLRM=api_functions(moodleWebserviceAccessParams,engineDB)

method_names['get_methods_list']=mgLRM.get_methods_list
method_names['get_methods_list_without_arguments']=mgLRM.get_methods_list_without_arguments
method_names['get_method_signature']=mgLRM.get_method_signature
method_names['call_moodle_webservice']=mgLRM.call_moodle_webservice
method_names['get_sql_request']=mgLRM.get_sql_request


#Add to API methods the web_API
#ChatGPT
method_names['call_chatgpt_API']=mgLRM.call_chatgpt_API

#Moodle quiz
method_names['create_moodle_quiz']=mgLRM.create_moodle_quiz

#Run the app
app = Flask(__name__)
#run_with_ngrok(app) #Comment to run on server
app=web_API(app)
#app.run()

