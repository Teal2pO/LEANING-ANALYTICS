#LRM-Webclient Function definitions - 09/03/2023:1616
import numpy as np
import itertools
import json
import copy
import inspect
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from requests import get, post
from pandas import DataFrame, to_datetime, concat, DateOffset, read_sql
from sqlalchemy import text as sql_text
import time
from datetime import datetime
import pytz
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)
from github import Github



import sklearn
from sklearn.mixture import GaussianMixture
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import r_regression
from pytube import YouTube
from pathlib import Path
import os
import re
import sys
import xmltodict



class api_functions:
    def __init__(self,DBAccessObj,GHAccessObj,mWAParams,GHAParams,SQLengine):
        self.mWAP=mWAParams
        self.engine=SQLengine
        self.mgDB=DBAccessObj
        self.mgGH=GHAccessObj
        self.GHAP=GHAParams
        self.contentDict={}
        self.hvp_local_methods={}
        self.hvp_local_methods['update_hvp_MCQ_questions']=self.update_hvp_MCQ_questions
        self.hvp_local_methods['update_hvp_SW']=self.update_hvp_SW
        self.hvp_local_methods['update_hvp_videointeractions_MCQ']=self.update_hvp_videointeractions_MCQ
        self.hvp_local_methods['get_hvp_video_interactions']=self.get_hvp_video_interactions
        self.hvp_local_methods['get_hvp_MCQ_questions']=self.get_hvp_MCQ_questions
        self.hvp_local_methods['get_hvp_SW_questions']=self.get_hvp_SW_questions
        self.chatgpt_methods={}
        self.chatgpt_methods['get_general_response']=self.get_general_response
        self.chatgpt_methods['create_language_mcq_questions']=self.create_language_mcq_questions
        self.chatgpt_methods['create_general_mcq_questions']=self.create_general_mcq_questions
#################################
#General functions
###############################
    def get_methods_list(self):
        response=[{"label":n, "value":json.dumps({ky:"<>" for ky in str(inspect.signature(v)).split(')')[0].split('(')[-1].split(',')})} for n,v in inspect.getmembers(self, inspect.ismethod)]
        #response=[{"label":n, "value":str(inspect.signature(v))} for n,v in inspect.getmembers(self, inspect.ismethod)]
        status='success'
        return {'status':status,'response':response}

    def get_methods_list_without_arguments(self):
        response=[{"label":n, "value":n} for n,v in inspect.getmembers(self, inspect.ismethod)]
        status='success'
        return {'status':status,'response':response}        

    def get_method_signature(self,methodname):
        response=[{"label":n, "value":json.dumps({ky:"<>" for ky in str(inspect.signature(v)).split(')')[0].split('(')[-1].split(',')})} for n,v in inspect.getmembers(self, inspect.ismethod) if n==methodname]
        status='success'
        return {'status':status,'response':response}

    def get_bulk_action_arguments_list(self):
        status='error'
        response=[]
        methods={'add_competencies_to_course':[{"courseid":"int","competencyid":"int"}],
                'add_module_competencies':[{"moduleid":"int","competencyid":"int"}],
                'assign_context_roles':[{'userid':'int', 'roleid':'int', 'contextid':'int'}],
                'assign_module_roles':[{'userid':'int', 'roleid':'int','instanceid':'int', 'contextid':'int','contextlevel':'module'}],
                'create_assignments':[{"courseid":"int", "sectionid":"int", "title":"str", "description":"str","duedate":"28/05/2023 0800","grade":"number"}],
                'create_calendar_events':[{"courseid":"int","name":"str","description":"str","eventtype":"str-user,course,group,category,site","repeats":"int","timestart":"24/12/2023 0800", "timeduration":"int - seconds"}],
                'create_cohorts':[{"cohortype":"str-id","typevalue":"category id - int","cohortname":"str","cohortid":"cohort idnumber-str"}],
                'create_competencies':[{"competencyframeworkid":"int","idnumber":"str","shortname":"str"}],
                'create_competency_frameworks':[{"categoryid":"int","idnumber":"str","shortname":"str", "description":"str"}],
                'create_courses':[{"fullname":"str","shortname":"str", "categoryid":"int","startdate":"24/12/2022 0800","enddate":"24/12/2032 0800"}],
                'create_course_categories_bulk':[{"parent":"int","name":"str","idnumber":"str","description":"str"}],
                'create_course_sections':[{"courseid":"int", "sectionname":"str"}],
                'create_scales':[{"courseid":"int","description":"str","name":"str"}],
                'create_schedules':[{"courseid":"int", "sectionid":"int", "title":"str", "description":"str"}],
                'create_users':[{"username":"str","firstname":"str","lastname":"str","email":"str"}],
                'get_users_modules_grades':[{"userid":"int","moduleid":"int"}],
                'manual_enrol_users_in_courses':[{'courseid':'int', 'userid':'int', 'roleid':'int'}],
                'manual_unenrol_users_in_courses':[{'courseid':'int', 'userid':'int', 'roleid':'int'}],
                'unassign_module_roles':[{'userid':'int', 'roleid':'int','instanceid':'int', 'contextid':'int','contextlevel':"module"}],
                'update_course_module_grades':[{"courseid":"int","moduleid":"int","userid":"int","grade":"float","modname":"str->assign,quiz,.."}],
                'create_hvp_MCQ_quiz':[{"question":"question text","correct":"correct answer","choice1":"answer choice1","choice2":"answer choice2"}],
                'create_hvp_SW_quiz':[{"title":"Title Goes Here", "inputLanguage":"si-LK","question":"The question", "acceptedAnswers":"කුමක් ද, මොකක්ද"}]
                }
        response=[{'label':ky, 'value':json.dumps({ky:methods[ky]})} for ky in [*methods]]
        return {'status':status,'response':response}

    def get_sql_request(self,sqlQ):
        status='error'
        response=[]
        try:
            self.engine.dispose()
            con=self.engine.connect()
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}
    
    def wrapper_fn(self,func): 
        
        def inner1(*x,**a): 
            c=func(*x,**a) 
            return c
                
        return inner1 

    def get_keys(self,dictionary):
        result = []
        for key, value in dictionary.items():
            if type(value) is dict:
                new_keys = self.get_keys(value)
                result.append(key)
                for innerkey in new_keys:
                    result.append(f'{key}/{innerkey}')
            else:
                result.append(key)
        return result

    def insert_records(self,tablename,updatedicts):
        Nds=len(updatedicts)
        status='error'
        response=[]
        self.engine.dispose()
        con=self.engine.connect()
        try:
            db_table_name=tablename
            db_table_PDF=read_sql(sql_text('SELECT * FROM {} WHERE id=(SELECT max(id) FROM {})'.format(db_table_name,db_table_name)), con)
            diffCols=set([*updatedicts[0]]).difference(set([*db_table_PDF]))
            if len(diffCols) == 0:
                lastIndex=db_table_PDF['id'].values[0]
                insert_entry_PDF=DataFrame(columns=[*db_table_PDF],index=[i for i in range(int(lastIndex+1),int(lastIndex+1)+Nds,1)]).drop(columns=['id'])
                insert_entry_PDF.loc[int(lastIndex+1):int(lastIndex)+Nds,[*updatedicts[0]]]=[[dct[ky] for ky in [*dct]] for dct in updatedicts]    
                insert_entry_PDF.to_sql(db_table_name,con,if_exists='append',index=True,index_label='id')
                insertedRecordDicts=insert_entry_PDF.to_dict(orient='records')
                status='Table {} updated successfully'.format(db_table_name)
                #response=status
                recordids=[ii for ii in [i for i in range(int(lastIndex+1),int(lastIndex+1)+Nds,1)]]
                for idct,dct in enumerate(insertedRecordDicts):
                    dct['id']=recordids[idct]
                    response+=[dct]
            else:
               status='Insert columns'+', '.join(diffCols)+' not in table'
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def call_chatgpt_API_davinci(self,functionname,parameters,model="text-davinci-003", temperature=0,max_tokens=2000):
        status='error'
        response=[]

        fn_2_return=self.wrapper_fn(self.chatgpt_methods[functionname])
        content=fn_2_return(**parameters)
        
        response = openai.Completion.create(model=model,
                                            prompt=content,
                                            temperature=temperature,max_tokens=max_tokens)
        responsetext=re.sub("\n","",response.choices[0].text)
        status='success'
        return {'status':status, 'response':responsetext}

    def call_chatgpt_API(self,functionname,parameters,model="gpt-3.5-turbo", temperature=0,max_tokens=2000):
        status='error'
        response=[]

        fn_2_return=self.wrapper_fn(self.chatgpt_methods[functionname])
        messages=fn_2_return(**parameters)
        response = openai.ChatCompletion.create(model=model, messages=messages,temperature=temperature,max_tokens=max_tokens)
        responsetext=response['choices'][0]['message']['content']

        status='success'
        return {'status':status, 'response':responsetext}


    def get_fig_menus(self,numberofmenus,datadicts):
        menus=()
        status='error'
        if len(datadicts)!=0:
            options=[{'label':ky,'value':ky} for ky in datadicts[0]]
            for nn in range(numberofmenus):
                menus+=options,
            status='success'
        else:
            pass
        return {'status':status, 'response':menus}
#######################################
#Moodle webservice call
#######################################
    def rest_api_parameters(self,in_args, prefix='', out_dict=None):
        """Transform dictionary/array structure to a flat dictionary, with key names
        defining the structure.
        Example usage:
        >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
        {'courses[0][id]':1,
        'courses[0][name]':'course1'}
        """
        if out_dict==None:
            out_dict = {}
        if not type(in_args) in (list,dict):
            out_dict[prefix] = in_args
            return out_dict
        if prefix == '':
            prefix = prefix + '{0}'
        else:
            prefix = prefix + '[{0}]'
        if type(in_args)==list:
            for idx, item in enumerate(in_args):
                self.rest_api_parameters(item, prefix.format(idx), out_dict)
        elif type(in_args)==dict:
            for key, item in in_args.items():
                self.rest_api_parameters(item, prefix.format(key), out_dict)
        return out_dict

    def call(self,accessParams, fname, **kwargs):
        """Calls moodle API function with function name fname and keyword arguments.
        Example:
        >>> call_mdl_function('core_course_update_courses',
                            courses = [{'id': 1, 'fullname': 'My favorite course'}])
        """
        parameters = self.rest_api_parameters(kwargs)
        parameters.update({"wstoken": accessParams['KEY'], 'moodlewsrestformat': 'json', "wsfunction": fname})
        response = post(accessParams['URL']+accessParams['ENDPOINT'], parameters,verify=False)
        response = response.json()
        if type(response) == dict and response.get('exception'):
            raise SystemError("Error calling Moodle API\n", response)
        return response

    def call_moodle_webservice(self,wsfunction,parameters):
        '''
        Webserice call: {"wsfunction":<the webservice function name>,"parameters":<kwargs>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        print(parameters)
        try:
            response=self.call(self.mWAP,wsfunction,**parameters)
            status='success'
        except:
            pass

        return {'status':status,'response':response}


#######################################
#Moodle quiz creation
#######################################

    def create_moodle_quiz(self,questionsdict):
        answerdict={'@fraction': '0',
                    '@format': 'html',
                    'text': '<p dir="ltr" style="text-align: left;">Choice<br></p>',
                    'feedback': {'@format': 'html', 'text': 'none'}}
        questionict={'@type': 'multichoice',
                    'name': {'text': 'Quation Name1'},
                    'questiontext': {'@format': 'html','text': '<p dir="ltr" style="text-align: left;"></p><p>Text 1<p></p>'},
                    'generalfeedback': {'@format': 'html', 'text': 'none'},
                    'defaultgrade': '1',
                    'penalty': '0',
                    'hidden': '0',
                    'idnumber': 'none',
                    'single': 'true',
                    'shuffleanswers': 'true',
                    'answernumbering': 'none',
                    'showstandardinstruction': '0',
                    'correctfeedback': {'@format': 'html', 'text': 'Your answer is correct.'},
                    'partiallycorrectfeedback': {'@format': 'html',
                    'text': 'Your answer is partially correct.'},
                    'incorrectfeedback': {'@format': 'html', 'text': 'Your answer is incorrect.'},
                    'shownumcorrect': 'none',
                    'answer': [answerdict]}
        xml_dict={'quiz':{'question':[questionict]}}
        question=[]
        for dct in questionsdict:
            qdct=copy.deepcopy(questionict)
            qdct['name']['text']=dct['name']
            dct.pop('name')
            qdct['defaultgrade']=dct['grade']
            dct.pop('grade')
            qdct['questiontext']['text']= '<p dir="ltr" style="text-align: left;"></p><p>{}<p></p>'.format(dct['question'])
            dct.pop('question')
            answer=[]
            for ky in [*dct]:
                adct=copy.deepcopy(answerdict)
                if dct[ky] not in ['',None]:
                    if ky=='correct':
                        adct['@fraction']='100'
                        adct['text']='<p dir="ltr" style="text-align: left;">{}<br></p>'.format(dct[ky])
                    else:
                        adct['@fraction']='0'
                        adct['text']='<p dir="ltr" style="text-align: left;">{}<br></p>'.format(dct[ky])
                    answer+=[adct]
                    qdct['answer']=answer
            question+=[qdct]
        xml_dict={'quiz':{'question':question}}
        xml_data = xmltodict.unparse(xml_dict, pretty=True)
        response=xml_data
        status='success'
        return {"status":status,"response":response} 

########################################
#ChatGPT
########################################

    def get_general_response(self, **kwargs):
        #prompt="""{}""".format(kwargs['query'])
        messages=[
            {
            "role": "user",
            "content": kwargs['query']
            }
        ]
        return messages

    def create_general_mcq_questions_v0(self, **kwargs):
        #prompt='generate '+str(kwargs['numberofquestions'])+' MCQs with 4 choices  to test the understanding of '+kwargs['topic']+'. Give the response as a list of dictionaries where each of the dictionaries corresponding to each of the questions take the form {"question":"the question","correct":"the correct answer","choice1":"incorrect choice 1","choice2":"incorrect choice 2","choice3":"incorrect choice 3"}'
        messages=[
            {
            "role": "system",
            "content": 'You will be provided with a topic, your task is to generate a list of dictionaries where each dictionary is of the form {"question":"the question","correct":"the correct answer","choice1":"incorrect choice 1","choice2":"incorrect choice 2","choice3":"incorrect choice 3"}. Here each dictionary corresponds to one question of set of '+str(kwargs['numberofquestions'])+' MCQs with 4 choices'
            },
            {
            "role": "user",
            "content": kwargs['topic']
            }
        ]
        return messages

    def create_general_mcq_questions(self, **kwargs):
        exampleResponse="[\n    {\n        \"question\": \"What is the correct form of the verb 'to be' in the present simple tense for the pronoun 'he'?\",\n        \"correct\": \"is\",\n        \"choice1\": \"am\",\n        \"choice2\": \"are\",\n        \"choice3\": \"be\"\n    },\n    {\n        \"question\": \"Which of the following is a coordinating conjunction?\",\n        \"correct\": \"and\",\n        \"choice1\": \"but\",\n        \"choice2\": \"although\",\n        \"choice3\": \"because\"\n    },\n    {\n        \"question\": \"What is the correct way to form the comparative degree of the adjective 'beautiful'?\",\n        \"correct\": \"more beautiful\",\n        \"choice1\": \"beautifuler\",\n        \"choice2\": \"most beautiful\",\n        \"choice3\": \"beautifully\"\n    },\n    {\n        \"question\": \"What is the correct form of the pronoun 'they' in the possessive case?\",\n        \"correct\": \"their\",\n        \"choice1\": \"theirs\",\n        \"choice2\": \"they's\",\n        \"choice3\": \"them's\"\n    }\n]"
        messages=[
                {"role": "system","content": 'You will be provided with a topic by the user, your task is to generate a list of dictionaries where each dictionary is of the form {"question":"the question","correct":"the correct answer","choice1":"incorrect choice 1","choice2":"incorrect choice 2","choice3":"incorrect choice 3"}. Here each dictionary corresponds to one question of set of '+str(kwargs['numberofquestions'])+' MCQs with 4 choices'},
                {"role": "user","content": 'Advanced English grammar'},
                {"role": "assistant","content": exampleResponse},
                {"role": "user","content": kwargs['topic']}
                ]
        return messages        

    def create_language_mcq_questions(self, **kwargs):
        messages=[
            {
            "role": "system",
            "content": 'You will be provided with a topic, your task is to generate a list of dictionaries where each dictionary is of the form {"question":"the question","correct":"the correct answer","choice1":"incorrect choice 1","choice2":"incorrect choice 2","choice3":"incorrect choice 3"}. Here each dictionary corresponds to one question of set of '+str(kwargs['numberofquestions'])+' MCQs with 4 choices'
            },
            {
            "role": "user",
            "content": kwargs['language']+' grammar'
            }
        ]
        return messages

#######################################################
#Graph-Q
#######################################################
    def epsilon_greedy_policy(self,sNow):
        epsilon=self.parameters['epsilon']
        #epsilon-greedy
        q_values_now=copy.deepcopy(self.q_values[sNow])
        #if a randomly chosen value between 0 and 1 is less than epsilon,
        #then choose the most promising value from the Q-table for this state.
        if np.random.random() < epsilon:
            return [*q_values_now][np.argmax([q_values_now[xx] for xx in q_values_now])]
        else: #choose a random action
            return [*q_values_now][np.random.randint(len([*q_values_now]))]

    def update_step(self, sOld):
        chosenAction = self.epsilon_greedy_policy(sOld) #get_next_action(G, sNow, epsilon,q_values0)
        #receive the reward for taking the action
        reward = self.rewardFunction(self.G,sOld,chosenAction,self.parameters)
        #transition to the next state (i.e., move to the next location)
        q_values_old=self.q_values[sOld]
        old_q_value = q_values_old[chosenAction]
        #receive the reward for moving to the new state, and calculate the temporal difference
        sNow=self.stateTransitionFunction(self.G,sOld,chosenAction,self.parameters)
        if sNow not in self.endStates:
            q_values_now=self.q_values[sNow]
            temporal_difference = reward + (self.discountFactor * np.max([q_values_now[xx] for xx in q_values_now])) - old_q_value
            #update the Q-value for the previous state and action pair
            new_q_value = old_q_value + (self.learningRate * temporal_difference)
            self.q_values[sOld][chosenAction] = new_q_value

        return sNow

    def q_training(self,trainingSteps):
        for episode in range(trainingSteps):
            sOld=list(self.G.nodes())[0]
            while sOld not in self.endStates:
                sOld=self.update_step(sOld)
        return self.q_values

    def get_optimal_path(self,sNow,sEnd):
        #return immediately if this is an invalid starting location
        if sNow in self.endStates:
            return []
        else: #if this is a 'legal' starting location
            current_s = sNow
            optimal_path = []
            optimal_path.append(current_s)
            #continue moving along the path until we reach the goal (i.e., the item packaging location)
            while sNow not in self.endStates:
                #get the best action to take
                action_chosen = self.epsilon_greedy_policy(current_s)
                reward = self.rewardFunction(self.G,current_s,action_chosen,self.parameters)
                #move to the next location on the path, and add the new location to the list
                current_s = self.stateTransitionFunction(self.G,current_s,action_chosen,self.parameters)  #state_transition(G,sNow,action_index,stateFnParams) #list(G.neighbors(sNow))[action_index]
                optimal_path.append(current_s)
                sNow=current_s
            #print(optimal_path)
            return optimal_path

    def path_reward(self,path):
        pathReward=0
        for isx,s in enumerate(path[:-1]):
            pathReward+=self.rewardFunction(self.G,s,(s,path[isx+1]),self.parameters)
        return pathReward


########################################################
#Working
########################################################
    def get_course_modules_list(self,courseid):
        #Don't delete
        response=[]
        status="error"
        courseSecnModulesDicts=self.get_course_modules(courseid)['response']
        coursemodules=[]
        for secn in courseSecnModulesDicts:
            for mod in secn['sectionmodules']:
                mod['sectionid']=secn['sectionid']
                mod['sectionname']=secn['sectionname']
                coursemodules+=[mod]
        response=coursemodules
        status='success'
        return {'status':status,'response':response}

#########################################################
#Bulk action functions
#########################################################

    def create_courses_in_category(self,categoryid, datadicts):
        '''
        {"fullname":"str","shortname":"str","startdate":"24/12/2023 0800","enddate":"24/12/2023 0800"}
        fullname, shortname, required
        '''
        status='error'
        response=[]
        categorydatadicts=[]
        for dct in datadicts:
            dct['categoryid']=categoryid
            categorydatadicts+=[dct]
        response=self.create_courses(categorydatadicts)['response']
        status='success'
        return {'status':status,'response':response}

##########################################################
#Create update competencies
##########################################################
    def get_competency_frameworks_list(self):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            sqlQ="SELECT id, shortname  FROM mdl_competency_framework"
            competencyFrameworks=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            response=[{'label':dct['shortname'],'value':dct['id']} for dct in competencyFrameworks]
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response} 

    def create_scales(self,datadicts):
        status='error'
        response=[]
        updatedict={'courseid':0,
                    'description':'',
                    'descriptionformat':0,
                    'name':'',
                    'scale':'',
                    'timemodified':round(time.time()),
                    'userid':2}
        #response=datadicts
        self.engine.dispose()
        con=self.engine.connect()
        updateDicts=[]  
        try:    
            for dct in datadicts:
                tempdict=copy.deepcopy(updatedict)
                for ky in [*dct]:
                    tempdict[ky]=dct[ky]
                updateDicts+=[tempdict]
            response=updateDicts
            response=self.insert_records("mdl_scale",updateDicts)['response']
            status='scale created'
        except:
            pass
        con.close()
        return {'status':status,'response':response} 

    def create_competency_frameworks(self,datadicts):
        '''
        datadicts=[{'categoryid':'int','idnumber':'str','shortname':'str', 'description':str}]
        '''
        status='error'
        response=[]
        contextlevel=40
        updatedict={'contextid': 1,
                    'description': '',
                    'descriptionformat': 1,
                    'idnumber': 'XYZ001',
                    'scaleconfiguration': json.dumps([{"scaleid":"2"},{"id":1,"scaledefault":1,"proficient":0},{"id":2,"scaledefault":0,"proficient":1}]),
                    'scaleid': 2,
                    'shortname': 'shortname',
                    'taxonomies': 'competency,competency,competency,competency',
                    'timecreated': round(time.time()),
                    'timemodified': round(time.time()),
                    'usermodified': 2,
                    'visible': 1}
        self.engine.dispose()
        con=self.engine.connect()
        #updateDicts=[]
        fname='core_competency_create_competency_framework'        
        try:    
            for inn,dct in enumerate(datadicts):
                tempdict={}
                sqlQ="SELECT id FROM mdl_context WHERE contextlevel = {} AND instanceid = {}".format(contextlevel,dct['categoryid'])
                contextid=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0]["id"]
                tempdict=copy.deepcopy(updatedict)
                tempdict['contextid']=contextid
                tempdict['idnumber']=dct['idnumber']
                tempdict['shortname']=dct['shortname']
                tempdict['description']=dct['description']     
                #updateDicts+=[tempdict]
                kwargs={"competencyframework":tempdict}
                response+=[self.call(self.mWAP, fname, **kwargs)]
            #response=self.insert_records("mdl_competency_framework",updateDicts)['response']
            status='competency framework created'
        except:
            pass
        con.close()
        return {'status':status,'response':response}    
    
    def create_competencies(self,datadicts):
        '''
        datadicts=[{'competencyframeworkid':'int','idnumber':'str','shortname':'str','description':'str'}]
        '''
        response=[]
        updatedict={'competencyframeworkid': 1,
                    'description': '',
                    'descriptionformat': 1,
                    'idnumber': 'idnumber',
                    'parentid': 0,
                    'path': '/0/',
                    'ruleconfig': None,
                    'ruleoutcome': 0,
                    'ruletype': None,
                    'scaleconfiguration': None,
                    'scaleid': None,
                    'shortname': 'shortname',
                    'sortorder': 0,
                    'timecreated': round(time.time()),
                    'timemodified': round(time.time()),
                    'usermodified': 2}

        # self.engine.dispose()
        # con=self.engine.connect()
        # sqlQ="SELECT sortorder FROM mdl_competency WHERE parentid=0"
        # maxsortorder=max(read_sql(sql_text(sqlQ),con)['sortorder'].to_list())
        fname='core_competency_create_competency'
        updateDicts=[]
        for inn,dct in enumerate(datadicts):
            tempdict=copy.deepcopy(updatedict)
            for ky in [*dct]:
                tempdict[ky]=dct[ky]
            kwargs={"competency":tempdict}
            response+=[self.call(self.mWAP, fname, **kwargs)]
            #tempdict['sortorder']=maxsortorder+1+inn      
            updateDicts+=[tempdict]
        #response=self.insert_records("mdl_competency",updateDicts)['response']
        status='competencies created'
        #con.close()
        return {'status':status,'response':response}

    def add_module_competencies(self,datadicts):
        '''
        datadicts=[{'moduleid':int,'competencyid':int}]
        '''
        updatedict={'cmid': 0,
                    'competencyid': 1,
                    'ruleoutcome': 0,
                    'sortorder': 0,
                    'timecreated': round(time.time()),
                    'timemodified': round(time.time()),
                    'usermodified': 2}

        self.engine.dispose()
        con=self.engine.connect()
        sqlQ="SELECT sortorder FROM mdl_competency_modulecomp"
        maxsortorder=max(read_sql(sql_text(sqlQ),con)['sortorder'].to_list())
        
        updateDicts=[]
        for inn,dct in enumerate(datadicts):
            tempdict=copy.deepcopy(updatedict)
            tempdict['cmid']=dct['moduleid']
            tempdict['competencyid']=dct['competencyid']
            tempdict['sortorder']=maxsortorder+1+inn      
            updateDicts+=[tempdict]
        response=updateDicts
        response=self.insert_records("mdl_competency_modulecomp",updateDicts)['response']
        status='competency created'
        con.close()
        #response=sqlQ #maxsortorder
        return {'status':status,'response':response}        

    def add_competencies_to_course(self,datadicts):
        '''
        datadicts=[{"courseid":int,"competencyid":int}]
        '''
        response=[]
        status='error'
        wsfunction="core_competency_add_competency_to_course"
        for dct in datadicts:
            response+=[self.call(self.mWAP,wsfunction,**dct)]
        status='success'

        return {'status':status,'response':response}

    def get_modules_competencies(self,moduleids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            sqlQ="SELECT mmcom.cmid AS moduleid, mcom.id, mcom.idnumber, mcom.description, mcom.shortname AS name, mcomf.idnumber AS framework_idnumber, mcomf.id AS frameworkid  FROM mdl_competency_modulecomp mmcom INNER JOIN mdl_competency mcom ON mcom.id=mmcom.competencyid INNER JOIN mdl_competency_framework mcomf ON mcomf.id=mcom.competencyframeworkid WHERE mmcom.cmid IN {}".format(tuple(moduleids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response}

    def get_modules_by_competencies(self,competencyids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            sqlQ="SELECT mmcom.cmid AS moduleid, mcom.id AS competencyid, mcom.idnumber, mcom.description, mcom.shortname AS name, mcomf.idnumber AS framework_idnumber, mcomf.id AS frameworkid  FROM mdl_competency_modulecomp mmcom INNER JOIN mdl_competency mcom ON mcom.id=mmcom.competencyid INNER JOIN mdl_competency_framework mcomf ON mcomf.id=mcom.competencyframeworkid WHERE mmcom.competencyid IN {}".format(tuple(competencyids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response}

    def get_courses_by_competencies(self,competencyids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            sqlQ="SELECT mccom.courseid, mcom.id AS competencyid, mcom.idnumber, mcom.description, mcom.shortname AS name, mcomf.idnumber AS framework_idnumber, mcomf.id AS frameworkid  FROM mdl_competency_coursecomp mccom INNER JOIN mdl_competency mcom ON mcom.id=mccom.competencyid INNER JOIN mdl_competency_framework mcomf ON mcomf.id=mcom.competencyframeworkid WHERE mccom.competencyid IN {}".format(tuple(competencyids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response}

    def get_competencies_by_frameworkids(self,frameworkids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            sqlQ="SELECT mcom.*, mcomf.idnumber AS framework_idnumber, mcomf.id AS frameworkid  FROM mdl_competency mcom INNER JOIN mdl_competency_framework mcomf ON mcomf.id=mcom.competencyframeworkid WHERE mcomf.id IN {}".format(tuple(frameworkids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response}

    def get_competencies_by_frameworkid_list(self,frameworkid):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            sqlQ="SELECT mcom.id, mcom.shortname  FROM mdl_competency mcom WHERE mcom.competencyframeworkid={}".format(frameworkid)            
            competencyDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            response=[{'label':dct['shortname'],'value':dct['id']} for dct in competencyDicts]
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response}        

    def get_competency_frameworks(self):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            sqlQ="SELECT *  FROM mdl_competency_framework"
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response} 

    def get_users_module_competencies(self,modname,rolename,userids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            colnames=['userid','firstname','competency','competencydescription','competencyidnumber','finalgrade','grade','coursename','name','intro','allowsubmissionsfromdate','duedate','cutoffdate','gradingduedate','id','moduleid','course','sectionid','competencyframeworkid','competencyid']
            sqlQ="SELECT mmcom.*, mcom.competencyframeworkid, mcom.id AS competencyid, mcom.shortname AS competency, mcom.idnumber AS competencyidnumber, mcom.description AS competencydescription, mcm.id AS moduleid, mcm.section AS sectionid, mh.*, mgg.finalgrade, mgg.userid, mu.firstname, mc.shortname AS coursename FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_grade_items mgi ON mh.id=mgi.iteminstance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id INNER JOIN mdl_role_assignments ra ON ra.contextid = mctx.id INNER JOIN mdl_role r ON r.id = ra.roleid INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_course mc ON mc.id=mh.course INNER JOIN mdl_competency_modulecomp mmcom ON mcm.id=mmcom.cmid INNER JOIN mdl_competency mcom ON mcom.id=mmcom.competencyid WHERE mcm.deletioninprogress=0 AND mm.name='{}' AND mctx.contextlevel={} AND mgg.userid=ra.userid AND ra.userid IN {} AND mgg.aggregationstatus='used' AND r.shortname='{}'".format(modname,modname,70,tuple(userids+[0]),rolename)
            responsePDF=read_sql(sql_text(sqlQ),con)[colnames]
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grade']
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response}

    def get_modules_users_information_by_competencies(self,competencyids,contextlevel=70,rolename='student',modname='assign'):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            colnames=['userid','firstname','competency','competencydescription','competencyidnumber','finalgrade','grade','coursename','name','intro','allowsubmissionsfromdate','duedate','cutoffdate','gradingduedate','id','moduleid','course','sectionid','competencyframeworkid','competencyid']
            #Dont delete this gives automatic module selection
            #sqlQ="SELECT mcom.id AS competencyid, mcom.shortname AS competency, mcom.idnumber AS competencyidnumber, mcom.competencyframeworkid, mcom.description AS competencydescription, mcm.id AS moduleid, mcm.section AS sectionid, mh.*, mgg.finalgrade, mgg.userid, mc.shortname AS coursename, mu.firstname FROM mdl_competency mcom INNER JOIN mdl_competency_modulecomp mmcom ON mcom.id=mmcom.competencyid INNER JOIN mdl_course_modules mcm ON mcm.id=mmcom.cmid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_grade_items mgi ON mh.id=mgi.iteminstance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_course mc ON mc.id=mh.course WHERE mmcom.competencyid IN {} AND mcm.deletioninprogress=0 AND mm.name='{}' AND mgg.aggregationstatus='used'".format(modname,tuple(competencyids+[0]),modname)
            sqlQ="SELECT mcom.id AS competencyid, mcom.shortname AS competency, mcom.idnumber AS competencyidnumber, mcom.competencyframeworkid, mcom.description AS competencydescription, mcm.id AS moduleid, mcm.section AS sectionid, mh.*, mgg.finalgrade, mgg.userid, mu.firstname, mc.shortname AS coursename FROM mdl_competency mcom INNER JOIN mdl_competency_modulecomp mmcom ON mcom.id=mmcom.competencyid INNER JOIN mdl_course_modules mcm ON mcm.id=mmcom.cmid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_grade_items mgi ON mh.id=mgi.iteminstance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id INNER JOIN mdl_role_assignments ra ON ra.contextid = mctx.id INNER JOIN mdl_role r ON r.id = ra.roleid INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_course mc ON mc.id=mh.course WHERE mmcom.competencyid IN {} AND mcm.deletioninprogress=0 AND mm.name='{}' AND mctx.contextlevel={} AND mgg.userid=ra.userid AND mgg.aggregationstatus='used' AND r.shortname='{}'".format(modname,tuple(competencyids+[0]),modname,contextlevel,rolename)
            
            responsePDF=read_sql(sql_text(sqlQ),con)[colnames]
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grade']
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response} 

    def get_assignment_users_information_by_competencies(self,rolename,competencyids):
        modname='assign'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try: 
            #sqlQ="SELECT mcom.id AS competencyid, mcom.shortname AS competency, mcom.idnumber AS competencyidnumber, mcom.competencyframeworkid, mcom.description AS competencydescription, mcm.id AS moduleid, mcm.section AS sectionid, mh.*, mgg.finalgrade, mgg.userid FROM mdl_grade_grades mgg INNER JOIN mdl_grade_items mgi ON mgi.id=mgg.itemid INNER JOIN mdl_{} mh ON mh.id=mgi.iteminstance INNER JOIN mdl_course_modules mcm ON mcm.instance=mh.id INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_competency_modulecomp mmcom ON mmcom.cmid=mcm.id INNER JOIN mdl_competency mcom ON mcom.id=mmcom.competencyid WHERE mgi.itemmodule='{}' AND mm.name='{}' AND mmcom.competencyid IN {}".format(modname,modname,modname,tuple(competencyids+[0]))
            #sqlQ="SELECT mcom.id AS competencyid, mcom.shortname AS competency, mcom.idnumber AS competencyidnumber, mcom.competencyframeworkid, mcom.description AS competencydescription, mcm.id AS moduleid, mcm.section AS sectionid, mh.*, mgg.finalgrade, mgg.userid FROM mdl_competency mcom INNER JOIN mdl_competency_modulecomp mmcom ON mcom.id=mmcom.competencyid INNER JOIN mdl_course_modules mcm ON mcm.id=mmcom.cmid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_grade_items mgi ON mh.id=mgi.iteminstance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id INNER JOIN mdl_role_assignments ra ON ra.contextid = mctx.id INNER JOIN mdl_role r ON r.id = ra.roleid WHERE mmcom.competencyid IN {} AND mm.name='{}' AND mctx.contextlevel={} AND r.shortname='{}'".format(modname,tuple(competencyids+[0]),modname,70,rolename)
            colnames=['userid','firstname','competency','competencydescription','competencyidnumber','finalgrade','grade','coursename','name','intro','allowsubmissionsfromdate','duedate','cutoffdate','gradingduedate','id','moduleid','course','sectionid','competencyframeworkid','competencyid']
            sqlQ="SELECT mcom.id AS competencyid, mcom.shortname AS competency, mcom.idnumber AS competencyidnumber, mcom.competencyframeworkid, mcom.description AS competencydescription, mcm.id AS moduleid, mcm.section AS sectionid, mh.*, mgg.grade AS finalgrade, mgg.userid, mu.firstname, mc.shortname AS coursename FROM mdl_competency mcom INNER JOIN mdl_competency_modulecomp mmcom ON mcom.id=mmcom.competencyid INNER JOIN mdl_course_modules mcm ON mcm.id=mmcom.cmid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_assign_grades mgg ON mh.id=mgg.assignment INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id INNER JOIN mdl_role_assignments ra ON ra.contextid = mctx.id INNER JOIN mdl_role r ON r.id = ra.roleid INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_course mc ON mc.id=mh.course WHERE mmcom.competencyid IN {} AND mcm.deletioninprogress=0 AND mm.name='{}' AND mctx.contextlevel={} AND mgg.userid=ra.userid AND r.shortname='{}'".format(modname,tuple(competencyids+[0]),modname,70,rolename)
            response=read_sql(sql_text(sqlQ),con)[colnames].to_dict(orient='records')
        except:
            pass
        status="success"
        con.close()
        return {"status":status,"response":response} 

##########################################################
#Create/Update Modules
##########################################################
    def hvp_function_call(self,functionName,*fnVaraibles,**functionParameters):
        '''functionParameters is a dictionary of the parameters to be passed to the function'''   
        function_to_be_called = self.wrapper_fn(functionName)  
        return function_to_be_called(*fnVaraibles,**functionParameters)

    def get_hvp_content_json(self,moduleid):
        '''
        Webserice call: {"moduleid":<moduleid>}
        Response: {'status':status,'response':response}
        '''    
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQm="SELECT mh.json_content FROM mdl_hvp mh INNER JOIN mdl_course_modules mcm ON mh.id=mcm.instance WHERE mcm.id={}".format(moduleid)
            print(sqlQm)
            response=read_sql(sql_text(sqlQm),con)['json_content'].to_list()[0]
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response} 

    def create_assignments(self,datadicts):
        '''datadicts -> list of
        {"courseid":<courseid>, "sectionid":<sectionid>, "title":<title>, "description":<description>, 
        "allowsubmissionsfromdate":0,"duedate":0,"cutoffdate"=0, "gradingduedate":0, "grade":100}
        '''
        modulename='assign'
        response=[]
        status='error'
        try:
            timeCols={"allowsubmissionsfromdate","duedate", "cutoffdate", "gradingduedate", "completionexpected"}
            temp=[]
            for dct in datadicts:
                cols2change=list(set([*dct]).intersection(timeCols))
                if len(cols2change)!=0:
                    for zz in cols2change:
                        try:
                            dct[zz]=int(time.mktime(to_datetime(dct[zz], errors='ignore', dayfirst=True).to_pydatetime().timetuple()))
                        except:
                            dct.pop(zz)
                temp+=[dct]
            datadicts=copy.deepcopy(temp)
            optionkeys=[dct['name'] for dct in self.get_assign_options(**{})]
            #dataPDF=DataFrame(datadicts)
            courseids=list(set([dct['courseid'] for dct in datadicts]))
            courseids.sort()
            fname="local_tealmodmanage_add_modules"
            self.engine.dispose()
            con=self.engine.connect()
            for courseid in courseids:
                modules=[]
                options=[]
                #courseDataDicts=dataPDF[dataPDF['courseid']==courseid].to_dict(orient='records')
                courseDataDicts=[dct for dct in datadicts if dct['courseid']==courseid]
                for dct in courseDataDicts:
                    sqlQs="SELECT section FROM mdl_course_sections WHERE id={}".format(dct['sectionid'])
                    section=read_sql(sql_text(sqlQs),con)['section'].to_list()[0]
                    #optionsDict={"allowsubmissionsfromdate":dct['allowsubmissionsfromdate'], "duedate":dct['duedate'], "cutoffdate":dct['cutoffdate'], "gradingduedate":dct['gradingduedate'], "completionexpected":dct['duedate']}
                    optionsDict={ky:dct[ky] for ky in optionkeys if ky in [*dct]}
                    options=self.get_assign_options(**optionsDict)
                    options=[{"name":"display","value":1}]+options
                    modules+=[{"modulename":modulename,"section":section,"name":dct['title'],"description":dct['description'],"descriptionformat":1,"visible":1,"options":options}]
                kwargs={"courseid":courseid,"modules":modules}
                response+=self.call(self.mWAP, fname, **kwargs)
            status="success"
        except:
           pass 
        con.close()                        
        return {"status":status,"response":response}

    def create_schedules(self,datadicts):
        '''datadicts -> list of
        {"courseid":<courseid>, "sectionid":<sectionid>, "title":<title>, "description":<description>}
        '''
        modulename='scheduler'
        response=[]
        status='error'
        try:
            optionkeys=[dct['name'] for dct in self.get_scheduler_options(**{})]
            #dataPDF=DataFrame(datadicts)
            courseids=list(set([dct['courseid'] for dct in datadicts]))
            courseids.sort()
            fname="local_tealmodmanage_add_modules"
            self.engine.dispose()
            con=self.engine.connect()
            for courseid in courseids:
                modules=[]
                options=[]
                #courseDataDicts=dataPDF[dataPDF['courseid']==courseid].to_dict(orient='records')
                courseDataDicts=[dct for dct in datadicts if dct['courseid']==courseid]
                for dct in courseDataDicts:
                    sqlQs="SELECT section FROM mdl_course_sections WHERE id={}".format(dct['sectionid'])
                    section=read_sql(sql_text(sqlQs),con)['section'].to_list()[0]
                    #optionsDict={"allowsubmissionsfromdate":dct['allowsubmissionsfromdate'], "duedate":dct['duedate'], "cutoffdate":dct['cutoffdate'], "gradingduedate":dct['gradingduedate'], "completionexpected":dct['duedate']}
                    optionsDict={ky:dct[ky] for ky in optionkeys if ky in [*dct]}
                    options=self.get_scheduler_options(**optionsDict)
                    options=[{"name":"display","value":1}]+options
                    modules+=[{"modulename":modulename,"section":section,"name":dct['title'],"description":dct['description'],"descriptionformat":1,"visible":1,"options":options}]
                kwargs={"courseid":courseid,"modules":modules}
                response+=self.call(self.mWAP, fname, **kwargs)
            status="success"
        except:
           pass 
        con.close()                        
        return {"status":status,"response":response}        

    def create_assignments_in_course_section(self,courseid,sectionid,datadicts):
        response=[]
        status="error"
        assignmentsdatadicts=[]
        for dct in datadicts:
            dct['courseid']=courseid
            dct['sectionid']=sectionid
            assignmentsdatadicts+=[dct]
        response=self.create_assignments(assignmentsdatadicts)['response']  
        return {'status':status,'response':response}

    def create_schedules_in_course_section(self,courseid,sectionid,datadicts):
        response=[]
        status="error"
        assignmentsdatadicts=[]
        for dct in datadicts:
            dct['courseid']=courseid
            dct['sectionid']=sectionid
            assignmentsdatadicts+=[dct]
        response=self.create_schedules(assignmentsdatadicts)['response']  
        return {'status':status,'response':response}        

    def create_hvp_MCQ_quiz(self,templatemoduleid,courseid,sectionid,title,questionsdict):
        response=[]
        status='error'
        templateModuleid=templatemoduleid
        hvpmethod="update_hvp_MCQ_questions"
        questions=[]
        for dct in questionsdict:
            questions+=[{'question':dct.pop('question'), 'answers':[{"text":dct.pop('correct'),'correct':1}]+[{'text':dct[ky],'correct':0} for ky in [*dct] if dct[ky] not in ['',None]]}]

        hvpparameters={"questions":questions}
        try:
            response=self.create_hvp_module(courseid,sectionid,templateModuleid,title,hvpmethod=hvpmethod,hvpparameters=hvpparameters)['response']
        except:
           pass                       
        return {"status":status,"response":response}

    def ai_generated_language_hvp_MCQ_quiz(self,numberofquestions,language,templatemoduleid,courseid,sectionid,title):
        response=[]
        status='error'
        functionname='create_language_mcq_questions'
        parameters={"numberofquestions":numberofquestions,"language":language}
        try:
            questionsdict=json.loads(self.call_chatgpt_API(functionname,parameters,model="gpt-3.5-turbo", temperature=1.0,max_tokens=2000)['response'])
            response=self.create_hvp_MCQ_quiz(templatemoduleid,courseid,sectionid,title,questionsdict)['response']
            #response=questionsdict
            status='success'
        except:
            pass
        return {"status":status,"response":response}        

    def ai_generated_general_hvp_MCQ_quiz(self,numberofquestions,topic,templatemoduleid,courseid,sectionid,title):
        response=[]
        status='error'
        functionname='create_general_mcq_questions'
        parameters={"numberofquestions":numberofquestions,"topic":topic}
        try:
            questionsdict=json.loads(self.call_chatgpt_API(functionname,parameters,model="gpt-3.5-turbo", temperature=1.0,max_tokens=2000)['response'])
            response=self.create_hvp_MCQ_quiz(templatemoduleid,courseid,sectionid,title,questionsdict)['response']
            #response=questionsdict
            status='success'
        except:
            pass
        return {"status":status,"response":response}        

    def ai_generated_general_MCQ_quiz(self,numberofquestions,topic):
        response=[]
        status='error'
        functionname='create_general_mcq_questions'
        parameters={"numberofquestions":numberofquestions,"topic":topic}
        try:
            questionsdict=json.loads(self.call_chatgpt_API(functionname,parameters,model="gpt-3.5-turbo", temperature=1.0,max_tokens=2000)['response'])
            tmp=[dct.update({'name':'Q#{}'.format(ix+1), 'grade':10}) for ix,dct in enumerate(questionsdict)]
            response=questionsdict
            status='success'
        except:
            pass
        return {"status":status,"response":response} 

    def create_hvp_SW_quiz(self,templatemoduleid,courseid,sectionid,title,questionsdict):
        #{"title":"Title Goes Here", "inputLanguage":"si-LK","question":"The question", "acceptedAnswers":"කුමක් ද, මොකක්ද"}
            
        response=[]
        status='error'
        templateModuleid=templatemoduleid
        hvpmethod="update_hvp_SW"
        questions=[]
        for dct in questionsdict:
            dct["acceptedAnswers"]=dct["acceptedAnswers"].split(',')
            questions+=[dct]
        hvpparameters={"questions":questions}
        try:
            response=self.create_hvp_module(courseid,sectionid,templateModuleid,title,hvpmethod=hvpmethod,hvpparameters=hvpparameters)['response']
        except:
           pass                       
        return {"status":status,"response":response}

    def get_users_assignments_by_roles_by_cutoffdate(self,roleids,userids,startTime,endTime):
        status='error'
        response=[]
        modname='assign'
        startTimeUnix=int(time.mktime(to_datetime(startTime, dayfirst=True).to_pydatetime().timetuple()))
        endTimeUnix=int(time.mktime(to_datetime(endTime, dayfirst=True).to_pydatetime().timetuple()))
 
        colnames=['userid','firstname','rolename','name','intro','grade','coursename','allowsubmissionsfromdate','cutoffdate','duedate','gradingduedate','course','moduleid','id','contextid']
        courseModulesPDF=DataFrame(self.get_users_modules_by_type_by_role_ids(modname,userids,roleids)['response'])
        response=courseModulesPDF[((courseModulesPDF['cutoffdate']>startTimeUnix) & (courseModulesPDF['cutoffdate']<endTimeUnix))][colnames].to_dict(orient='records')
        
        status='success'
        return {"status":status,"response":response}

    def create_course_module(self,modulename,courseid,sectionid,title,description="",templateModuleid=None,visible=1,optionsDict=None):
        response=[]
        status='error'
        if optionsDict==None:
            optionsDict={}

        if modulename=="questionnaire":
            options=self.get_questionnaire_options(**optionsDict)
        elif modulename=="assign":
            options=self.get_assign_options(**optionsDict)
        elif modulename=="forum":
            options=self.get_forum_options(**optionsDict)
        elif modulename=="schedulerr":
            options=self.get_scheduler_options(**optionsDict)
        elif modulename=="resource":
            options=self.get_resource_options(**optionsDict)
        elif modulename=="hvp":
            options=self.get_hvp_options(templateModuleid,**optionsDict)
        else:
            options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]
        
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQs="SELECT section FROM mdl_course_sections WHERE id={}".format(sectionid)
            section=read_sql(sql_text(sqlQs),con)['section'].to_list()[0]
            
            #options=[{"name":"display", "value":1},{"name":"h5paction","value":"create"},{"name":"h5plibrary","value":libraryid},{"name":"params","value":json_content}]
            options=[{"name":"display","value":1}]+options
            fname="local_tealmodmanage_add_modules"
            modules=[{"modulename":modulename,"section":section,"name":title,"description":description,"descriptionformat":1,"visible":visible,"options":options}]
            kwargs={"courseid":courseid,"modules":modules}
            response=kwargs
            response=self.call(self.mWAP, fname, **kwargs)
            status="success"
        except:
           pass 
        con.close()                        
        return {"status":status,"response":response}

    def update_course_module(self,courseid,sectionid,moduleid,title=None,description=None,visible=1,optionsDict=None):
        response=[]
        status='error'
        modulename=self.get_course_module_by_id(moduleid)['response'][0]['modname']
        self.engine.dispose()
        con=self.engine.connect()
        sqlQs="SELECT section FROM mdl_course_sections WHERE id={}".format(sectionid)
        section=read_sql(sql_text(sqlQs),con)['section'].to_list()[0]
        sqlQt="SELECT mh.name, mh.intro FROM mdl_{} mh INNER JOIN mdl_course_modules mcm ON mcm.instance=mh.id WHERE mcm.id={}".format(modulename,moduleid)
        modInfo=read_sql(sql_text(sqlQt),con)
        con.close()

        if optionsDict is None:
            optionsDict={}
        if title is None:
            title=modInfo['name'].to_list()[0]
        if description is None:
            description=modInfo['intro'].to_list()[0]    

        if modulename=="questionnaire":
            options=self.get_questionnaire_options(**optionsDict)
        elif modulename=="assign":
            options=self.get_assign_options(**optionsDict)
        elif modulename=="forum":
            options=self.get_forum_options(**optionsDict)
        elif modulename=="scheduler":
            options=self.get_scheduler_options(**optionsDict)
        elif modulename=="resource":
            options=self.get_resource_options(**optionsDict)
        elif modulename=="hvp":
            options=self.get_hvp_options(templateModuleid,**optionsDict)
        else:
            options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]
        response=options
        fname="local_tealmodmanage_update_modules"
        #options=[{"name":"coursemodule","value":moduleid},{"name":"display","value":1}]+[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]
        options=[{"name":"coursemodule","value":moduleid},{"name":"display","value":1}]+options
        modules=[{"modulename":modulename,"section":section,"name":title,"description":description,"descriptionformat":1,"visible":visible,"options":options}]
        kwargs={"courseid":courseid,"modules":modules}
        response=kwargs
        response=self.call(self.mWAP, fname, **kwargs)                         
        return {"status":status,"response":response}

    def get_questionnaire_options(self,showdescription=0,opendate=0,closedate=0,qtype=0,cannotchangerespondenttype=0,respondenttype="fullname",
                                resp_view=1,notifications=0,resume=0,navigate=0,autonum=3,progressbar=0,grade=0,
                                completionunlocked=1,completion=2,completionview=0,completionpass=0,completionexpected=0,completionsubmit=1):
        optionsDict={"showdescription":showdescription,
                "opendate":opendate,
                "closedate":closedate,
                "qtype":qtype,
                "cannotchangerespondenttype":cannotchangerespondenttype,
                "respondenttype":respondenttype,
                "resp_view":resp_view,
                "notifications":notifications,
                "resume":resume,
                "navigate":navigate,
                "autonum":autonum,
                "progressbar":progressbar,
                "grade": grade,
                "create":"new-0",
                "completionunlocked":completionunlocked,
                "completion":completion,"completionview":completionview,"completionpass":completionpass,
                "completionsubmit":completionsubmit,"completionexpected":completionexpected
                }
        options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]
        return options

    def get_forum_options(self,showdescription=0,type="general", duedate=0, cutoffdate=0, maxbytes=512000, 
                        maxattachments=9, displaywordcount=0, forcesubscribe=0, trackingtype=1, 
                        lockdiscussionafter=0, blockperiod=0, blockafter=0, warnafter=0, grade_forum=0, 
                        assessed=0, scale=100, gradepass=0,
                        completionpostsenabled=1,completionposts=1,completiondiscussions=0,completionreplies=0,
                        completionunlocked=1,completion=2,completionview=1,completionpass=0,completionexpected=0):
        optionsDict={"showdescription":showdescription,"type":type, "duedate":duedate, "cutoffdate":cutoffdate, "maxbytes":maxbytes, 
                        "maxattachments":maxattachments, "displaywordcount":displaywordcount, 
                        "forcesubscribe":forcesubscribe, "trackingtype":trackingtype, 
                        "lockdiscussionafter":lockdiscussionafter, "blockperiod":blockperiod, 
                        "blockafter":blockafter, "warnafter":warnafter, "grade_forum":grade_forum, 
                        "assessed":assessed, "scale":scale, "gradepass":gradepass,
                        "completionunlocked":completionunlocked,"completion":completion,"completionview":completionview,
                        "completionpostsenabled":completionpostsenabled, "completionposts":completionposts,"completiondiscussions":completiondiscussions,"completionreplies":completionreplies,
                        "completionpass":completionpass,"completionexpected":completionexpected}
        options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]
        return options

    def get_assign_options(self,showdescription=1,allowsubmissionsfromdate=0, duedate=0, cutoffdate=0, gradingduedate=0, 
                        assignsubmission_onlinetext_enabled=1, assignsubmission_file_enabled=1, 
                        assignsubmission_comments_enabled=1, assignsubmission_file_maxfiles=20, 
                        assignsubmission_file_maxsizebytes=0, assignfeedback_comments_enabled=1, 
                        assignfeedback_editpdf_enabled=1, assignfeedback_comments_commentinline=0, submissiondrafts=0, 
                        requiresubmissionstatement=0, maxattempts=-1, teamsubmission=0, 
                        preventsubmissionnotingroup=0, requireallteammemberssubmit=0, 
                        teamsubmissiongroupingid=0, sendnotifications=0, sendlatenotifications=0, 
                        sendstudentnotifications=1, grade=100, gradecat=5, 
                        gradepass=0, blindmarking=0, hidegrader=0, markingworkflow=0,
                        completionunlocked=1,completion=2,completionview=1,completionsubmit=1,completionusegrade=0,completionpass=0,completionexpected=0):

        optionsDict={"showdescription":showdescription,"allowsubmissionsfromdate":allowsubmissionsfromdate, "duedate":duedate, 
                        "cutoffdate":cutoffdate, "gradingduedate":gradingduedate, 
                        "assignsubmission_onlinetext_enabled":assignsubmission_onlinetext_enabled, 
                        "assignsubmission_file_enabled":assignsubmission_file_enabled, 
                        "assignsubmission_comments_enabled":assignsubmission_comments_enabled, 
                        "assignsubmission_file_maxfiles":assignsubmission_file_maxfiles, 
                        "assignsubmission_file_maxsizebytes":assignsubmission_file_maxsizebytes, 
                        "assignfeedback_comments_enabled":assignfeedback_comments_enabled, 
                        "assignfeedback_editpdf_enabled":assignfeedback_editpdf_enabled, 
                        "assignfeedback_comments_commentinline":assignfeedback_comments_commentinline, 
                        "submissiondrafts":submissiondrafts, "requiresubmissionstatement":requiresubmissionstatement, 
                        "maxattempts":maxattempts, "teamsubmission":teamsubmission, 
                        "preventsubmissionnotingroup":preventsubmissionnotingroup, 
                        "requireallteammemberssubmit":requireallteammemberssubmit, 
                        "teamsubmissiongroupingid":teamsubmissiongroupingid, "sendnotifications":sendnotifications, 
                        "sendlatenotifications":sendlatenotifications, 
                        "sendstudentnotifications":sendstudentnotifications, "grade":grade, "gradecat":gradecat, 
                        "gradepass":gradepass, "blindmarking":blindmarking, "hidegrader":hidegrader, 
                        "markingworkflow":markingworkflow,
                        "completionunlocked":completionunlocked,"completion":completion,
                        "completionusegrade":completionusegrade,"completionsubmit":completionsubmit,
                        "completionview":completionview,"completionpass":completionpass,"completionexpected":completionexpected}
        options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]        
        return options   

    def get_scheduler_options(self,showdescription=0,mform_isexpanded_id_optionhdr=1,staffrolename="Facilitator", maxbookings=10, schedulermode="oneonly", 
                                bookingrouping=-1, guardtime=0, defaultslotduration=60, allownotifications=0, 
                                usenotes=1, grade=0, usebookingform=0, usestudentnotes=0, uploadmaxfiles=0, requireupload=0,
                                completionunlocked=1,completion=0,completionview=0,completionpass=0,completionexpected=0):

        optionsDict={"showdescription":showdescription,"mform_isexpanded_id_optionhdr":mform_isexpanded_id_optionhdr,"staffrolename":staffrolename, "maxbookings":maxbookings, "schedulermode":schedulermode, 
                    "bookingrouping":bookingrouping, "guardtime":guardtime, "defaultslotduration":defaultslotduration, 
                    "allownotifications":allownotifications, "usenotes":usenotes, "grade":grade, 
                    "usebookingform":usebookingform, "usestudentnotes":usestudentnotes, 
                    "uploadmaxfiles":uploadmaxfiles, "requireupload":requireupload,
                    "completionunlocked":completionunlocked,"completion":completion,"completionview":completionview,"completionpass":completionpass,"completionexpected":completionexpected
                    }

        options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]        
        return options   
        
    def get_resource_options(self,showdescription=0,display=0,popupwidth=620, popupheight=450, printintro=1,filterfiles= 0,
                            completionunlocked=1,completion=2,completionview=1,completionpass=0,completionexpected=0):
        optionsDict={"showdescription":showdescription,"display":display,"popupwidth":popupwidth,"popupheight":popupheight,"printintro":printintro,"filterfiles":filterfiles,
                    "completionunlocked":completionunlocked,"completion":completion,"completionview":completionview,"completionpass":completionpass,"completionexpected":completionexpected}
        options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]        
        return options

    def get_hvp_options(self,moduleid,showdescription=0, h5paction="create", h5pmaxscore=0, gradecat=5, maximumgrade=10,
                        completionunlocked=1,completion=2,completionview=1,completionusegrade=1,completionpass=0,completionexpected=0,params=None):
        paramsOld, title, machine_name, libraryid=self.get_hvp_template_content_moodle(moduleid)
        if params==None:
            params=paramsOld

        optionsDict={"showdescription":showdescription,
                    "h5paction":h5paction,
                    "h5plibrary":libraryid,
                    "h5pmaxscore":h5pmaxscore,
                    "gradecat":gradecat,
                    "gradepass":0,
                    "maximumgrade":maximumgrade,
                    "completionunlocked":completionunlocked,"completion":completion,
                    "completionview":completionview,"completionpass":completionpass,"completionusegrade":completionusegrade,"completionexpected":completionexpected,
                    "params":params}
        options=[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]        
        return options

    def get_hvp_template_content_moodle(self,moduleid):
        regex = re.compile(r'<[^>]+>')
        #try:
        self.engine.dispose()
        con=self.engine.connect()
        #sqlQm="SELECT mh.json_content, mh.name, ml.machine_name FROM mdl_hvp mh INNER JOIN mdl_course_modules mcm ON mh.id=mcm.instance INNER JOIN mdl_hvp_libraries ml ON ml.id=mh.main_library_id WHERE mcm.id={}".format(moduleid)
        sqlQm="SELECT mh.main_library_id, mh.name, mh.json_content, mhl.machine_name, mhl.major_version, mhl.minor_version, mhl.patch_version FROM mdl_hvp mh INNER JOIN mdl_course_modules mcm ON mcm.instance=mh.id INNER JOIN mdl_hvp_libraries mhl WHERE mcm.id={} AND mhl.id=mh.main_library_id".format(moduleid)
        hvpRecord=read_sql(sql_text(sqlQm),con).to_dict(orient="records")[0]
        contentsjson=hvpRecord['json_content']  #.replace("\\n","").replace("&nbsp;","").replace("<div>","").replace("<p>","").replace("</div>","").replace("</p>","").replace("<\\/p>","").replace("\\","")

        title=hvpRecord['name']
        machine_name=hvpRecord['machine_name']
        libraryid="{} {}.{}".format(hvpRecord['machine_name'],hvpRecord['major_version'],hvpRecord['minor_version'])
        #contentDict=json.loads(contentsjson)
        #except:
        #    pass
        con.close()
        return regex.sub('', contentsjson), title, machine_name, libraryid        

    def create_hvp_module(self,courseid,sectionid,templateModuleid,title,description="",visible=1,optionsDict=None,hvpmethod=None,hvpparameters=None):
        modulename='hvp'
        statusResponse=self.create_course_module(modulename,courseid,sectionid,title,description,templateModuleid=templateModuleid,visible=visible,optionsDict=optionsDict)
        moduleid=statusResponse['response'][0]['moduleid']
        statusResponse=self.update_hvp_module(courseid,sectionid,moduleid,hvpmethod=hvpmethod,hvpparameters=hvpparameters)
        return statusResponse

    def update_hvp_module(self,courseid,sectionid,moduleid,title=None,description=None,visible=1,optionsDict=None,hvpmethod=None,hvpparameters=None):
        clean = re.compile(r'<[^>]+>')
        response=[]
        status='error'
        description=""
        try:
            json_content, name, hvpMainMachineName, libraryid=self.get_hvp_template_content_moodle(moduleid)
            args=(json.loads(json_content),)
            if optionsDict==None:
                optionsDict={}

            if title!=None:
                name=title

            if hvpmethod!=None:
                updatedContentDict=self.hvp_function_call(self.hvp_local_methods[hvpmethod],*args,**hvpparameters)
                #.replace("\\n","").replace("&nbsp;","").replace("<div>","").replace("<p>","").replace("</div>","").replace("</p>","")
                json_content=clean.sub('',json.dumps(updatedContentDict))
            optionsDict['params']=json_content
            optionsDict["showdescription"]=1
            optionsDict["h5paction"]="create"
            optionsDict["h5plibrary"]=libraryid

            modulename='hvp'
            self.engine.dispose()
            con=self.engine.connect()
            sqlQs="SELECT section FROM mdl_course_sections WHERE id={}".format(sectionid)
            section=read_sql(sql_text(sqlQs),con)['section'].to_list()[0]
            
            fname="local_tealmodmanage_update_modules"
            options=[{"name":"coursemodule","value":moduleid},{"name":"display","value":1}]+[{"name":ky, "value":optionsDict[ky]} for ky in [*optionsDict]]
            modules=[{"modulename":modulename,"section":section,"name":name,"description":description,"descriptionformat":1,"visible":visible,"options":options}]
            kwargs={"courseid":courseid,"modules":modules}
            response=kwargs
            response=self.call(self.mWAP, fname, **kwargs)
        except:
           pass 
        con.close()            
        return {"status":status,"response":response}

    def get_hvp_interactions(self,hvpmethod,moduleid):
        response=[]
        status='error'
        try:
            contentDict, titleold, hvpMainMachineName, libraryid=self.get_hvp_template_content_moodle(moduleid)
            args=(contentDict,)
            parameters={}
            response=self.hvp_function_call(self.hvp_local_methods[hvpmethod],*args,**parameters)
        except:
            pass 
        return {"status":status,"response":response}
##########
#HVP-MCQ
##########
    def add_multichoice_choice(self,text,correct):
        choice={'correct': correct, 'tipsAndFeedback': {'tip': '','chosenFeedback': '','notChosenFeedback': ''},'text': "{}".format(text)}
        return choice
    
    def update_hvp_MCQ_questions(self, *args, **kwargs):
        '''
        Webserice call: {"moduleid":<moduleid>}
        kwargs['questions']=[{'question':<>, 'answers':[{'text':<>,'correct':<1 or 0>}]}]
        Response: {'status':status,'response':response}
        ''' 
        contentDict=args[0]
        questions=kwargs['questions']
        temp=[]
        for intd in questions:
            question=copy.deepcopy(contentDict['questions'][0])
            question['params']['question']="{}".format(intd['question'])
            choices=[]
            for dct in intd['answers']:
                choices+=[self.add_multichoice_choice(dct['text'],dct['correct']==1)]
            question['params']['answers']=choices
            temp+=[question]                
        contentDict['questions']=copy.deepcopy(temp)
        # #self.add_hvp_template_content_dict(contentDict)
        response=contentDict
        #reponse=questions
        return response   

    def get_hvp_MCQ_questions(self,contentDict):
        '''
        Webserice call: {"moduleid":<moduleid>}
        questions=[{'question':<>, 'answers':[{'text':<>,'correct':<1 or 0>}]}]
        Response: {'status':status,'response':response}
        ''' 
        response={'questions':contentDict}
        status='error' 
        try:
            questions=contentDict['questions']
            temp=[]
            for intd in questions:
                tmpDct={}
                tmpDct['question']=intd['params']['question']
                choices=[]
                for dct in intd['params']['answers']:
                    choices+=[{'text':dct['text'],'correct':dct['correct']}]
                tmpDct['answers']=choices
                temp+=[tmpDct]                    
            response={'questions':temp}
            status='success'
        except:
           pass
        return response

############################
#HVP - Speak the words set
############################
    def update_hvp_SW(self,*args,**kwargs):
        '''
        Webserice call: {"moduleid":<moduleid>}
        questions=[{"title":"Title Goes Here", "inputLanguage":"si-LK","question":"The question", "acceptedAnswers":"කුමක් ද"}]
        Response: {'status':status,'response':response}
        ''' 
        contentDict=args[0]
        questions=kwargs['questions']
        temp=[]
        for qq in questions:
            question=copy.deepcopy(contentDict['questions'][0])
            question['metadata']['extraTitle']="{}".format(qq['title'])
            question['metadata']['title']="{}".format(qq['title'])
            question['params']['inputLanguage']=qq['inputLanguage']
            question['params']['question']=qq['question']
            question['params']['acceptedAnswers']=qq['acceptedAnswers']
            temp+=[question]                
        contentDict['questions']=copy.deepcopy(temp)
        #self.add_hvp_template_content_dict(contentDict)
        return  contentDict
            
    def get_hvp_SW_questions(self,contentDict):
        '''
        Webserice call: {"moduleid":<moduleid>}
        questions=[{"title":"Title Goes Here", "inputLanguage":"si-LK","question":"The question", "acceptedAnswers":"කුමක් ද"}]
        Response: {'status':status,'response':response}
        ''' 
        response={'questions':contentDict}
        status='error' 
        try:
            questions=contentDict['questions'] 
            temp=[]
            for intd in questions:
                tmpDct={}
                tmpDct['title']=intd['metadata']['title']
                tmpDct['inputLanguage']=intd['params']['inputLanguage']
                tmpDct['question']=intd['params']['question']
                tmpDct['acceptedAnswers']=intd['params']['acceptedAnswers']
                temp+=[tmpDct]                    
            response={'questions':temp}
            status='success'
        except:
           pass
        return response
    
###################
#HVP Interactive Video
###################
    def add_video(self,contentDict,url):
        contentDict['interactiveVideo']['video']['files']=[{'path': url,'mime': 'video/YouTube','copyright': {'license': 'U'}}]
        self.add_hvp_template_content_dict(contentDict)
        return contentDict

    def update_hvp_videointeractions_MCQ(self,*args,**kwargs):
        '''
        Webserice call: {"moduleid":<moduleid>}
        interactions=[{'label':<>, 'question':<>, 'answers':[{'text':<>,'correct':<1 or 0>}], 'start':<>, 'end':<>}]
        Response: {'status':status,'response':response}
        ''' 
        contentDict=args[0]
        url=kwargs['url']
        interactions=kwargs['interactions']
        if url!='':
            contentDict['interactiveVideo']['video']['files']=[{'path': url,'mime': 'video/YouTube','copyright': {'license': 'U'}}]
        temp=[]
        for intd in interactions:
            interaction=copy.deepcopy(contentDict['interactiveVideo']['assets']['interactions'][0])
            interaction['action']['metadata']['extraTitle']="{}".format(intd['label'])
            interaction['action']['metadata']['title']="{}".format(intd['label'])
            interaction['label']="{}".format(intd['label'])
            interaction['duration']={'from':intd['start'],'to':intd['end']}
            interaction['action']['params']['question']="{}".format(intd['question'])
            choices=[]
            for dct in intd['answers']:
                choices+=[self.add_multichoice_choice(dct['text'],dct['correct']==1)]
            interaction['action']['params']['answers']=choices
            temp+=[interaction]                
        contentDict['interactiveVideo']['assets']['interactions']=copy.deepcopy(temp)
        #self.add_hvp_template_content_dict(contentDict)
        return  contentDict

    def get_hvp_video_interactions(self,contentDict):
        '''
        Webserice call: {"moduleid":<moduleid>}
        interactions=[{'label':<>, 'question':<>, 'answers':[{'text':<>,'correct':<1 or 0>}], 'duration':{'start':<>, 'end':<>}}]
        Response: {'status':status,'response':response}
        ''' 
        response={"files":[],"interactions":contentDict}
        status='error' 
        try:
            files=contentDict['interactiveVideo']['video']['files']
            interactions=contentDict['interactiveVideo']['assets']['interactions'] 
            temp=[]
            for intd in interactions:
                tmpDct={}
                tmpDct['label']=intd['label']
                tmpDct['duration']=intd['duration']
                tmpDct['question']=intd['action']['params']['question']
                choices=[]
                for dct in intd['action']['params']['answers']:
                    choices+=[{'text':dct['text'],'correct':dct['correct']}]
                tmpDct['answers']=choices
                temp+=[tmpDct]                    
            response={"files":files,"interactions":temp}
            status='success'
        except:
           pass
        return response

    def get_video_interactions_list(self):
        clean = re.compile(r'<[^>]+>')
        interactionsList={re.sub(clean, '', dct['label']):dct for dct in self.contentDict['interactiveVideo']['assets']['interactions']}
        return interactionsList

    def get_video_interaction(self,label):
        interaction=[dct for dct in self.contentDict['interactiveVideo']['assets']['interactions'] if re.sub(clean, '', dct['label'])==label][0]
        return interaction  


##########################################################
#Data Analysis
##########################################################
    def principle_component_values(self, modeldata, predictdata, nnPCs):
        response={'PCA_object':[],'PCAmeans':[],'fitScores': {'PCApredictScore':[], 'PCAmodelScore':[]}, 'PCweights':[], 'modelnumPCA':[],'predictnumPCA':[]}
        status='error'
        try:
            modelDF=DataFrame(modeldata)
            predictDF=DataFrame(predictdata)
            pca=sklearn.decomposition.PCA(n_components=nnPCs);
            modelnumPCA=pca.fit_transform(modelDF);
            PCweights=pca.singular_values_;
            PCAmodelScore=pca.score(modelDF);
            PCAmeans=pca.mean_
            predictnumPCA=pca.transform(predictDF);
            PCApredictScore=pca.score(predictDF);
            response={'PCA_object':pca,'PCAmeans':PCAmeans,'fitScores': {'PCApredictScore':PCApredictScore, 'PCAmodelScore':PCAmodelScore}, 'PCweights':PCweights, 'modelnumPCA':modelnumPCA,'predictnumPCA':predictnumPCA}
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def gmm_data_classifier(self, modelDataDicts, predictDataDicts,nClusters):
        response={'labeled model data':[], 'labeled predict data':[],'fitScore':{'modelFitScore':[], 'predictFitScore':[]},'Probability Model':[]}
        status='error'
        try:
            modelDataPDF0=DataFrame(modelDataDicts);
            predictDataPDF0=DataFrame(predictDataDicts);
            modelData=modelDataPDF0.to_numpy();
            predictData=predictDataPDF0.to_numpy();
            nPCs=modelData.shape[1]
            gmm = sklearn.mixture.GaussianMixture(n_components = nClusters)
            gmm.fit(modelData)

            mLabels = gmm.predict(modelData)
            modelDist={'Model Mean':gmm.means_, 'Model Covaraince':gmm.covariances_};
            modelSampleFitScore=gmm.score_samples(modelData);
            modelDataPDF0['labels']=mLabels
            modelDataPDF0['Fit Score']=modelSampleFitScore;

            pLabels = gmm.predict(predictData)
            predictProbDist=gmm.predict_proba(predictData);
            predictSampleFitScore=gmm.score_samples(predictData);

            predictDataPDF0['labels']=pLabels
            predictDataPDF0['Fit Score']=predictSampleFitScore;
            response={'labeled model data':modelDataPDF0.to_dict(orient='records'), 'labeled predict data':predictDataPDF0.to_dict(orient='records'),'fitScore':{'modelFitScore':modelSampleFitScore, 'predictFitScore':predictSampleFitScore},'Probability Model':modelDist}
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_course_users_module_interaction(self,courseid,startDateStr,endDateStr):
        response=[]
        status='error'
        try:
            userslist=self.get_course_users_list(courseid)['response']
            userids=list(set([dct['value'] for dct in userslist]))
            userids.sort()
            contextlevel=70
            edulevel=2
            userints=self.get_users_graph_properties(userids,contextlevel,edulevel,startDateStr,endDateStr)['response']
            print(userints)
            dataPDF=DataFrame.from_records(userints,index='userid')
            dataPDF.loc[:,'usrdt']=[zz for zz in dataPDF['usrdt'].to_list()]        
            print(dataPDF)
            PCAdata=self.principle_component_values(dataPDF.to_dict(orient='records'),dataPDF.to_dict(orient='records'),5)['response']
            print(PCAdata)
            #dataPCA=DataFrame(PCAdata['modelnumPCA'],index=dataPDF.index.values)
            results=self.gmm_data_classifier(PCAdata['modelnumPCA'],PCAdata['modelnumPCA'],3)['response']
            clustered=dataPDF.copy(deep=True)
            clustered.loc[:,'labels']=pd.DataFrame(results['labeled model data'])['labels'].to_list()

            response=clustered.to_dict(orient='index')
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_course_user_clusters(self, courseid, startDateStr, endDateStr):
        response=[]
        status='error'
        try:
            userslist=self.get_course_users_list(courseid)['response']
            userids=list(set([dct['value'] for dct in userslist]))
            userids.sort()
            contextlevel=70; edulevel=2;
            userints=self.get_users_graph_properties(userids,contextlevel,edulevel,startDateStr,endDateStr)['response']
            dataPDF=DataFrame.from_records(userints,index='userid')[['density','global_reaching_centrality','total_re_visits','number_of_nodes','number_of_selfloops','totaldedication','totalgrade']]
            #dataPDF.loc[:,'usrdt']=[zz for zz in dataPDF['usrdt'].to_list()]
            PCAdata=self.principle_component_values(dataPDF.to_dict(orient='records'),dataPDF.to_dict(orient='records'),5)['response']
            #dataPCA=DataFrame(PCAdata['modelnumPCA'],index=dataPDF.index.values)
            results=self.gmm_data_classifier(PCAdata['modelnumPCA'],PCAdata['modelnumPCA'],3)['response']
            clustered=dataPDF.copy(deep=True)
            clustered.loc[:,'labels']=DataFrame(results['labeled model data'])['labels'].to_list()
            clustered.loc[:,'userid']=dataPDF.index.values
            usersDict={dct['value']:dct['label'] for dct in userslist}
            usernames=[usersDict[id] for id in dataPDF.index.values]
            clustered.loc[:,'user']=usernames
            response=clustered.to_dict(orient='records')
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_course_user_clusters_figures(self, courseid, startDateStr, endDateStr):
        response=[]
        status='error'
        try:
            userslist=self.get_course_users_list(courseid)['response']
            userids=list(set([dct['value'] for dct in userslist]))
            userids.sort()
            contextlevel=70; edulevel=2;
            userints=self.get_users_graph_properties(userids,contextlevel,edulevel,startDateStr,endDateStr)['response']
            dataPDF=DataFrame.from_records(userints,index='userid')[['density','global_reaching_centrality','total_re_visits','number_of_nodes','number_of_selfloops','totaldedication','totalgrade']]
            #dataPDF.loc[:,'usrdt']=[zz for zz in dataPDF['usrdt'].to_list()]
            PCAdata=self.principle_component_values(dataPDF.to_dict(orient='records'),dataPDF.to_dict(orient='records'),5)['response']
            #dataPCA=DataFrame(PCAdata['modelnumPCA'],index=dataPDF.index.values)
            results=self.gmm_data_classifier(PCAdata['modelnumPCA'],PCAdata['modelnumPCA'],3)['response']
            df=dataPDF.copy(deep=True)
            df.loc[:,'labels']=DataFrame(results['labeled model data'])['labels'].to_list()
            df.loc[:,'userid']=dataPDF.index.values
            usersDict={dct['value']:dct['label'] for dct in userslist}
            usernames=[usersDict[id] for id in dataPDF.index.values]
            df.loc[:,'user']=usernames

            df.loc[:,'labels']=['G-'+str(zz) for zz in df['labels'].to_list()]
            df.loc[:,'totaldedication']=[round(zz) for zz in df['totaldedication'].to_list()]
            df.loc[:,'totalgrade']=[round(zz) for zz in df['totalgrade'].to_list()]

            renameMap={'number_of_nodes':'Number of activities','totaldedication':'Time spent / mins','labels':'Cluster','total_re_visits':'Number of re-visits','number_of_selfloops':'Number of continuations'}
            df.rename(columns=renameMap,inplace=True)
            hovercol='Number of activities' #['density','global_reaching_centrality','Cluser','Number of activities','Number of continuations','Number of re-visits','Time spent','userid']
            xcol='Time spent / mins'
            colorcol='Cluster'
            ycol='Number of re-visits'
            sizecol='Number of continuations'
            zcol='Number of activities'
            #fig2d = px.scatter(df, x=xcol, y=ycol, color=colorcol,size=sizecol, hover_data=['user'])        
            fig3d = px.scatter_3d(df, x=xcol, y=ycol, z=zcol, color=colorcol,size=sizecol, hover_data=['user','Time spent / mins','totalgrade'])        
            response={'figures':[fig3d.to_json()],'data':df.to_dict(orient='records')}
            status='success'
        except:
            pass
        return {'status':status,'response':response}
###########################################################
##Working area
##########################################################
    def get_module_files(self,moduleid):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT mf.* FROM mdl_files mf WHERE mf.contextid=(SELECT mctx.id FROM mdl_context mctx WHERE mctx.contextlevel = 70 AND mctx.instanceid={})".format(moduleid)            
            filesDict=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            filesList=[]
            for dct in filesDict:
                if dct['filename']!='.':
                    filesList+=["{}/pluginfile.php/{}/{}/{}/{}{}{}".format(siteURL,dct['contextid'],dct['component'],dct['filearea'],dct['itemid'],dct['filepath'],dct['filename'])]    
            status='success'
            response=filesList
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_contextid_from_module_instance(self,modtype,instanceid):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ='SELECT mc.id AS contextid, mcm.id AS moduleid FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_context mc ON mc.instanceid=mcm.instance WHERE mm.name="{}" AND mcm.instance={} AND mc.contextlevel=70'.format(modtype,instanceid)
            #{"sqlQ":"SELECT * FROM mdl_context WHERE instanceid=864"}
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_course_assignment_local_roles_full_info(self,courseids):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=70
        modtype='assign'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            #sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.course={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,courseid)                
            #sqlQ="SELECT mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.firstname AS userfirstname, mu.lastname AS userlastname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.deletioninprogress=0 AND mcm.course={} AND mctx.contextlevel={}".format(courseid,contextlevel)
            #sqlQ="SELECT mh.activity, mh.allowsubmissionsfromdate, mh.timelimit, mh.intro AS activityintro, mh.cutoffdate, mh.duedate, mh.grade, mh.gradingduedate, mh.name AS activityname, mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={}".format(modtype,tuple(courseids+[0]),contextlevel)
            #sqlQ="SELECT mgg.finalgrade AS grade, mh.activity, mh.allowsubmissionsfromdate, mh.timelimit, mh.intro AS activityintro, mh.cutoffdate, mh.duedate, mgi.grademax, mgi.grademin, mgi.gradepass, mh.gradingduedate, mh.name AS activityname, mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mh.id INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={} AND mra.userid=mgg.userid".format(modtype,tuple(courseids+[0]),contextlevel)
            #sqlQ="SELECT mgi.gradetype, mgg.finalgrade AS grade, mh.activity, mh.allowsubmissionsfromdate, mh.timelimit, mh.intro AS activityintro, mh.cutoffdate, mh.duedate, mgi.grademax, mgi.grademin, mgi.gradepass, mh.gradingduedate, mh.name AS activityname, mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mh.id LEFT JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id AND mgg.userid=mra.userid WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={}".format(modtype,tuple(courseids+[0]),contextlevel)
            sqlQ="SELECT mgi.gradetype, mgg.finalgrade AS grade, mh.activity, mh.allowsubmissionsfromdate, mh.timelimit, mh.intro AS activityintro, mh.cutoffdate, mh.duedate, mgi.grademax, mgi.grademin, mgi.gradepass, mh.gradingduedate, mh.name AS activityname, mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mh.id LEFT JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id AND mgg.userid=mra.userid WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mgi.itemmodule='{}' AND mctx.contextlevel={}".format(modtype,tuple(courseids+[0]),modtype,contextlevel)
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['allowsubmissionsfromdate'] = to_datetime(df['allowsubmissionsfromdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['duedate'] = to_datetime(df['duedate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['cutoffdate'] = to_datetime(df['cutoffdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['gradingduedate'] = to_datetime(df['gradingduedate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            response=df.to_dict(orient='records')

            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records')          
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_course_assignment_local_roles_full_info_by_role_by_userids(self,courseids,userids,rolename):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=70
        modtype='assign'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            #sqlQ="SELECT mh.activity, mh.allowsubmissionsfromdate, mh.timelimit, mh.intro AS activityintro, mh.cutoffdate, mh.duedate, mh.grade, mh.gradingduedate, mh.name AS activityname, mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={} AND mr.shortname='{}' AND mra.userid IN {}".format(modtype,tuple(courseids+[0]),contextlevel,rolename,tuple(userids+[0]))
            sqlQ="SELECT mgg.finalgrade AS grade, mh.activity, mh.allowsubmissionsfromdate, mh.timelimit, mh.intro AS activityintro, mh.cutoffdate, mh.duedate, mgi.grademax, mgi.grademin, mgi.gradepass, mh.gradingduedate, mh.name AS activityname, mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mh.id INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={} AND mra.userid=mgg.userid AND mra.userid IN {} AND mr.shortname='{}'".format(modtype,tuple(courseids+[0]),contextlevel,tuple(userids+[0]),rolename)
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['allowsubmissionsfromdate'] = to_datetime(df['allowsubmissionsfromdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['duedate'] = to_datetime(df['duedate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['cutoffdate'] = to_datetime(df['cutoffdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['gradingduedate'] = to_datetime(df['gradingduedate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            response=df.to_dict(orient='records')

            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records')          
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_assignment_local_roles_full_info_by_modules(self,moduleids):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=70
        modtype='assign'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            #sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.course={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,courseid)                
            #sqlQ="SELECT mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.firstname AS userfirstname, mu.lastname AS userlastname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.deletioninprogress=0 AND mcm.course={} AND mctx.contextlevel={}".format(courseid,contextlevel)
            sqlQ="SELECT mh.activity, mh.allowsubmissionsfromdate, mh.timelimit, mh.intro AS activityintro, mh.cutoffdate, mh.duedate, mh.grade AS grademax, mh.gradingduedate, mh.name AS activityname, mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.deletioninprogress=0 AND mcm.id IN {} AND mctx.contextlevel={}".format(modtype,tuple(moduleids+[0]),contextlevel)
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['allowsubmissionsfromdate'] = to_datetime(df['allowsubmissionsfromdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['duedate'] = to_datetime(df['duedate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['cutoffdate'] = to_datetime(df['cutoffdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['gradingduedate'] = to_datetime(df['gradingduedate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            response=df.to_dict(orient='records')
            
            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records')          
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_course_modules_local_roles_full_info(self,courseids):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=70
        try:
            self.engine.dispose()
            con=self.engine.connect()
            #sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.course={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,courseid)                
            sqlQ="SELECT mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.firstname AS userfirstname, mu.lastname AS userlastname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={}".format(tuple(courseids+[0]),contextlevel)
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            for modtype in list(set(df['modulename'].to_list())):
                tmpPDF0=df[df['modulename']==modtype].copy()
                for instnceid in list(set(tmpPDF0['instanceid'].to_list())):
                    tmpPDF1=tmpPDF0[tmpPDF0['instanceid']==instnceid]
                    modDicts=tmpPDF1.to_dict(orient='records')
                    instanceDicts=[{}]
                    sqlQ="SELECT mh.name AS activityname FROM mdl_{} mh WHERE mh.id={}".format(modtype,instnceid)
                    instanceDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    for modDict in modDicts:
                        modDict.update(instanceDicts[0])
                        response+=[modDict]
            
            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                        
                    response+=modulePDF.to_dict(orient='records') 

            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_modules_local_roles_full_info_by_ids(self,moduleids):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=70
        try:
            self.engine.dispose()
            con=self.engine.connect()
            #sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.course={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,courseid)                
            sqlQ="SELECT mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.firstname AS userfirstname, mu.lastname AS userlastname, mu.email AS useremail, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.deletioninprogress=0 AND mcm.id IN {} AND mctx.contextlevel={}".format(tuple(moduleids+[0]),contextlevel)
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            for modtype in list(set(df['modulename'].to_list())):
                tmpPDF0=df[df['modulename']==modtype].copy()
                for instnceid in list(set(tmpPDF0['instanceid'].to_list())):
                    tmpPDF1=tmpPDF0[tmpPDF0['instanceid']==instnceid]
                    modDicts=tmpPDF1.to_dict(orient='records')
                    instanceDicts=[{}]
                    sqlQ="SELECT mh.name AS activityname FROM mdl_{} mh WHERE mh.id={}".format(modtype,instnceid)
                    instanceDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    for modDict in modDicts:
                        modDict.update(instanceDicts[0])
                        response+=[modDict]
            
            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                        
                    response+=modulePDF.to_dict(orient='records') 

            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_course_modules_full_info(self,courseids):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=70
        try:
            self.engine.dispose()
            con=self.engine.connect()
            #sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.course={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,courseid)                
            sqlQ="SELECT mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category WHERE mcm.deletioninprogress=0 AND mcm.course IN {}".format(tuple(courseids+[0]))
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            for modtype in list(set(df['modulename'].to_list())):
                tmpPDF0=df[df['modulename']==modtype].copy()
                for instnceid in list(set(tmpPDF0['instanceid'].to_list())):
                    tmpPDF1=tmpPDF0[tmpPDF0['instanceid']==instnceid]
                    modDicts=tmpPDF1.to_dict(orient='records')
                    instanceDicts=[{}]
                    sqlQ="SELECT mh.name AS activityname FROM mdl_{} mh WHERE mh.id={}".format(modtype,instnceid)
                    instanceDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    for modDict in modDicts:
                        modDict.update(instanceDicts[0])
                        response+=[modDict]
            df=DataFrame(response)
            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records')                         
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_modules_full_info_by_ids(self,moduleids):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=70
        try:
            self.engine.dispose()
            con=self.engine.connect()
            #sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.course={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,courseid)                
            sqlQ="SELECT mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category WHERE mcm.deletioninprogress=0 AND mcm.id IN {}".format(tuple(moduleids+[0]))
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            for modtype in list(set(df['modulename'].to_list())):
                tmpPDF0=df[df['modulename']==modtype].copy()
                for instnceid in list(set(tmpPDF0['instanceid'].to_list())):
                    tmpPDF1=tmpPDF0[tmpPDF0['instanceid']==instnceid]
                    modDicts=tmpPDF1.to_dict(orient='records')
                    instanceDicts=[{}]
                    sqlQ="SELECT mh.name AS activityname FROM mdl_{} mh WHERE mh.id={}".format(modtype,instnceid)
                    instanceDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    for modDict in modDicts:
                        modDict.update(instanceDicts[0])
                        response+=[modDict]
            df=DataFrame(response)
            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records')                         
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_course_modules_by_type(self,modtype,courseid):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        self.engine.dispose()
        con=self.engine.connect()
        contextlevel=70
        try:
            #sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.course={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,courseid)                
            sqlQ="SELECT mr.name AS rolename, mr.shortname AS roleshortname, mm.name AS modulename, mh.*, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mra.contextid, mra.roleid, mra.userid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mu.firstname AS userfirstname, mu.lastname AS userlastname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mra.userid INNER JOIN mdl_role mr ON mr.id=mra.roleid WHERE mcm.deletioninprogress=0 AND mcm.course={} AND mctx.contextlevel={} AND mm.name='{}'".format(modtype,courseid,contextlevel,modtype)
            df=read_sql(sql_text(sqlQ),con)
            response=df.to_dict(orient='records')
            
            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = round(int(dct['value'])) # datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records')            
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_section_modules_by_type(self,modtype,sectionid):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        self.engine.dispose()
        con=self.engine.connect()    
        try:
            sqlQ="SELECT mcm.id AS moduleid, mcm.section AS sectionid, mcm.visible AS modvisible, mcm.visibleoncoursepage, mcm.completion, mcs.name AS sectionname, mcs.section AS sectionorder, mc.shortname AS courseshortname, mc.fullname AS coursename, mcc.id AS categoryid, mctx.id AS contextid, ma.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.section={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0)".format(modtype,modtype,sectionid)                
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_section_modules_list_by_type(self,modtype,sectionid,modvisible=1):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mcm.id AS value, ma.name AS label FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} ma ON ma.id=mcm.instance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE (mm.name='{}' AND mcm.section={} AND mctx.contextlevel=70 AND mcm.deletioninprogress=0 AND mcm.visible={})".format(modtype,modtype,sectionid,modvisible)                
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'    
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def create_calendar_events(self,datadicts):
        '''
        Webserice call: {"datadicts":[{"courseid":"int","name":"str","description":"str","eventtype":"str-user,course","repeats":"int","timestart":"24/12/2023 0800", "timeduration":""}]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        eventedicts=[]
        for dct in datadicts:
            dct['timestart']=int(time.mktime(to_datetime([dct['timestart']], errors='raise', dayfirst=True,infer_datetime_format=True).to_pydatetime()[0].timetuple()))
            eventedicts+=[dct]

        parameters={"events":eventedicts}
        print(parameters)
        try:
            response=self.call(self.mWAP,'core_calendar_create_calendar_events',**parameters)
            print(response)
            status='success'
        except:
            pass

        return {'status':status,'response':response}

    def get_course_scheduler_events_full_info(self,courseids):
        '''
        Webserice call: {"courseid":courseid,"schedulerid":schedulerid}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect() 
        modtype='scheduler'  
        contextlevel=70    
        try:
            #sqlQ="SELECT mss.starttime, mss.teacherid, mss.notes, mss.hideuntil, mss.duration, mss.emaildate, mh.name AS schedulername, mh.staffrolename, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_scheduler_slots mss ON mss.schedulerid=mh.id INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category WHERE mcm.deletioninprogress=0 AND mcm.course={}".format(modtype,courseid)
            #sqlQ="SELECT msa.studentid, msa.attended, msa.appointmentnote, msa.teachernote, msa.studentnote, msa.grade , mss.starttime, mss.teacherid, mss.notes AS schedulenotes, mss.hideuntil, mss.duration, mss.emaildate, mh.name AS schedulername, mh.staffrolename, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_scheduler_slots mss ON mss.schedulerid=mh.id INNER JOIN mdl_scheduler_appointment msa ON msa.slotid=mss.id INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category WHERE mcm.deletioninprogress=0 AND mcm.course={}".format(modtype,courseid)
            #sqlQ="SELECT mh.intro AS schedulerintro, mss.appointmentlocation, mus.email AS student, mut.email AS teacher, msa.studentid, msa.attended, msa.appointmentnote, msa.teachernote, msa.studentnote, msa.grade , mss.starttime, mss.teacherid, mss.notes AS schedulenotes, mss.hideuntil, mss.duration, mss.emaildate, mh.name AS schedulername, mh.staffrolename, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_scheduler_slots mss ON mss.schedulerid=mh.id INNER JOIN mdl_scheduler_appointment msa ON msa.slotid=mss.id INNER JOIN mdl_user mut ON mut.id=mss.teacherid INNER JOIN mdl_user mus ON mus.id=msa.studentid INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {}".format(modtype,tuple(courseids+[0]))
            #sqlQ="SELECT mctx.id AS contextid, mh.intro AS schedulerintro, mss.appointmentlocation, mus.email AS student, mut.email AS teacher, msa.studentid, msa.attended, msa.appointmentnote, msa.teachernote, msa.studentnote, msa.grade , mss.starttime, mss.teacherid, mss.notes AS schedulenotes, mss.hideuntil, mss.duration, mss.emaildate, mh.name AS schedulername, mh.staffrolename, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_scheduler_slots mss ON mss.schedulerid=mh.id INNER JOIN mdl_scheduler_appointment msa ON msa.slotid=mss.id INNER JOIN mdl_user mut ON mut.id=mss.teacherid INNER JOIN mdl_user mus ON mus.id=msa.studentid INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={}".format(modtype,tuple(courseids+[0]),contextlevel)
            sqlQ="SELECT mgi.gradetype, mgi.grademax, mgi.grademin, mgi.gradepass, mctx.id AS contextid, mh.intro AS schedulerintro, mss.appointmentlocation, mus.email AS student, mut.email AS teacher, msa.studentid, msa.attended, msa.appointmentnote, msa.teachernote, msa.studentnote, msa.grade , mss.starttime, mss.teacherid, mss.notes AS schedulenotes, mss.hideuntil, mss.duration, mss.emaildate, mh.name AS schedulername, mh.staffrolename, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_scheduler_slots mss ON mss.schedulerid=mh.id INNER JOIN mdl_scheduler_appointment msa ON msa.slotid=mss.id INNER JOIN mdl_user mut ON mut.id=mss.teacherid INNER JOIN mdl_user mus ON mus.id=msa.studentid INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mcm.id INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mh.id WHERE mcm.course=mh.course AND mcm.deletioninprogress=0 AND mcm.course IN {} AND mctx.contextlevel={} AND mgi.itemmodule='{}'".format(modtype,tuple(courseids+[0]),contextlevel,modtype)
            df=read_sql(sql_text(sqlQ),con)
            df['schedulerintro'] = df['schedulerintro'].str.replace(r'<[^<>]*>', '', regex=True)
            df['appointmentnote'] = df['appointmentnote'].str.replace(r'<[^<>]*>', '', regex=True)
            df['schedulenotes'] = df['schedulenotes'].str.replace(r'<[^<>]*>', '', regex=True)
            df['studentnote'] = df['studentnote'].str.replace(r'<[^<>]*>', '', regex=True)
            df['teachernote'] = df['teachernote'].str.replace(r'<[^<>]*>', '', regex=True)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s', utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['starttime'] = to_datetime(df['starttime'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')            
            df['emaildate'] = to_datetime(df['emaildate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')            
            df['hideuntil'] = to_datetime(df['hideuntil'],unit='s', utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')            
            response=df.to_dict(orient='records')

            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records') 

            status='success'
        except:
            pass
        con.close()            
        return {'status':status,'response':response}

    def get_course_scheduler_events_full_info_by_role_by_userids(self,courseids,userids,rolename):
        '''
        Webserice call: {"courseid":courseid,"schedulerid":schedulerid}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'   
        try:
            shcedulerPDF=DataFrame(self.get_course_scheduler_events_full_info(courseids)['response'])
            if rolename=='student':
                response=shcedulerPDF[shcedulerPDF['studentid'].isin(userids)].to_dict(orient='records')
            elif rolename=='teacher':
                response=shcedulerPDF[shcedulerPDF['teacherid'].isin(userids)].to_dict(orient='records')
            status='success'
        except:
            pass          
        return {'status':status,'response':response}        

    def get_scheduler_events_full_info_by_modules(self,moduleids):
        '''
        Webserice call: {"courseid":courseid,"schedulerid":schedulerid}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect() 
        modtype='scheduler'      
        try:
            sqlQ="SELECT mh.intro AS schedulerintro, mss.appointmentlocation, mus.email AS student, mut.email AS teacher, msa.studentid, msa.attended, msa.appointmentnote, msa.teachernote, msa.studentnote, msa.grade , mss.starttime, mss.teacherid, mss.notes AS schedulenotes, mss.hideuntil, mss.duration, mss.emaildate, mh.name AS schedulername, mh.staffrolename, mm.name AS modulename, mcm.instance AS instanceid, mcm.id AS moduleid, mcm.section AS sectionid, mcm.course AS courseid, mc.category AS categoryid, mcs.name AS sectionname, mc.fullname AS coursename, mcc.name AS categoryname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_scheduler_slots mss ON mss.schedulerid=mh.id INNER JOIN mdl_scheduler_appointment msa ON msa.slotid=mss.id INNER JOIN mdl_user mut ON mut.id=mss.teacherid INNER JOIN mdl_user mus ON mus.id=msa.studentid INNER JOIN mdl_course mc ON mc.id=mcm.course INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category WHERE mcm.deletioninprogress=0 AND mcm.id IN {}".format(modtype,tuple(moduleids+[0]))
            df=read_sql(sql_text(sqlQ),con)
            # df['schedulerintro'] = df['schedulerintro'].str.replace(r'<[^<>]*>', '', regex=True)
            # df['appointmentnote'] = df['appointmentnote'].str.replace(r'<[^<>]*>', '', regex=True)
            # df['schedulenotes'] = df['schedulenotes'].str.replace(r'<[^<>]*>', '', regex=True)
            # df['studentnote'] = df['studentnote'].str.replace(r'<[^<>]*>', '', regex=True)
            # df['teachernote'] = df['teachernote'].str.replace(r'<[^<>]*>', '', regex=True)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['starttime'] = to_datetime(df['starttime'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')            
            df['emaildate'] = to_datetime(df['emaildate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')            
            df['hideuntil'] = to_datetime(df['hideuntil'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')            
            response=df.to_dict(orient='records')

            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records') 

            status='success'
        except:
            pass
        con.close()            
        return {'status':status,'response':response}
    
    def core_xapi_statement_post(self,component):
        '''
        Webserice call: {"eventsinfodict":<{"courseid":courseid,"name":name,"description":description,"eventtype":eventtype,"repeats":repeats,"timestart":timestartstr, "timeduration":timeduration}}>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        statement={
            "actor": {
                "account": {
                            "objectType": "agent",
                            "homePage": "wwwroot", 
                            "name": "4"
                }
            },
            "verb": {
                    "id": "http://adlnet.gov/expapi/verbs/viewed"
            },
            "object": {
                        
                        "objectType": "activity"
            }
            }
        requestjson=json.dumps(statement)
        print(requestjson)
        parameters={"component":component,"requestjson":requestjson}
        print(parameters)
        #try:
        response=self.call(self.mWAP,'core_xapi_statement_post',**parameters)
        print(response)
        status='success'
        #except:
        #    pass

        return {'status':status,'response':response}

    def get_module_users_grade(self, moduleid, userids):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            moduleid,
            #sqlQ="SELECT gi.courseid, gi.categoryid, gi.grademax, gi.grademin, gi.gradepass, gi.id AS itemid, gg.rawgrade,	gg.rawgrademax,	gg.rawgrademin,	gg.finalgrade, gg.timecreated, gg.timemodified, gg.userid  FROM mdl_grade_items gi INNER JOIN mdl_grade_grades gg ON gi.id=gg.itemid WHERE gi.iteminstance={} AND gg.userid IN {}".format(moduleid,tuple(userids+[0]))
            sqlQ="SELECT mgi.*, mgg.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_grade_items mgi ON mgi.itemmodule=mm.name INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mcm.instance=mgi.iteminstance AND mcm.id={} AND mgg.userid IN {}".format(moduleid,tuple(userids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'
        except:
            pass
        con.close()            
        return {'status':status,'response':response}

###########################################################
##Group create/edit/delete
##########################################################
    def add_group_members(self,members):
        '''
        Webserice call: {"members":[{"groupid":<group id>,"userid":<userid>}]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        #try:
        response=self.call(self.mWAP,'core_group_add_group_members', members=members)
        print(response)
        status='success'
        #except:
        #    pass

        return {'status':status,'response':response}  

    def create_course_groups(self,groups):
        '''
        Webserice call: {"groups":[{"courseid":<courseid>,"name":<name>,"description":<description>,"idnumber":<idnumber>}]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_group_create_groups',groups=groups)
            print(response)
            status='success'
        except:
            pass

        return {'status':status,'response':response}  

    def get_course_groups(self,courseid):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        #try:
        response=self.call(self.mWAP,'core_group_get_course_groups',courseid=courseid)
        print(response)
        status='success'
        #except:
        #    pass

        return {'status':status,'response':response}  

    def get_group_members(self,groupids):
        '''
        Webserice call: {"courseid":<courseid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        #try:
        response=self.call(self.mWAP,'core_group_get_group_members',groupids=groupids)
        print(response)
        status='success'
        #except:
        #    pass

        return {'status':status,'response':response}  


###########################################################
##Category create/edit/delete
##########################################################
    def create_course_categories_bulk(self,datadicts):
        response=[]
        status='error'
        category={'name':'name','idnumber':'','description':'','descriptionformat': 1, 'parent': 0,'theme':''}
        categoryinfodicts=datadicts
        try:
            categories=[]
            for dct in categoryinfodicts:
                temp=copy.deepcopy(category)
                for ky in [*dct]:
                    temp[ky]=dct[ky]
                categories+=[temp]
            response=self.call(self.mWAP,'core_course_create_categories', categories=categories)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def create_course_category(self,categoryname,parentid=0,description='',idnumber=''):
        response=[]
        status='error'
        try:
            catDicts=self.call(self.mWAP,'core_course_get_categories ',criteria=[{'key':'name', 'value':categoryname}])
            catDicts=[dct for dct in catDicts if dct['name']==categoryname]
            if len(catDicts)==0:
                    categorydict={'name':categoryname,'idnumber':idnumber,'description':description,'descriptionformat': 1, 'parent': parentid,'theme':''}
                    print(categorydict)
                    response=self.call(self.mWAP,'core_course_create_categories', categories=[categorydict])
                    status='success'
                    print(response)
            else:
                status='Category by the name '+categoryname+' already exists'
                response=[]
        except:
            pass
        return {'status':status,'response':response}

    def delete_course_categories(self,categoryids):
        response=[]
        status='error'
        try:
            categoryids.sort(reverse=True)
            deleteCategories=[{'id': id, 'recursive':1} for id in categoryids]
            print(deleteCategories)
            response=self.call(self.mWAP,'core_course_delete_categories',categories=deleteCategories)
            status='success'
        except:
            pass

        return {'status':status, 'response':response}

    def get_category_list_old(self):
        response=[{'label':'Top','value':0}]
        status="error"
        try:
            categoriesInfo=self.call(self.mWAP,'core_course_get_categories')
            #categoriesInfo+=[{'name':'Top', 'id':0}]
            labelNames=[dct['name'] for dct in categoriesInfo]
            #labelNames.sort()
            response=[{'label':lbl,'value':dct['id']} for lbl in labelNames for dct in categoriesInfo  if dct['name']==lbl]
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_category_list(self,visible=1):
        response=[{'label':'Top','value':0}]
        status="error"
        try:
            categoriesInfo=self.call(self.mWAP,'core_course_get_categories')
            #categoriesInfo+=[{'name':'Top', 'id':0}]
            labelNames=[dct['name'] for dct in categoriesInfo]
            #labelNames.sort()
            response=[{'label':lbl,'value':dct['id']} for lbl in labelNames for dct in categoriesInfo  if ((dct['name']==lbl) & (dct['visible']==visible))]
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_categories_get_categorynames_list(self,categoryids):
        '''
        '''
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mc.name AS label, mc.id AS value FROM mdl_course_categories mc WHERE mc.id IN {}".format(tuple(categoryids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')   
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response} 

    def get_user_role_get_categorynames_list(self,userid,rolename):
        '''
        '''
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            rolename='manager'
            sqlQr="SELECT mctx.instanceid AS categoryid FROM mdl_role_assignments mra INNER JOIN mdl_role mr ON mr.id=mra.roleid INNER JOIN mdl_context mctx ON mctx.id=mra.contextid WHERE mra.userid={} AND mr.shortname='{}' AND mctx.contextlevel=40".format(userid,rolename)
            categoryids=read_sql(sql_text(sqlQr),con)['categoryid'].to_list()
            sqlQ="SELECT mc.name AS label, mc.id AS value FROM mdl_course_categories mc WHERE mc.id IN {}".format(tuple(categoryids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')   
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}               
###########################################################
#### Course/Module creation/Edit functions ######################
###########################################################
    def change_edit_mode(self, editmode, userid, contextlevel, instanceid, editrole):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            if contextlevel==40:
                contextid=self.get_category_contextid(instanceid,contextlevel)['response']
            elif contextlevel==50:
                contextid=self.get_course_contextid(instanceid,contextlevel)['response']
            elif contextlevel==70:
                contextid=self.get_module_contextid(instanceid,contextlevel)['response']
            else:
                contextid=[]
            if contextid!=[]:
                roleids=self.get_context_user_roleids(userid,contextid)['response']
                print(roleids)
                roleIDs=', '.join([str(zz) for zz in roleids])
                contextroles=read_sql(sql_text("SELECT shortname FROM mdl_role WHERE id IN ({})".format(roleIDs)),con)['shortname'].to_list()
                if editrole in contextroles:
                   response=self.call(self.mWAP,'core_change_edit_mode',setmode=editmode,contextid=contextid) 
            else:
                response=[]
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}

    def create_courses(self,datadicts):
        ''' courses-> List of
        {fullname:"fullname",shortname:"shortname", categoryid:0,
        cformat:"topics", visible:1, showgrades:1, showreports:0, 
        groupmode:0, groupmodeforce:0, defaultgroupingid:0, 
        enablecompletion:1, completionnotify:1,
        startdate:0,enddate:0}
        fullname, shortname, categoryid - required
        '''
        course={"fullname":"fullname",
                "shortname":"shortname", 
                "categoryid":0,
                "format":"topics", #course format: weeks, topics, social, site,..
                "summary":"",
                "showgrades":0, 
                "startdate":0,
                "enddate":0,
                "showreports":0,
                "visible":1,
                "groupmode":0,
                "groupmodeforce":0,
                "defaultgroupingid":0,
                "enablecompletion":1,
                "completionnotify":1}
        response=datadicts
        timeCols={"startdate","enddate"}
        tempDicts=[]
        for dct in datadicts:
            cols2change=list(set([*dct]).intersection(timeCols))
            if len(cols2change)!=0:
                for zz in cols2change:
                    try:
                        dct[zz]=int(time.mktime(to_datetime(dct[zz], errors='ignore', dayfirst=True).to_pydatetime().timetuple()))
                    except:
                        dct.pop(zz)
            tempDicts+=[dct]            
        courses=[]
        for dct in tempDicts:
            tmp=copy.deepcopy(course)
            for ky in [*dct]:
                tmp[ky]=dct[ky]
            courses+=[tmp]

        response=courses
        status="error"
        try:
            response=self.call(self.mWAP,'core_course_create_courses',courses=courses)
            status='success'
        except:
            pass
        return {'status':status, 'response':response}

    def create_course(self,categoryid,fullname,shortname,cformat="topics",visible=1,showgrades=1,startdate=0,enddate=0,
                        showreports=0,groupmode=0,groupmodeforce=0,defaultgroupingid=0,enablecompletion=1,completionnotify=1):  
        response=[]
        status="error"
        try:
            courses=[{"fullname":fullname,
                        "shortname":shortname, 
                        "categoryid":categoryid,
                        "format":cformat, #course format: weeks, topics, social, site,..
                        "showgrades":showgrades, 
                        "startdate":startdate,
                        "enddate":enddate,
                        "showreports":showreports,
                        "visible":visible,
                        "groupmode":groupmode,
                        "groupmodeforce":groupmodeforce,
                        "defaultgroupingid":defaultgroupingid,
                        "enablecompletion":enablecompletion,
                        "completionnotify":completionnotify}
                    ]
            response=courses         
            response=self.call(self.mWAP,'core_course_create_courses',courses=courses)
            status='success'
        except:
            pass
        return {'status':status, 'response':response}

    def create_course_4m_moodle_template(self,siteurl,courseinfodict):  
        '''
        Webserice call: {"courseinfodict":{"templatename":<template shortname>,"categoryid":<Category ID>,"shortname":<Course short name>,"fullname":<Course full name>},"startdate":<start time str>,"enddate":<end time str>,}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            webserviceAccessParams=self.mWAP
            output={}
            templateShortName=courseinfodict['templatename']
            categoryid=courseinfodict['categoryid']
            #customFields=customfields #params['customfields']
            templateContentDict=[crs for crs in self.call(webserviceAccessParams,'core_course_search_courses',criterianame='search',criteriavalue=templateShortName)['courses'] if crs['shortname']==templateShortName][0]
            templateCourseID=templateContentDict['id']
            course2AddDict=self.call(webserviceAccessParams,'core_course_get_courses',options={'ids':[templateCourseID]})[0]
            for ky in ['id','categorysortorder','displayname','showactivitydates','showcompletionconditions','timecreated','timemodified']: #,'lang']:
                try:
                    del course2AddDict[ky]
                except:
                    status='No {} in keys'.format(ky)

            course2AddDict['shortname']=courseinfodict['shortname']
            course2AddDict['fullname']=courseinfodict['fullname']
            course2AddDict['categoryid']=categoryid
            course2AddDict['startdate']=int(time.mktime(to_datetime([courseinfodict['startdate']], errors='raise', dayfirst=True,infer_datetime_format=True).to_pydatetime()[0].timetuple()))
            course2AddDict['enddate']=int(time.mktime(to_datetime([courseinfodict['enddate']], errors='raise', dayfirst=True,infer_datetime_format=True).to_pydatetime()[0].timetuple()))
            course2AddDict['lang']='en'
            if 'customfields' in [*course2AddDict]:
                course2AddDict['customfields']=[{ky:course2AddDict['customfields'][0][ky] for ky in ['shortname','value']}]
            
            reponse=self.call(webserviceAccessParams,'core_course_create_courses',courses=[course2AddDict])
            #reponse=self.call(webserviceAccessParams,'core_course_duplicate_course',courseid=templateCourseID,fullname=courseinfodict['fullname'],shortname=courseinfodict['shortname'],categoryid=categoryID,visible=1,options=[{'name':'role_assignments','value':1}])

            createdCrsId=reponse[0]['id']
            output['courseid']=createdCrsId
            self.call(webserviceAccessParams,'core_course_import_course',importfrom=templateCourseID, importto=createdCrsId)
            output['courseurl']=siteurl+'/course/view.php?id={}'.format(createdCrsId)
            status='success'
            response=output
        except:
            pass
        return {'status':status, 'response':response}

    def create_course_sections_in_course(self,courseid,datadicts):
        response=[]
        status="error"
        sectionsdatadicts=[]
        for dct in datadicts:
            dct['courseid']=courseid
            sectionsdatadicts+=[dct]
        response=self.create_course_sections(sectionsdatadicts)['response']  
        return {'status':status,'response':response}

    def create_course_sections(self,datadicts):
        '''
        Webserice call: {"courseid":<Course id>, "sectionname":<section name>, "sectionnumber":<section number>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        courseids=list(set([dct['courseid'] for dct in datadicts]))
        for courseid in courseids:
            sections=[]
            courseSecnDataDicts=[dct for dct in datadicts if dct['courseid']==courseid]
            parameters={"courseid":courseid,"position":0,"number":len(courseSecnDataDicts)}
            try:
                createdsections=self.call(self.mWAP,'local_wsmanagesections_create_sections',**parameters)
                if len(createdsections)!=0:
                    for iscn,csecn in enumerate(courseSecnDataDicts):
                        sections+=[{"type":"id","section":createdsections[iscn]['sectionid'],"name":csecn['sectionname'],"visible":1}]
                        response+=[{"courseid":courseid,'sectionid':createdsections[iscn]['sectionid'],"name":csecn['sectionname']}]
                    params={"courseid":courseid,"sections":sections}
                    print(params)
                    response2=self.call(self.mWAP,'local_wsmanagesections_update_sections',**params)
                #response+=[{"courseid":courseid,'sectionid':zz['sectionid'],'sectionnumber':zz['sectionnumber']} for zz in createdsections]
                status='success'
            except:
                pass
        return {'status':status,'response':response}

    def create_course_section(self,courseid,sectionname,sectionnumber):
        '''
        Webserice call: {"courseid":<Course id>, "sectionname":<section name>, "sectionnumber":<section number>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        parameters={"courseid":courseid,"position":sectionnumber,"number":1}
        try:
            response=self.call(self.mWAP,'local_wsmanagesections_create_sections',**parameters)
            print(response)
            if len(response)!=0:
                sections=[{"type":"num","section":response[0]['sectionnumber'],"name":sectionname,"visible":1}]
                params={"courseid":courseid,"sections":sections}
                print(params)
                response2=self.call(self.mWAP,'local_wsmanagesections_update_sections',**params)
                print(response)
                status='success'
        except:
            pass
        return {'status':status,'response':response}

    def update_course_section(self,courseid,sectioninfo):
        '''
        Webserice call: {"courseid":<Course id>, "sectioninfo":{"type":"id","section":<sectionid>,"name":<sectionname>,"visible":<visible>}}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        #try:
        params={"courseid":courseid,"sections":[sectioninfo]}
        response=self.call(self.mWAP,'local_wsmanagesections_update_sections',**params)
        print(response)
        status='success'
        #except:
        #    pass

        return {'status':status,'response':response}

    def update_course_sections(self,datadicts):
        '''
        Webserice call: datadicts=[{"courseid":<Course id>,"section":<sectionid>,"name":<sectionname>,"visible":<visible>}]
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        courseids=list(set([dct['courseid'] for dct in datadicts]))
    
        temp=[]
        for courseid in courseids:
            temp+=[{'courseid':courseid,'sections':[{'type':'id','section':dct['sectionid'],'name':dct['name'],'visible':dct['visible']} for dct in datadicts if dct['courseid']==courseid]}]
        
        for params in temp:
            response+=[self.call(self.mWAP,'local_wsmanagesections_update_sections',**params)]
        print(response)
        status='success'

        return {'status':status,'response':response}              

    def delete_courses(self,courseids):
        '''
        Webserice call: {"coursenames":<[list of course ids]>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        #courseDicts=[]
        courseIDs=[]
        try:
            response=self.call(self.mWAP,'core_course_delete_courses',courseids=courseids)
            status='success'
        except:
            pass

        return {'status':status, 'response':response}

    def delete_sections(self,courseid,sectionids):
        response=[]
        status='error'
        parameters={"courseid":courseid,"sectionids":sectionids}
        try:
            response=self.call(self.mWAP,'local_wsmanagesections_delete_sections',**parameters)
            status='success'
        except:
            pass

        return {'status':status, 'response':response}

    def delete_modules(self,moduleids):
        response=[]
        status='error'
        #courseDicts=[]
        courseIDs=[]
        try:
            response=self.call(self.mWAP,'core_course_delete_modules',cmids=moduleids)
            status='success'
        except:
            pass

        return {'status':status, 'response':response}

    def duplicate_course(self,courseid,categoryid,shortname,fullname):  
        '''
        Webserice call: {"courseid":<courseid>,"categoryid":<Category ID>,"shortname":<Course short name>,"fullname":<Course full name>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            output={}
            courseinfodict={"courseid":courseid,"categoryid":categoryid,"fullname":fullname,"shortname":shortname}    
            print(courseinfodict)
            courseinfo=self.call(self.mWAP,'core_course_duplicate_course',**courseinfodict)
            #output['courseurl']=siteurl+'/course/view.php?id={}'.format(courseinfo['id'])
            status='success'
            response=courseinfo
        except:
            pass
        return {'status':status, 'response':response}

    def edit_course_section_visibility(self,parameters):
        '''
        Webserice call: {"action":<one of hide/show/stealth/duplicate/edit>, "id":<section id>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        #kwargs=parameters #{'action':action,'id':sectionid}
        try:
            print(parameters)
            response=self.call(self.mWAP,'core_course_edit_section',**parameters)
            print(response)
            status='success'
        except:
            pass

        return {'status':status,'response':response}

    def duplicate_module(self,sectionreturn,moduleid):
        '''
        Webserice call: {"action":<one of hide/show/stealth/duplicate/edit>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_course_edit_module',action='duplicate',id=moduleid, sectionreturn=sectionreturn)
            status='success'
        except:
            pass

        return {'status':status,'response':response}    
        
    def edit_module_visibility(self,action,moduleid):
        '''
        Webserice call: {"action":<one of hide/show/stealth/duplicate/edit>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_course_edit_module',action=action,id=moduleid)
            status='success'
        except:
            pass

        return {'status':status,'response':response}

    def get_category_contextid(self,categoryid,contextlevel):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT id FROM mdl_context WHERE contextlevel = {} AND instanceid = (SELECT id FROM mdl_course_categories WHERE id = {})".format(contextlevel,categoryid)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0]["id"]
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}    

    def get_category_info(self):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mcc.name, mcc.parent, mcc.idnumber, mcc.description FROM mdl_course_categories mcc"
            df=read_sql(sql_text(sqlQ),con)
            df['description']=df['description'].str.replace(r'<[^<>]*>', '', regex=True)
            response=df.to_dict(orient='records')
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_category_course_info(self,categoryids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mc.shortname, mc.fullname, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course mc WHERE mc.category IN {}".format(tuple(categoryids+[-1]))
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            response=df.to_dict(orient='records')
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_course_sections_info(self,courseids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            #sqlQ="SELECT mcs.name FROM mdl_course_sections mcs WHERE mcs.course={}".format(courseid)
            sqlQ="SELECT mcc.id AS categoryid, mc.id AS courseid, mcs.id AS sectionid, mcc.name AS categoryname, mcs.summary, mcs.name AS sectionname, mc.fullname AS coursename, mc.startdate AS coursestartdate, mc.enddate AS courseenddate FROM mdl_course_sections mcs INNER JOIN mdl_course mc ON mc.id=mcs.course INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category WHERE mcs.course IN {}".format(tuple(courseids+[0]))
            df=read_sql(sql_text(sqlQ),con)
            df['coursestartdate'] = to_datetime(df['coursestartdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['courseenddate'] = to_datetime(df['courseenddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            response=df.to_dict(orient='records')
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_roles_all_courses(self,siteURL,roleids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mc.visible, mr.shortname AS rolename, mc.startdate, mc.enddate, mu.email AS user, mra.userid, mctx.id AS contextid, mc.id AS courseid, mc.category AS categoryid, mc.fullname, mcc.name AS categoryname FROM mdl_course mc INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_context mctx ON mctx.instanceid=mc.id AND mctx.contextlevel=50 INNER JOIN mdl_role_assignments mra ON mra.contextid=mctx.id INNER JOIN mdl_role mr ON mr.id=mra.roleid AND mr.id IN {} INNER JOIN mdl_user mu ON mu.id=mra.userid".format(tuple(roleids+[0]))
            df=read_sql(sql_text(sqlQ),con)
            df['startdate'] = to_datetime(df['startdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
            df['enddate'] = to_datetime(df['enddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')     
            df['url']=[siteURL+'course/view.php?id={}'.format(cid) for cid in df['courseid'].to_list()]
            response=df.to_dict(orient='records')
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response}        

    def get_category_course_full_information(self, categoryid):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            courses=self.call(self.mWAP,'core_course_get_courses_by_field',field='category',value=str(categoryid))['courses'] 
            if len(courses)!=0:
                coloumnNames=['shortname','fullname','summary','startdate','enddate'] #'categoryname',
                if 'customfields' in [*courses[0]]:
                    coloumnNames=coloumnNames+['customfields']
                df=DataFrame([{ky:crs[ky] for ky in coloumnNames} for crs in courses])
                df['startdate'] = to_datetime(df['startdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
                df['enddate'] = to_datetime(df['enddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
                #df['summary'] = df['summary'].str.replace(r'<[^<>]*>', '', regex=True)
                response=df.to_dict(orient='records')
                if 'customfields' in df.columns:
                    temp=[]
                    for crs in response:
                        for dct in crs['customfields']:
                            if dct['type'] in ['textarea','text']:
                                value=re.sub('<[^<]+?>', '', dct['valueraw'])
                            if dct['type']=='select':
                                value=dct['value']
                            elif dct['type']=='checkbox':
                                value=dct['value']
                            elif dct['type']=='date':
                                value=to_datetime(dct['valueraw'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').strftime('%Y-%m-%d %X')
                            else:
                                value=''
                            #crs.update({dct['name']: for dct in crs['customfields']})
                            crs.update({dct['name']:value})
                        crs.pop('customfields')
                        temp+=[crs]
                    response=temp
                status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_categories_course_full_information(self, categoryids):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        for categoryid in categoryids:
            try:
                courses=self.call(self.mWAP,'core_course_get_courses_by_field',field='category',value=str(categoryid))['courses'] 
                if len(courses)!=0:
                    coloumnNames=['categoryname','shortname','fullname','summary','startdate','enddate'] #
                    if 'customfields' in [*courses[0]]:
                        coloumnNames=coloumnNames+['customfields']
                    df=DataFrame([{ky:crs[ky] for ky in coloumnNames} for crs in courses])
                    df['startdate'] = to_datetime(df['startdate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
                    df['enddate'] = to_datetime(df['enddate'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%Y-%m-%d %X')
                    #df['summary'] = df['summary'].str.replace(r'<[^<>]*>', '', regex=True)
                    response+=df.to_dict(orient='records')
                status='success'
            except:
                pass
        if len(response)!=0:
            if 'customfields' in [*response[0]]:
                temp=[]
                for crs in response:
                    for dct in crs['customfields']:
                        if dct['type'] in ['textarea','text']:
                            value=re.sub('<[^<]+?>', '', dct['valueraw'])
                        if dct['type']=='select':
                            value=dct['value']
                        elif dct['type']=='checkbox':
                            value=dct['value']
                        elif dct['type']=='date':
                            value=to_datetime(dct['valueraw'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').strftime('%Y-%m-%d %X')
                        else:
                            value=''
                        #crs.update({dct['name']: for dct in crs['customfields']})
                        crs.update({dct['shortname']:value})
                    crs.pop('customfields')
                    temp+=[crs]
                response=temp           
            

        return {'status':status,'response':response}

    def get_category_course_list(self, categoryid,visible=1):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        dropdownlist=[]
        status="error"
        try:
            categoryContentListPDF=DataFrame(self.call(self.mWAP,'core_course_get_courses_by_field',field='category',value=str(categoryid))['courses']) #New 11/12/2022
            categoryInfo=[{'id':crs['id'],'shortname':crs['shortname']} for crs in categoryContentListPDF.to_dict(orient='records') if crs['visible']==visible]
            print(categoryInfo)
            if len(categoryInfo)!=0:
                labelNames=[dct['shortname'] for dct in categoryInfo]
                #labelNames.sort()
                dropdownlist=[{'label':lbl,'value':dct['id']} for lbl in labelNames for dct in categoryInfo  if dct['shortname']==lbl]
                status='success'
            else:
                dropdownlist=[]
        except:
            pass
        #dropdownlist=response.text
        print(dropdownlist)
        return {'status':status,'response':dropdownlist}

    def get_categories_course_list(self, categoryids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mc.id, mc.shortname FROM mdl_course_categories mcc INNER JOIN mdl_course mc ON mcc.id=mc.category WHERE mc.category IN {}".format(tuple(categoryids+[0]))
            courses=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            labelNames=[dct['shortname'] for dct in courses]
            dropdownlist=[{'label':lbl,'value':dct['id']} for lbl in labelNames for dct in courses  if dct['shortname']==lbl]
            status='success'
        except:
            pass
        con.close() 
        return {'status':status,'response':dropdownlist}

    def get_context_user_roleids(self,userid,contextid):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT ra.roleid FROM mdl_role_assignments ra INNER JOIN  mdl_context ctx ON ra.contextid = ctx.id WHERE ra.userid = {} AND ctx.id = {}".format(userid,contextid)
            roleids=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'
            if len(roleids)==0:
                status='User '+str(userid)+' not assigned in context '+str(contextid)
                response=[]
            else:
                response=[rl['roleid'] for rl in roleids]
            status='success'
        except:
            pass
        con.close()            
        return {'status':status,'response':response}

    def get_context_all_users_and_roles(self, contextlevel, instanceid):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT ra.userid AS userid, ra.roleid, r.shortname FROM mdl_role_assignments ra INNER JOIN mdl_role r ON r.id = ra.roleid INNER JOIN mdl_context mctx ON ra.contextid = mctx.id WHERE mctx.contextlevel={} AND mctx.instanceid={}".format(contextlevel,instanceid)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records') 
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_context_user_roles(self, userid, contextlevel, instanceid):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT ra.roleid, r.shortname FROM mdl_role_assignments ra INNER JOIN mdl_role r ON r.id = ra.roleid INNER JOIN mdl_context mctx ON ra.contextid = mctx.id WHERE mctx.contextlevel={} AND mctx.instanceid={} AND ra.userid={}".format(contextlevel,instanceid,userid)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records') 
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response}

    def get_user_role_context_get_instances(self, userid,rolename,contextlevel):
        '''
        '''
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT mr.shortname AS rolename, mra.contextid, mctx.contextlevel, mctx.instanceid FROM mdl_role_assignments mra INNER JOIN mdl_role mr ON mr.id=mra.roleid INNER JOIN mdl_context mctx ON mctx.id=mra.contextid WHERE mra.userid={} AND mr.shortname='{}' AND mctx.contextlevel={}".format(userid,rolename,contextlevel)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')   
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}


    def get_user_roles(self, userid):
        '''
        '''
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT mr.shortname AS rolename, mra.contextid, mctx.contextlevel, mctx.instanceid FROM mdl_role_assignments mra INNER JOIN mdl_role mr ON mr.id=mra.roleid INNER JOIN mdl_context mctx ON mctx.id=mra.contextid WHERE mra.userid={}".format(userid)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')   
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}

    def get_context_user_inherited_roles(self, userid, contextdicts):
        '''
        contextdicts=[{'contextlevel':'<>','instanceid':}]
        '''
        response=[]
        status='error'
        contextlevels=[dct['contextlevel'] for dct in contextdicts]
        instanceids=[dct['instanceid'] for dct in contextdicts]
        roles=[]
        try:
            self.engine.dispose()
            con=self.engine.connect()
            for ic,contextlevel in enumerate(contextlevels):
                if contextlevel==10:
                    sqlQ="SELECT r.id, r.shortname FROM mdl_user u JOIN mdl_role_assignments ra ON ra.userid = u.id JOIN mdl_role r ON r.id = ra.roleid WHERE u.id = {} AND ra.contextid = (SELECT id FROM mdl_context WHERE contextlevel = {})".format(userid,contextlevel)
                    roles+=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    contextiddicts=[]
                    #print(roles)
                elif contextlevel==40:
                    sqlQ="SELECT id FROM mdl_context WHERE contextlevel = {} AND instanceid = {}".format(contextlevel,instanceids[ic])
                    contextiddicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    #contextid=self.get_category_contextid(instanceids[ic],contextlevel)['response']
                elif contextlevel==50:
                    sqlQ="SELECT id FROM mdl_context WHERE contextlevel = {} AND instanceid = {}".format(contextlevel,instanceids[ic])
                    contextiddicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    #contextid=self.get_course_contextid(instanceids[ic],contextlevel)['response']
                elif contextlevel==70:
                    sqlQ="SELECT id FROM mdl_context WHERE contextlevel = {} AND instanceid = {}".format(contextlevel,instanceids[ic])
                    contextiddicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                    #contextid=self.get_module_contextid(instanceids[ic],contextlevel)['response']
                else:
                    contextiddicts=[]
                print(contextiddicts)    
                if contextiddicts!=[]:
                    contextid=contextiddicts[0]['id']
                    roleids=self.get_context_user_roleids(userid,contextid)['response']
                    #print(roleids)
                    roleIDs=', '.join([str(zz) for zz in roleids])
                    if len(roleids)!=0:
                       roles+=read_sql(sql_text("SELECT id, shortname FROM mdl_role WHERE id IN ({})".format(roleIDs)),con).to_dict(orient='records')
                    #print(roles)
                else:
                    pass
            response=[zz for iz,zz in enumerate(roles) if zz not in roles[iz+1:]]    
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}
    
    def get_course_contextid(self,courseid,contextlevel):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT id FROM mdl_context WHERE contextlevel = {} AND instanceid = (SELECT id FROM mdl_course WHERE id = {})".format(contextlevel,courseid)
            #print(sqlQ)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0]["id"]
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}    

    def get_course_full_info(self, courseid):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        print(response)
        try:
            response=self.call(self.mWAP,'core_course_get_contents',courseid=courseid)
            if len(secnInfo)!=0:
                status='status'
            else:
                pass
        except:
            pass
        return {'status':status,'response':response}        

    def get_course_modules(self,courseid,modvisible=1,secnvisible=1):
        '''
        Webserice call: {"courseid":<Course ID>, "modvisible"=<1 or 0>, "secnvisible"=<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        try:
            response=[{'sectionid':secn['id'], 'sectionname':secn['name'],'sectionmodules':[{'id':mod['id'], 'name':mod['name'], 'modname':mod['modname'],'contextid':mod['contextid'],'instance':mod['instance'],'url':mod['url']} for mod in secn['modules'] if mod['visible']==modvisible]} for secn in self.call(self.mWAP,'core_course_get_contents',courseid=courseid) if secn['visible']==secnvisible] 
            status='success'
        except:
            response=[]
            status='error'

        return {'status':status,'response':response}

    def get_course_users_complete_info(self,courseid):
        '''
        Webserice call: {"courseid":<Course ID>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_enrol_get_enrolled_users',courseid=courseid)
            status='success'
        except:
            pass

        return {'status':status,'response':response}

    def get_course_users(self,courseid):
        '''
        Webserice call: {"courseid":<Course ID>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            courseUsers=self.call(self.mWAP,'core_enrol_get_enrolled_users',courseid=courseid)
            if len(courseUsers)!=0:
                labelNames=[dct['username'] for dct in courseUsers]
                labelNames.sort()
                response=[{'id':dct['id'],'firstname':lbl, 'username':dct['username'], 'fullname':dct['fullname'], 'roles':dct['roles']} for lbl in labelNames for dct in courseUsers  if dct['username']==lbl]
                status='success'
        except:
            pass

        return {'status':status,'response':response}        

    def get_course_users_list(self,courseid):
        '''
        Webserice call: {"courseid":<Course ID>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        courseUsers=self.get_course_users(courseid)['response']
        if len(courseUsers)!=0:
            labelNames=[dct['username'] for dct in courseUsers]
            labelNames.sort()
            response=[{'label':dct['fullname'],'value':dct['id']} for lbl in labelNames for dct in courseUsers  if dct['username']==lbl]
            status='success'
        return {'status':status,'response':response}        

    def get_courses_users(self,courseids):
        '''
        Webserice call: {"courseid":<Course ID>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            for courseid in courseids:
                courseUsers=self.call(self.mWAP,'core_enrol_get_enrolled_users',courseid=courseid)
                if len(courseUsers)!=0:
                    labelNames=[dct['username'] for dct in courseUsers]
                    labelNames.sort()
                    response+=[{'courseid':courseid,'id':dct['id'],'firstname':lbl, 'username':dct['username'], 'fullname':dct['fullname'], 'roles':dct['roles']} for lbl in labelNames for dct in courseUsers  if dct['username']==lbl]
                    status='success'
        except:
            pass

        return {'status':status,'response':response}  

    def get_courses_users_list(self,courseids):
        '''
        Webserice call: {"courseid":<Course ID>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        courseUsersPDF=DataFrame(self.get_courses_users(courseids)['response'])
        if len(courseUsersPDF)!=0:
            labelNames=list(set(courseUsersPDF['username'].to_list()))
            labelNames.sort()
            for lbl in labelNames:
                dct=courseUsersPDF[courseUsersPDF['username']==lbl].to_dict(orient='records')[0]
                response+=[{'label':dct['fullname'],'value':dct['id']}]
            status='success'
        return {'status':status,'response':response}

    def get_course_section_from_section_id(self,sectionid):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT section, course FROM mdl_course_sections WHERE id ={}".format(sectionid)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0] #["section"]
            status='success'
        except:
            pass 

        con.close()
        return {'status':status,'response':response}    

    def get_course_sections_list(self, courseid, secnvisible=1):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        dropdownlist=[]
        status="error"
        try:
            secnInfo=response=[{'sectionid':secn['id'], 'sectionname':secn['name']} for secn in self.call(self.mWAP,'core_course_get_contents',courseid=courseid) if secn['visible']==secnvisible]             
            if len(secnInfo)!=0:
                labelNames=[secn['sectionname'] for secn in secnInfo]
                #labelNames.sort()
                dropdownlist=[{'label':lbl,'value':dct['sectionid']} for lbl in labelNames for dct in secnInfo  if dct['sectionname']==lbl]
                status='status'
            else:
                pass
        except:
            pass
        response=dropdownlist
        return {'status':status,'response':response}

    def get_courses_sections_list(self, courseids, secnvisible=1):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        dropdownlist=[]
        status="error"
        secnInfo=[]
        for courseid in courseids:
            try:
                secnInfo+=[{'sectionid':secn['id'], 'sectionname':secn['name']} for secn in self.call(self.mWAP,'core_course_get_contents',courseid=courseid) if secn['visible']==secnvisible]             
            except:
                pass
            
        if len(secnInfo)!=0:
            labelNames=[secn['sectionname'] for secn in secnInfo]
            #labelNames.sort()
            dropdownlist=[{'label':lbl,'value':dct['sectionid']} for lbl in labelNames for dct in secnInfo  if dct['sectionname']==lbl]
            status='status'
        else:
            pass
    
        response=dropdownlist
        return {'status':status,'response':response}        
      
    def get_course_section_modules(self, courseid, sectionid):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        secnModules=[]
        status="error"
        try:
            parameters={"courseid":courseid, "options":[{"name":"sectionid", "value":sectionid}]}
            secnInfo=self.call(self.mWAP,'core_course_get_contents',**parameters)
            #secnInfo=[{'sectionid':secn['id'], 'sectionname':secn['name'],'sectionmodules':[{'id':mod['id'], 'name':mod['name'], 'modname':mod['modname'],'contextid':mod['contextid'],'instance':mod['instance'],'url':mod['url']} for mod in secn['modules']]} for secn in self.call(self.mWAP,'core_course_get_contents',courseid=courseid) if secn['id']==sectionid] 
            #secnInfo=[{'sectionid':secn['id'], 'sectionname':secn['name'],'sectionmodules':[{'id':mod['id'], 'name':mod['name'], 'modname':mod['modname'],'contextid':mod['contextid'],'instance':mod['instance'],'url':mod['url']} for mod in secn['modules'] if mod['visible']==modvisible]} for secn in self.call(self.mWAP,'core_course_get_contents',courseid=courseid) if ((secn['id']==sectionid) & (secn['visible']==secnvisible))] 
            if len(secnInfo)!=0:
                secnModules=secnInfo[0]['modules']
                status='success'
            else:
                pass
        except:
            pass
        return {'status':status,'response':secnModules}        

    def get_course_section_modules_list(self, courseid, sectionid, secnvisible=1, modvisible=1):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        dropdownlist=[]
        status="error"
        try:
            secnInfo=[{'sectionid':secn['id'], 'sectionname':secn['name'],'sectionmodules':[{'id':mod['id'], 'name':mod['name'], 'modname':mod['modname'],'contextid':mod['contextid'],'instance':mod['instance'],'url':mod['url']} for mod in secn['modules'] if mod['visible']==modvisible]} for secn in self.call(self.mWAP,'core_course_get_contents',courseid=courseid) if ((secn['id']==sectionid) & (secn['visible']==secnvisible))] 
            if len(secnInfo)!=0:
                secnModules=secnInfo[0]['sectionmodules']
                print(secnModules)
                if len(secnModules)!=0:
                    labelNames=[mod['name'] for mod in secnModules]
                    #labelNames.sort()
                    dropdownlist=[{'label':lbl,'value':dct['id']} for lbl in labelNames for dct in secnModules  if dct['name']==lbl]
                    print(dropdownlist)
                    status='success'
                else:
                    dropdownlist=[]
                    status='no such modules'
            else:
                pass
        except:
            pass
        #print(secnModules)
        print(dropdownlist)
        #secnModules=response.text
        return {'status':status,'response':dropdownlist}

    def get_courses_sections_modules_list(self, courseids, sectionids, secnvisible=1, modvisible=1):
        '''
        Webserice call: {"categoryid":<Category ID>,"visible":<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        dropdownlist=[]
        status="error"
        secnModules=[]
        for courseid in courseids:
            for sectionid in sectionids:
                try:
                    secnInfo=[{'sectionid':secn['id'], 'sectionname':secn['name'],'sectionmodules':[{'id':mod['id'], 'name':mod['name'], 'modname':mod['modname'],'contextid':mod['contextid'],'instance':mod['instance'],'url':mod['url']} for mod in secn['modules'] if mod['visible']==modvisible]} for secn in self.call(self.mWAP,'core_course_get_contents',courseid=courseid) if ((secn['id']==sectionid) & (secn['visible']==secnvisible))] 
                    if len(secnInfo)!=0:
                        secnModules+=secnInfo[0]['sectionmodules']
                    else:
                        pass
                except:
                    pass
        if len(secnModules)!=0:
            labelNames=[mod['name'] for mod in secnModules]
            #labelNames.sort()
            dropdownlist=[{'label':lbl,'value':dct['id']} for lbl in labelNames for dct in secnModules  if dct['name']==lbl]
            status='success'
        else:
            dropdownlist=[]
            status='no such modules'
        return {'status':status,'response':dropdownlist}        

    def get_course_module_by_id(self,moduleid):
        '''
        Webserice call: {"action":<one of hide/show/stealth/duplicate/edit>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            output=self.call(self.mWAP,'core_course_get_course_module',cmid=moduleid)
            response=output['cm']
            status='success'
        except:
            pass

        return {'status':status,'response':[response]}

    def get_modules_contextids(self,moduleids):
        response=[]
        status='error'
        contextlevel=70
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT id AS contextid, instanceid AS moduleid FROM mdl_context WHERE contextlevel = {} AND instanceid IN {}".format(contextlevel,tuple(moduleids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response} 

    def get_module_contextid(self,moduleid,contextlevel):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT id FROM mdl_context WHERE contextlevel = {} AND instanceid = {}".format(contextlevel,moduleid)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0]["id"]
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}    

    def get_module_full_info_by_id(self,moduleid):
        response=[]
        status='error'
        try:
            modinfo=self.get_course_module_by_id(moduleid)['response']
            print(modinfo)
            response=[mod for mod in self.get_course_section_modules(modinfo['course'], modinfo['section'])['response'] if mod['id']==moduleid][0]
            status='success'
        except:
            pass
        return {'status':status,'response':response}   

    def get_module_section_in_course(self,moduleid):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT s.section FROM mdl_course_sections s JOIN mdl_course_modules m ON m.section = s.id WHERE m.id ={}".format(moduleid)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0]["section"]
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}    

    def get_user_contextid(self,userid,contextlevel):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ="SELECT ctx.id FROM mdl_context ctx INNER JOIN mdl_role_assignments ra ON ra.contextid = ctx.id INNER JOIN mdl_user u ON u.id = ra.userid WHERE u.id = {} AND ctx.contextlevel = {}".format(userid,contextlevel)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}
    
    def get_user_capabilities(self,userid, contextlevel, instanceid):
        '''
        Webserice call: {"userid":<Logged in user userid>, "hidden"=<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        try:
            response+=self.get_context_user_rolenames(userid, contextlevel, instanceid)['response']
            response+=self.get_system_user_rolenames(userid)['response']
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_user_courses(self,userid, hidden):
        '''
        Webserice call: {"userid":<Logged in user userid>, "hidden"=<1 or 0>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        try:
            usersDict=self.call(self.mWAP,'core_user_get_users',criteria=[{'key':'id','value':userid}])
            if not usersDict['users'][0]['suspended']:
                response=[{'value':crs['id'],'label':crs['shortname']} for crs in self.call(self.mWAP,'core_enrol_get_users_courses', userid=userid) if crs['hidden']==hidden]
                status='success'
            else:
                response=[]
                status='user suspended'
        except:
            pass
        return {'status':status,'response':response}

    def get_system_user_rolenames(self, userid):
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            response=read_sql(sql_text("SELECT r.id, r.shortname FROM mdl_user u JOIN mdl_role_assignments ra ON ra.userid = u.id JOIN mdl_role r ON r.id = ra.roleid WHERE u.id = {} AND ra.contextid = (SELECT id FROM mdl_context WHERE contextlevel = 10)".format(userid)),con).to_dict(orient='records')
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}

    def move_course_section(self,courseid,sectionid,position):
        '''
        Webserice call: {"courseid":<Course id>, "sectioninfo":{"type":"id","section":<sectionid>,"name":<sectionname>,"visible":<visible>}}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            self.engine.dispose()
            con=self.engine.connect()
            sectionnumber=read_sql(sql_text("SELECT section FROM mdl_course_sections WHERE id={}".format(sectionid)),con).to_dict(orient='records')[0]['section']
            params={"courseid":courseid,"sectionnumber":sectionnumber,"position":position}
            response=self.call(self.mWAP,'local_wsmanagesections_move_section',**params)
            print(response)
            status='success'
        except:
            pass
        con.close()
        return {'status':status,'response':response} 

#######################################
##User interactions
############################################

    def get_user_course_activity_completion(self,userid,courseid):
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_completion_get_activities_completion_status',courseid=courseid,userid=userid)                    
            status='success'        
        except:
            pass

        return {'status':status,'response':response}

    def get_user_context_events(self,userid,contextlevel,edulevel,startDateStr,endDateStr):
        interactionDict={}
        response=[]
        status="error"
        startDate=to_datetime(startDateStr,dayfirst=True).to_pydatetime()
        endDate=to_datetime(endDateStr,dayfirst=True).to_pydatetime()
        start_date_UNIX=time.mktime(startDate.timetuple())
        end_date_UNIX=time.mktime(endDate.timetuple())

        parameters={"db_table_name":"mdl_logstore_standard_log","returnColumns":["*"],"filterDict":{"userid":userid},"colName":"timecreated","startVal":start_date_UNIX,"endVal":end_date_UNIX}
        userDataPDF=DataFrame(self.mgDB.get_filtered_records_between_ranges(parameters)['response'])
        if len(userDataPDF)!=0:
            studentInteraction={}# pd.DataFrame(np.zeros([1,len(columnsList)]),index=[chosenUser], columns=columnsList)
            usrwisePDF=userDataPDF.sort_values(by='timecreated').copy(deep=True)
            #print(usrwisePDF['courseid'])
            #usrwisePDF['eventname']=usrwisePDF['eventname'].str.split('\\',expand=True)[3]               
            cn=to_datetime(usrwisePDF['timecreated'], unit='s',utc=True).dt.tz_convert('Asia/Colombo').to_list()

            cp=[cn[0]]+cn[:-1]
            trr=to_datetime(cn, dayfirst=True).to_pydatetime()-to_datetime(cp, dayfirst=True).to_pydatetime()
            tru=trr.tolist()
            usrwisePDF['usrdt']=[float("{:.2f}".format((dt.seconds/60.))) for dt in tru]
            
            scInteraction={}
            cuwisePDF=usrwisePDF[(usrwisePDF['contextlevel']==contextlevel) & (usrwisePDF['edulevel']==edulevel)].copy(deep=True)
            cuwisePDF['timecreated']=to_datetime(cuwisePDF['timecreated'],unit='s',utc=True).dt.tz_convert('Asia/Colombo').dt.strftime('%d-%m-%Y %X').to_list()
            #print(cuwisePDF)
            response=cuwisePDF[["id","userid","courseid","edulevel","eventname","timecreated","contextlevel","contextid","contextinstanceid","ip","relateduserid","target","usrdt"]].to_dict(orient='records')
            status="success"

        else:
            response=[]
            status="No user activity"   
                
        return {'status':status,'response':response} #concat([aastudentPDF,DataFrame(numberofUsrActivityPDF.to_dict(orient='records'),index=[0])],axis=1)

    def get_users_modules_dedication(self, userids, moduleids):
        response=[]
        status='error'
        #sqlQ="SELECT ldc.courseid, ldc.userid, ldm.* FROM mdl_local_ld_course ldc INNER JOIN mdl_local_ld_module ldm ON ldm.ldcourseid=ldc.id WHERE ldc.userid IN {} AND ldm.coursemoduleid IN {}".format(tuple(userids+[0]),tuple(moduleids+[0]))
        #sqlQ="SELECT c.id AS contextid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score, ldc.courseid AS ldccourseid, ldc.userid, ldm.*  FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id INNER JOIN mdl_local_ld_module ldm ON c.instanceid=ldm.coursemoduleid INNER JOIN mdl_local_ld_course ldc ON ldm.ldcourseid=ldc.id WHERE c.instanceid IN {} AND ldc.userid IN {}".format(tuple(moduleids+[0]),tuple(userids+[0]))
        #sqlQ="SELECT c.id AS contextid, cm.id AS moduleid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score, ldc.userid, ldm.totaldedication, ldmd.dedication, ldmd.day, ldmd.daytime  FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id INNER JOIN mdl_local_ld_module ldm ON c.instanceid=ldm.coursemoduleid INNER JOIN mdl_local_ld_course ldc ON ldm.ldcourseid=ldc.id INNER JOIN mdl_local_ld_module_day ldmd ON ldmd.ldmoduleid=ldm.id WHERE ldm.coursemoduleid IN {} AND ldc.userid IN {} AND c.contextlevel=70".format(tuple(moduleids+[0]),tuple(userids+[0]))
        sqlQ="SELECT mctx.id AS contextid, mcm.score, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllm.coursemoduleid IN {} AND mllc.userid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel=70".format(tuple(moduleids+[0]),tuple(userids+[0]))
        self.engine.dispose()
        con=self.engine.connect()
        try:
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            status='success'
        except:
            pass
        con.close()    
        return {'status':status,'response':response}   

    def get_module_contexts_info(self,contextids):
        response=[]
        status='error'
        try:
            sqlQ="SELECT c.id AS contextid, cm.id AS moduleid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id WHERE c.id IN {} AND c.contextlevel=70".format(tuple(contextids+[0]))
            #sqlQ="SELECT c.id AS contextid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score, ldc.courseid AS ldccourseid, ldc.userid, ldm.*  FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id INNER JOIN mdl_local_ld_module ldm ON c.instanceid=ldm.coursemoduleid INNER JOIN mdl_local_ld_course ldc ON ldm.ldcourseid=ldc.id WHERE c.id IN {}".format(tuple(contextids+[0]))
            #print(sqlQ)
            self.engine.dispose()
            con=self.engine.connect()
            moduleInfoDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            if len(moduleInfoDicts)!=0:
                for dct in moduleInfoDicts:
                    sqlQ2="SELECT mm.name FROM mdl_{} mm WHERE mm.id={}".format(dct['modtype'],dct['instanceid'])
                    #print(sqlQ2)
                    modnameDict=read_sql(sql_text(sqlQ2),con).to_dict(orient='records')
                    if len(modnameDict)!=0:
                        dct['modulename']=modnameDict[0]['name']
                    else:
                        dct['modulename']=''
                    response+=[dct]
            else:
                status='context does not exist'
        except:
            pass
        
        #print(response)
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_modules_users_grades_dedications_by_courses(self,courseids):
        response=[]
        status='error'
        contextlevel=70
        self.engine.dispose()
        con=self.engine.connect()
        try:
            #sqlQ="SELECT mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mllc.courseid IN {} AND mcm.deletioninprogress=0 AND mgi.itemmodule=mm.name".format(tuple(courseids+[0]))
            #sqlQ="SELECT mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllc.courseid IN {} AND mcm.deletioninprogress=0".format(tuple(courseids+[0]))
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllc.courseid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(tuple(courseids+[0]),contextlevel)
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grademax']
            responsePDF['dedication']=responsePDF['dedication']/60.
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_modules_users_grades_dedications_by_courses_figures(self,courseids):
        response=[]
        status='error'
        contextlevel=70
        self.engine.dispose()
        con=self.engine.connect()
        try:
            #sqlQ="SELECT mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mllc.courseid IN {} AND mcm.deletioninprogress=0 AND mgi.itemmodule=mm.name".format(tuple(courseids+[0]))
            #sqlQ="SELECT mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllc.courseid IN {} AND mcm.deletioninprogress=0".format(tuple(courseids+[0]))
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllc.courseid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(tuple(courseids+[0]),contextlevel)
            outputPDF=read_sql(sql_text(sqlQ),con)
            outputPDF['attainment']=outputPDF['finalgrade']/outputPDF['grademax']
            outputPDF['dedication']=outputPDF['dedication']/60.

            outputPDF['fullname']=outputPDF['firstname']+' '+outputPDF['lastname']
            colomnnames=['day','dedication','finalgrade','grademax','itemname','fullname','modulescore','sectionname']
            df=outputPDF[colomnnames].copy()
            renamemap={'dedication':'timespent/mins'}
            df.rename(columns=renamemap,inplace=True)
            #df.round(decimals=2)
            ycol='timespent/mins'
            xcol='fullname'
            colorcol='day'
            hoverdata=['finalgrade','grademax','itemname','sectionname']
            fig=px.bar(df, y=ycol, x=xcol, color=colorcol, barmode='stack', height=400, hover_data=hoverdata)
            colorcol='itemname'
            hoverdata=['finalgrade','grademax','day','sectionname']
            fig2=px.bar(df, y=ycol, x=xcol, color=colorcol, barmode='stack', height=400, hover_data=hoverdata)
            response={"figures":[fig.to_json(),fig2.to_json()],"data":df.to_dict(orient='records')}
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_modules_users_grades_dedications_competencies(self):
        response=[]
        status='error'
        contextlevel=70
        self.engine.dispose()
        con=self.engine.connect()
        try:
            #sqlQ="SELECT mcm.score AS modulescore, mcompf.shortname AS competencyframework, mcomp.idnumber AS competencylabel, mcomp.shortname AS competencyname, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_competency_modulecomp mcompm ON mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mcm.deletioninprogress=0" # AND mcomp.competencyframeworkid IN ()".format(frameworkids+[0])
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mcompf.shortname AS competencyframework, mcomp.idnumber AS competencylabel, mcomp.shortname AS competencyname, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_competency_modulecomp mcompm ON mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(contextlevel) # AND mcomp.competencyframeworkid IN ()".format(frameworkids+[0])
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grademax']
            responsePDF['dedication']=responsePDF['dedication']/60.
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}                 

    def get_modules_users_dedications_by_courses(self,courseids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        contextlevel=70
        try:
            #sqlQ="SELECT mcm.score AS modulescore, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance WHERE mgi.itemmodule=mm.name AND mllc.courseid IN {} AND mcm.deletioninprogress=0".format(tuple(courseids+[0]))
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgi.itemmodule=mm.name AND mllc.courseid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(tuple(courseids+[0]),contextlevel)
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['dedication']=responsePDF['dedication']/60.
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}         

    def get_modules_user_grades_dedications_by_users(self,userids):
        response=[]
        status='error'
        contextlevel=70
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllc.userid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(tuple(userids+[0]),contextlevel)
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grademax']
            responsePDF['dedication']=responsePDF['dedication']/60.
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response} 

    def get_modules_user_grades_dedications_by_users_figures(self,userids):
        response=[]
        status='error'
        contextlevel=70
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllc.userid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(tuple(userids+[0]),contextlevel)
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grademax']
            responsePDF['dedication']=responsePDF['dedication']/60.

            ycol='dedication'
            xcol='itemname'#'userid' #'modtype' #'userid'
            colorcol='day' #'instanceid'
            hoverdata=['coursename','sectionname','finalgrade','grademax']
            fig = px.bar(responsePDF, y=ycol, x=xcol, color=colorcol, barmode='stack', height=400, hover_data=hoverdata) #, histfunc='avg')
            response={'figures':[fig.to_json()],'data':responsePDF.to_dict(orient='records')}

        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}          

    def get_course_modules_user_grades_dedications_by_users(self,courseid,userids):
        response=[]
        status='error'
        contextlevel=70
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mllc.courseid={} AND mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllc.userid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(courseid,tuple(userids+[0]),contextlevel)
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grademax']
            responsePDF['dedication']=responsePDF['dedication']/60.
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response} 

    def get_grades_dedications_by_users_by_modules(self,moduleids,userids):
        response=[]
        status='error'
        contextlevel=70
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mctx.id AS contextid, mcm.score AS modulescore, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mgi.itemname, mgi.grademax, mgi.grademin, mgi.gradepass, mu.firstname, mu.lastname, mc.shortname AS coursename, mcs.name AS sectionname, mm.name AS modulename, mcm.instance AS instanceid, mcm.section AS sectionid, mllmd.*, mllm.coursemoduleid AS moduleid, mllm.totaldedication AS moduletotaldedication, mllc.courseid, mllc.userid, mllc.totaldedication AS coursetotaldedication FROM mdl_local_ld_module_day mllmd INNER JOIN mdl_local_ld_module mllm ON mllm.id=mllmd.ldmoduleid INNER JOIN mdl_local_ld_course mllc ON mllc.id=mllm.ldcourseid INNER JOIN mdl_course_modules mcm ON mcm.id=mllm.coursemoduleid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mllc.courseid INNER JOIN mdl_user mu ON mu.id=mllc.userid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid INNER JOIN mdl_context mctx ON mctx.instanceid=mllm.coursemoduleid WHERE mgg.userid=mllc.userid AND mgi.itemmodule=mm.name AND mllm.coursemoduleid IN {} AND mllc.userid IN {} AND mcm.deletioninprogress=0 AND mctx.contextlevel={}".format(tuple(moduleids+[0]),tuple(userids+[0]),contextlevel)
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grademax']
            responsePDF['dedication']=responsePDF['dedication']/60.
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}         

    def get_modules_users_dedication(self,moduleids,userids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            #sqlQ="SELECT c.id AS contextid, cm.id AS moduleid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id WHERE c.id IN {}".format(tuple(contextids+[0]))
            #sqlQ="SELECT c.id AS contextid, cm.id AS moduleid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score, ldc.userid, ldm.totaldedication  FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id INNER JOIN mdl_local_ld_module ldm ON c.instanceid=ldm.coursemoduleid INNER JOIN mdl_local_ld_course ldc ON ldm.ldcourseid=ldc.id WHERE cm.id IN {} AND ldc.userid IN {}".format(tuple(moduleids+[0]),tuple(userids+[0]))
            sqlQ="SELECT c.id AS contextid, cm.id AS moduleid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, ldc.userid, ldm.totaldedication, ldmd.dedication, ldmd.day, ldmd.daytime, u.firstname  FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id INNER JOIN mdl_local_ld_module ldm ON c.instanceid=ldm.coursemoduleid INNER JOIN mdl_local_ld_course ldc ON ldm.ldcourseid=ldc.id INNER JOIN mdl_local_ld_module_day ldmd ON ldmd.ldmoduleid=ldm.id INNER JOIN mdl_user u ON u.id=ldc.userid WHERE ldm.coursemoduleid IN {} AND ldc.userid IN {} AND c.contextlevel=70".format(tuple(moduleids+[0]),tuple(userids+[0]))
            
            #print(sqlQ)
            moduleInfoDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            if len(moduleInfoDicts)!=0:
                for dct in moduleInfoDicts:
                    #sqlQ2="SELECT mm.name FROM mdl_{} mm WHERE mm.id={}".format(dct['modtype'],dct['instanceid'])
                    sqlQ2="SELECT mgi.*, mgg.* FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_grade_items mgi ON mgi.itemmodule=mm.name INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mcm.instance=mgi.iteminstance AND mcm.id={} AND mgg.userid IN {}".format(dct['moduleid'],tuple(userids+[0]))

                    #print(sqlQ2)
                    modnameDict=read_sql(sql_text(sqlQ2),con).to_dict(orient='records')
                    if len(modnameDict)!=0:
                        dct['modulename']=modnameDict[0]['itemname']
                        dct['score']=modnameDict[0]['finalgrade']
                    else:
                        dct['modulename']=''
                        dct['score']=''
                    response+=[dct]
            else:
                status='context does not exist'
        except:
            pass
        
        #print(response)
        status="success"  
        con.close()  
        return {"status":status,"response":response}         

    def get_users_modules_by_type_by_role_ids(self,modname,userids,roleids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT ra.userid, mu.firstname, mr.shortname AS rolename, mc.shortname AS coursename, mctx.id AS contextid, mctx.instanceid AS moduleid, mm.name, mh.* FROM mdl_role_assignments ra INNER JOIN mdl_context mctx ON ra.contextid = mctx.id INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_{} mh ON mh.id=mcm.instance INNER JOIN mdl_role mr ON mr.id=ra.roleid INNER JOIN mdl_user mu ON mu.id=ra.userid INNER JOIN mdl_course mc ON mc.id=mcm.course WHERE ra.userid IN {} AND ra.roleid IN {} AND mm.name='{}'".format(modname,tuple(userids+[0]),tuple(roleids+[0]),modname)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response} 

    def get_users_module_contexts_info(self,userids,contextids):
        response=[]
        status='error'
        contextlevel=70
        try:
            #sqlQ="SELECT c.id AS contextid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id WHERE c.id IN {}".format(tuple(contextids+[0]))
            #sqlQ="SELECT c.id AS contextid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score, ldc.userid, ldm.coursemoduleid, ldmd.day, ldmd.daytime  FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id INNER JOIN mdl_local_ld_module ldm ON c.instanceid=ldm.coursemoduleid INNER JOIN mdl_local_ld_course ldc ON ldm.ldcourseid=ldc.id INNER JOIN mdl_local_ld_module_day ldmd ON ldmd.ldmoduleid=ldm.id WHERE c.id IN {} AND ldc.userid IN {}".format(tuple(contextids+[0]),tuple(userids+[0]))
            sqlQ="SELECT c.id AS contextid, cm.id AS moduleid, cm.course AS courseid, mc.fullname AS coursename, cm.instance AS instanceid, mm.name AS modtype, cm.score, ldc.userid, ldm.totaldedication, ldmd.dedication, ldmd.day, ldmd.daytime  FROM mdl_context c INNER JOIN mdl_course_modules cm ON c.instanceid=cm.id INNER JOIN mdl_modules mm ON cm.module=mm.id INNER JOIN mdl_course mc ON cm.course=mc.id INNER JOIN mdl_local_ld_module ldm ON c.instanceid=ldm.coursemoduleid INNER JOIN mdl_local_ld_course ldc ON ldm.ldcourseid=ldc.id INNER JOIN mdl_local_ld_module_day ldmd ON ldmd.ldmoduleid=ldm.id WHERE c.id IN {} AND ldc.userid IN {} AND c.contextlevel={}".format(tuple(contextids+[0]),tuple(userids+[0]),contextlevel)
            print(sqlQ)
            self.engine.dispose()
            con=self.engine.connect()
            moduleInfoDicts=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            if len(moduleInfoDicts)!=0:
                for dct in moduleInfoDicts:
                    sqlQ2="SELECT mm.name FROM mdl_{} mm WHERE mm.id={}".format(dct['modtype'],dct['instanceid'])
                    #print(sqlQ2)
                    modnameDict=read_sql(sql_text(sqlQ2),con).to_dict(orient='records')
                    if len(modnameDict)!=0:
                        dct['modulename']=modnameDict[0]['name']
                    else:
                        dct['modulename']=''
                    response+=[dct]
            else:
                status='context does not exist'
        except:
            pass
        
        #print(response)
        status="success"  
        con.close()  
        return {"status":status,"response":response}           

    def get_course_user_dedication(self,courseid,rolename):
        modvisible=1
        secnvisible=1
        response=[]
        status='error'
        try:
            userDicts=self.get_course_users_by_rolename(courseid,rolename)['response']
            if len(userDicts)!=0:
                userids=[dct['id'] for dct in userDicts]
                moduleDicts=self.get_course_modules(courseid,modvisible,secnvisible)['response']
                if len(moduleDicts)!=0:
                    modSecnDicts={mod['id']:secn['sectionname'] for secn in moduleDicts for mod in secn['sectionmodules']}
                    moduleids=[*modSecnDicts]
                    moduleids.sort()
                    response0=self.get_modules_users_dedication(moduleids,userids)['response']
                    for dct in response0:
                        dct['sectionname']=modSecnDicts[dct['moduleid']]
                        response+=[dct]
                    status="success" 
                else:
                    status='No such modules'
            else:
                status='No users enrolled in course with role '+rolename        
        except:
            pass
        
        #print(response) 
        return {"status":status,"response":response}      

    def get_users_modules_grades(self,datadicts):
        '''
        datadicts=[{"userid":75,"moduleid":968}]
        '''
        response=datadicts
        status='error'
        moduleids=[dct['moduleid'] for dct in datadicts]
        userids=[dct['userid'] for dct in datadicts]
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mgg.finalgrade, mgg.rawgrademax, mcm.id AS moduleid, mgg.userid  FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_grade_items mgi ON mgi.itemmodule=mm.name INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mcm.instance=mgi.iteminstance AND mcm.id IN {} AND mgg.userid IN {} AND mcm.deletioninprogress=0 AND mgg.aggregationstatus='used'".format(tuple(moduleids+[0]),tuple(userids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response} 

    def get_all_modules_grades(self,itemmodule='assign'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mcm.score AS modulescore, mgi.grademax, mgi.grademin, mgi.gradepass, mgi.scaleid, mgi.timecreated AS gradeitemcreated, mgi.timemodified AS gradeitemmodified, mgi.outcomeid, mc.shortname AS course, mgi.itemname AS gradeitemname, mgi.iteminstance, mgg.finalgrade, mgg.rawgrade, mgg.rawgrademax, mgg.rawgrademin, mu.lastname AS lastname, mu.firstname AS firstname, mgg.itemid, mgg.usermodified AS gradeusermodified, mcm.id AS moduleid, mcs.name AS sectionname, mcm.added AS moduleadded, mc.id AS courseid, mu.id AS userid, mcs.id AS sectionid, mcm.instance AS instanceid, mc.category AS categoryid, mcc.name AS categoryname, mh.* FROM mdl_grade_grades mgg INNER JOIN mdl_grade_items mgi ON mgi.id=mgg.itemid INNER JOIN mdl_course mc on mc.id=mgi.courseid INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_modules mm ON mm.name=mgi.itemmodule INNER JOIN mdl_course_modules mcm ON mcm.instance=mgi.iteminstance INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc ON mcc.id=mc.category INNER JOIN mdl_{} mh ON mh.id=mcm.instance WHERE mgi.itemtype='{}' AND  mgi.itemmodule='{}' AND mctx.contextlevel={}".format(itemmodule,itemtype,itemmodule,contextlevel)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response} 

    def get_all_modules_student_grades(self,itemmodule='assign',studentrolename='student'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mcm.module=(SELECT id FROM mdl_modules mm WHERE mm.name='{}') AND mgg.userid=mra.userid AND mcm.deletioninprogress=0".format(studentrolename,itemmodule)
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}         

    def get_all_modules_student_grades_by_courses(self,courseids,itemmodule='assign',studentrolename='student'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mcm.module=(SELECT id FROM mdl_modules mm WHERE mm.name='{}') AND mgg.userid=mra.userid AND mcm.deletioninprogress=0 AND mgi.courseid IN {}".format(studentrolename,itemmodule,tuple(courseids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_all_modules_student_grades_by_userses(self,userids,itemmodule='assign',studentrolename='student'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mcm.module=(SELECT id FROM mdl_modules mm WHERE mm.name='{}') AND mgg.userid=mra.userid AND mcm.deletioninprogress=0 AND mgg.userid IN {}".format(studentrolename,itemmodule,tuple(userids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_all_student_grades_by_modules(self,moduleids,itemmodule='assign',studentrolename='student'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mcm.module=(SELECT id FROM mdl_modules mm WHERE mm.name='{}') AND mgg.userid=mra.userid AND mcm.deletioninprogress=0 AND mcm.id IN {}".format(studentrolename,itemmodule,tuple(moduleids+[0]))
            response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}               

    def get_all_modules_course_student_grades_competency(self,studentrolename='student'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mu.id AS userid, mcompf.shortname AS competencyframework, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid INNER JOIN mdl_modules mm ON mm.id=mcm.module WHERE mgi.itemmodule=mm.name AND mcm.deletioninprogress=0"
            responsePDF=read_sql(sql_text(sqlQ),con)
            responsePDF['gradedeficit']=responsePDF['grademax']-responsePDF['finalgrade']
            responsePDF['attainment']=responsePDF['finalgrade']/responsePDF['grademax']
            responsePDF['minattainment']=responsePDF['gradepass']/responsePDF['grademax']
            #responsePDF.round(decimal=2)
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_categories_course_modules_student_grades_competency(self,categoryids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mgg.userid, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mc.shortname AS coursename, mcs.name AS sectionname, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade FROM mdl_grade_items mgi INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_modules mm ON mm.name=mgi.itemmodule INNER JOIN mdl_course_modules mcm ON mcm.module=mm.id INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid WHERE mcc.id IN {} AND mgi.itemtype='mod' AND mgg.aggregationstatus='used' AND mcm.instance=mgi.iteminstance".format(tuple(categoryids+[0]))
            responsePDF=read_sql(sql_text(sqlQ),con)
            totalStudents=len(list(set(responsePDF['userid'].to_list())))
            # totalActivities=len(list(set(responsePDF['activityname'].to_list())))
            # maxgrades=[]
            # for activity in list(set(responsePDF['activityname'].to_list())):
            #     maxgrades+=list(set(responsePDF[responsePDF['activityname']==activity]['grademax'].to_list()))
            # totalmaxgrades=sum(maxgrades)
            #responsePDF['gradedeficit']=responsePDF['grademax']-responsePDF['finalgrade']
            responsePDF['attainment']=(responsePDF['finalgrade']/responsePDF['grademax'])/totalStudents #(totalmaxgrades)
            responsePDF['minattainment']=(responsePDF['gradepass']/responsePDF['grademax'])/totalStudents #/totalActivities #/(totalStudents*totalActivities) #(totalStudents*totalActivities)
            responsePDF['maxattainment']=(responsePDF['grademax']/responsePDF['grademax'])/totalStudents #/(totalStudents*totalActivities) #/totalActivities #
            responsePDF['fullname']=responsePDF['firstname']+' '+responsePDF['lastname']
            response=responsePDF.drop(columns=['firstname','lastname']).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_categories_course_modules_student_grades_competency_figures(self,categoryids):
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mgg.userid, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mc.shortname AS coursename, mcs.name AS sectionname, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade FROM mdl_grade_items mgi INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_modules mm ON mm.name=mgi.itemmodule INNER JOIN mdl_course_modules mcm ON mcm.module=mm.id INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid WHERE mcc.id IN {} AND mgi.itemtype='mod' AND mgg.aggregationstatus='used' AND mcm.instance=mgi.iteminstance".format(tuple(categoryids+[0]))
            responsePDF=read_sql(sql_text(sqlQ),con)
            totalStudents=len(list(set(responsePDF['userid'].to_list())))
            # maxgrades=[]
            # for activity in list(set(responsePDF['activityname'].to_list())):
            #     maxgrades+=list(set(responsePDF[responsePDF['activityname']==activity]['grademax'].to_list()))
            # totalmaxgrades=sum(maxgrades)
            #responsePDF['gradedeficit']=responsePDF['grademax']-responsePDF['finalgrade']
            responsePDF['attainment']=(responsePDF['finalgrade']/responsePDF['grademax'])/totalStudents #(totalmaxgrades)
            responsePDF['minattainment']=(responsePDF['gradepass']/responsePDF['grademax'])/totalStudents #/totalActivities #/(totalStudents*totalActivities) #(totalStudents*totalActivities)
            responsePDF['maxattainment']=(responsePDF['grademax']/responsePDF['grademax'])/totalStudents #/(totalStudents*totalActivities) #/totalActivities #
            responsePDF['fullname']=responsePDF['firstname']+' '+responsePDF['lastname']
            fig = px.histogram(responsePDF, x='competencyname', y='attainment', histfunc='sum', title="Program relative competency attainement")
            figmax = px.histogram(responsePDF, x='competencyname', y='maxattainment', histfunc='sum', title="Program maximum possible relative competency attainment")
            figstudent = px.bar(responsePDF, x='competencyname', y='attainment', color='fullname', text='activityname', title="Student wise relative competency attainement")
            response={"figures":[fig.to_json(),figmax.to_json(),figstudent.to_json()], "data":responsePDF.to_dict(orient="records")}
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}


    def get_courses_modules_student_grades_competency(self,courseids):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mgg.userid, mcompf.shortname AS competencyframework, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mc.shortname AS coursename, mcs.name AS sectionname, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade FROM mdl_grade_items mgi INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_modules mm ON mm.name=mgi.itemmodule INNER JOIN mdl_course_modules mcm ON mcm.module=mm.id INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid WHERE mgi.courseid IN {} AND mgi.itemtype='mod' AND mgg.aggregationstatus='used' AND mcm.instance=mgi.iteminstance".format(tuple(courseids+[0]))
            responsePDF=read_sql(sql_text(sqlQ),con)
            totalStudents=len(list(set(responsePDF['userid'].to_list())))
            maxgrades=[]
            for activity in list(set(responsePDF['activityname'].to_list())):
                maxgrades+=list(set(responsePDF[responsePDF['activityname']==activity]['grademax'].to_list()))
            totalmaxgrades=sum(maxgrades)
            #responsePDF['gradedeficit']=responsePDF['grademax']-responsePDF['finalgrade']
            responsePDF['attainment']=responsePDF['finalgrade']/totalmaxgrades
            responsePDF['maxattainment']=responsePDF['grademax']/(totalStudents*totalmaxgrades)
            responsePDF['minattainment']=responsePDF['gradepass']/(totalStudents*totalmaxgrades)
            responsePDF['fullname']=responsePDF['firstname']+' '+responsePDF['lastname']
            response=responsePDF.drop(columns=['firstname','lastname']).to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_all_modules_local_student_grades_competency(self,studentrolename='student'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            #sqlQ="SELECT mu.id AS userid, mcompf.shortname AS competencyframework, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid INNER JOIN mdl_{} mh ON mh.id=mgi.iteminstance WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mcm.module=(SELECT id FROM mdl_modules mm WHERE mm.name='{}') AND mgg.userid=mra.userid AND mcm.deletioninprogress=0".format(itemmodule,studentrolename,itemmodule)
            sqlQ="SELECT mcm.id AS moduleid, mu.id AS userid, mcompf.shortname AS competencyframework, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid INNER JOIN mdl_modules mm ON mm.id=mcm.module WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mgi.itemmodule=mm.name AND mgg.userid=mra.userid AND mcm.deletioninprogress=0".format(studentrolename)
            responsePDF=read_sql(sql_text(sqlQ),con)
            totalstudents=len(list(set(responsePDF['userid'].to_list())))
            maxgrades=[]
            for activity in list(set(responsePDF['activityname'].to_list())):
                maxgrades+=list(set(responsePDF[responsePDF['activityname']==activity]['grademax'].to_list()))
            totalmaxgrades=sum(maxgrades)
            responsePDF['gradedeficit']=responsePDF['grademax']-responsePDF['finalgrade']
            responsePDF['attainment']=responsePDF['finalgrade']/(totalmaxgrades)
            responsePDF['maxattainment']=responsePDF['grademax']/(totalstudents*totalmaxgrades)
            responsePDF['minattainment']=responsePDF['gradepass']/(totalstudents*totalmaxgrades)
            #responsePDF.round(decimal=2)
            response=responsePDF.to_dict(orient='records')

            df=responsePDF
            moduleids=list(set(df['moduleid'].to_list()))
            sqlQ2="SELECT mcf.configdata, mcf.shortname, mcf.type, mcd.contextid, mcd.instanceid, mcd.value, mcd.intvalue FROM mdl_customfield_data mcd INNER JOIN mdl_customfield_field mcf ON mcf.id=mcd.fieldid WHERE mcd.instanceid IN {}".format(tuple(moduleids+[0]))
            configdataPDF=read_sql(sql_text(sqlQ2),con)            
            if len(configdataPDF)!=0:
                response=[]
                for moduleid in moduleids:
                    moduleConfigDicts=configdataPDF[configdataPDF['instanceid']==moduleid].to_dict(orient='records')
                    modulePDF=df[df['moduleid']==moduleid]
                    for dct in moduleConfigDicts:
                        if dct['type']=='select':
                            modulePDF[dct['shortname']]=json.loads(dct['configdata'])['options'].split('\r\n')[int(dct['value'])-1]
                        elif dct['type']=='date':
                            modulePDF[dct['shortname']] = datetime.fromtimestamp(int(dct['value'])).strftime('%Y-%m-%d %X')
                        else:
                            modulePDF[dct['shortname']]=dct['value']
                    response+=modulePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_courses_modules_student_grades_competency_full_info(self,courseids):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mu.id AS userid, mcc.id AS categoryid, mc.id AS courseid, mcs.id AS sectionid, mcm.id AS moduleid,  mgi.iteminstance AS activityid, mgi.id AS gradeitmid, mgg.id AS gradeid, mgg.usermodified, mcompf.id AS competencyframeworkid, mcomp.id AS competencyid, mcompf.shortname AS competencyframework, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mc.shortname AS coursename, mcs.name AS sectionname, mgi.itemname AS activityname, mgi.itemmodule AS modulename, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin FROM mdl_grade_items mgi INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_modules mm ON mm.name=mgi.itemmodule INNER JOIN mdl_course_modules mcm ON mcm.module=mm.id INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid WHERE mgi.courseid IN {} AND mgi.itemtype='mod' AND mgg.aggregationstatus='used' AND mcm.instance=mgi.iteminstance".format(tuple(courseids+[0]))
            responsePDF=read_sql(sql_text(sqlQ),con)
            totalmaxgrades=[]
            for activity in list(set(responsePDF['activityname'].to_list())):
                totalmaxgrades+=list(set(responsePDF[responsePDF['activityname']==activity]['grademax'].to_list()))
            responsePDF['gradedeficit']=responsePDF['grademax']-responsePDF['finalgrade']
            responsePDF['attainment']=responsePDF['finalgrade']/sum(totalmaxgrades)
            responsePDF['maxattainment']=responsePDF['grademax']/sum(totalmaxgrades)
            responsePDF['minattainment']=responsePDF['gradepass']/sum(totalmaxgrades)
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def get_all_modules_local_student_grades_competency_full_info(self,studentrolename='student'):
        #itemtype -> 'mod', 'course'
        itemtype='mod'
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            #sqlQ="SELECT mu.id AS userid, mc.id AS courseid, mcs.id AS sectionid, mcm.id AS moduleid, mh.id AS activityid, mgi.id AS gradeitmid, mgg.id AS gradeid, mcompf.id AS competencyframeworkid, mcomp.id AS competencyid, mcompf.shortname AS competencyframework, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid INNER JOIN mdl_{} mh ON mh.id=mgi.iteminstance WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mcm.module=(SELECT id FROM mdl_modules mm WHERE mm.name='{}') AND mgg.userid=mra.userid AND mcm.deletioninprogress=0".format(itemmodule,studentrolename,itemmodule)
            sqlQ="SELECT mu.id AS userid, mc.id AS courseid, mcs.id AS sectionid, mcm.id AS moduleid, mcm.instance AS activityid, mgi.id AS gradeitmid, mgg.id AS gradeid, mcompf.id AS competencyframeworkid, mcomp.id AS competencyid, mcompf.shortname AS competencyframework, mcomp.shortname AS competencyname, mu.firstname, mu.lastname, mcc.name AS categoryname, mcs.name AS sectionname, mcm.score AS modulescore, mcm.added AS moduleadded, mc.shortname AS coursename, mgi.itemname AS activityname, mgi.grademin, mgi.grademax, mgi.gradepass, mgg.finalgrade, mgg.rawgrademax, mgg.rawgrade, mgg.rawgrademin, mgg.usermodified FROM mdl_role_assignments mra INNER JOIN mdl_context mctx ON mctx.id=mra.contextid INNER JOIN mdl_course_modules mcm ON mcm.id=mctx.instanceid INNER JOIN mdl_grade_items mgi ON mgi.iteminstance=mcm.instance INNER JOIN mdl_grade_grades mgg ON mgg.itemid=mgi.id INNER JOIN mdl_course mc ON mc.id=mgi.courseid INNER JOIN mdl_course_sections mcs ON mcs.id=mcm.section INNER JOIN mdl_course_categories mcc on mcc.id=mc.category INNER JOIN mdl_user mu ON mu.id=mgg.userid INNER JOIN mdl_competency_modulecomp mcompm on mcompm.cmid=mcm.id INNER JOIN mdl_competency mcomp ON mcomp.id=mcompm.competencyid INNER JOIN mdl_competency_framework mcompf ON mcompf.id=mcomp.competencyframeworkid INNER JOIN mdl_modules mm ON mm.id=mcm.module WHERE mra.roleid=(SELECT mr.id FROM mdl_role mr WHERE mr.shortname='{}') AND mm.name=mgi.itemmodule AND mgg.userid=mra.userid AND mcm.deletioninprogress=0".format(studentrolename)
            responsePDF=read_sql(sql_text(sqlQ),con)
            totalmaxgrades=[]
            for activity in list(set(responsePDF['activityname'].to_list())):
                totalmaxgrades+=list(set(responsePDF[responsePDF['activityname']==activity]['grademax'].to_list()))
            #responsePDF['gradedeficit']=responsePDF['grademax']-responsePDF['finalgrade']
            responsePDF['attainment']=responsePDF['finalgrade']/sum(totalmaxgrades)
            responsePDF['maxattainment']=responsePDF['grademax']/sum(totalmaxgrades)
            responsePDF['minattainment']=responsePDF['gradepass']/sum(totalmaxgrades)
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        status="success"  
        con.close()  
        return {"status":status,"response":response}

    def update_course_module_grades(self,datadicts):
        '''
        datadicts=[{"courseid":"int","moduleid":"int","userid":"int","grade":"float","modname":"str->assign,quiz,.."}]
        '''
        response=[]
        status='error'        
        itemnumber=0
        wsfunction='core_grades_update_grades'
        try:
            for dct in datadicts:
                grades=[{"studentid":dct['userid'],"grade":dct['grade']}]
                parameters={"source":'Teal Webserice',"courseid":dct['courseid'],"component":"mod_"+dct['modname'],"activityid":dct['moduleid'],"itemnumber":itemnumber, 'grades':grades}
                response+=[{"updated":self.call(self.mWAP,wsfunction,**parameters)==0}]              
            status='success'        
        except:
            pass
        return {"status":status,"response":response}
    
########################################################################
    def get_module_user_dedication(self,courseid,moduleid,rolename):
        modvisible=1
        secnvisible=1
        response=[]
        status='error'
        try:
            userDicts=self.get_course_users_by_rolename(courseid,rolename)['response']
            if len(userDicts)!=0:
                userids=[dct['id'] for dct in userDicts]
                print(userids)
                response=self.get_modules_users_dedication([moduleid],userids)['response']
                status="success" 
            else:
                status='No users enrolled in course with role '+rolename        
        except:
            pass
        
        print(response) 
        return {"status":status,"response":response}   

    def get_user_context_connectivity2(self,userid,contextlevel,edulevel,startDateStr,endDateStr):
        nodeInfo=[]
        edgeInfo=[]
        response={"nodeInfo":nodeInfo,"edgeInfo":edgeInfo}
        status='No activity'
        eventDicts=self.get_user_context_events(userid,contextlevel,edulevel,startDateStr,endDateStr)['response']
        try:
            if len(eventDicts)!=0:
                eventsPDF=DataFrame(eventDicts)
                #print(eventDicts)
                states=eventsPDF['contextid'].to_list()
                contextsList=list(set(states))
                edgeInfoDict=eventsPDF[['eventname','relateduserid','target','timecreated','usrdt','ip','userid']].to_dict(orient='records')
                nodeDataKeys=['contextid','contextlevel','contextinstanceid','courseid']
                modContexts=self.get_module_contexts_info(contextsList)['response']
                modulesList=[dct['moduleid'] for dct in modContexts]
                dedicationsDict=self.get_users_modules_dedication([userid], modulesList)['response']
                self.engine.dispose()
                con=self.engine.connect()
                for nd in contextsList:
                    node_n_infoDict={ky:0 for ky in nodeDataKeys}
                    node_n_infoDict['score']=0
                    tmpPDF=eventsPDF[eventsPDF['contextid']==nd]
                    node_n_infoDict=tmpPDF.loc[tmpPDF.index.values[0],nodeDataKeys].to_dict()
                    temp=[mod for mod in modContexts if mod['contextid']==nd][0]  #self.get_module_contexts_info([node_n_infoDict['contextid']])['response']
                    node_n_infoDict['modulename']=temp['modulename']
                    node_n_infoDict['coursename']=temp['coursename']
                    node_n_infoDict['modtype']=temp['modtype']
                    node_n_infoDict['modscore']=temp['score']
                    #self.get_users_modules_dedication([userid], [['moduleid']])['response']
                    #dedication=[dct for dct in dedicationsDict if dct['contextid']==nd]
                    node_n_infoDict['totaldedication']=sum([dct['dedication'] for dct in dedicationsDict if dct['contextid']==nd])
                    
                    try:
                        moduleid=node_n_infoDict['contextinstanceid']
                        sqlQ="SELECT mgg.finalgrade FROM mdl_course_modules mcm INNER JOIN mdl_modules mm ON mm.id=mcm.module INNER JOIN mdl_grade_items mgi ON mgi.itemmodule=mm.name INNER JOIN mdl_grade_grades mgg ON mgi.id=mgg.itemid WHERE mcm.instance=mgi.iteminstance AND mcm.id={} AND mgg.userid={}".format(moduleid,userid)
                        gradesdict=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
                        if len(gradesdict)!=0:
                            finalGrade=gradesdict[0]['finalgrade']
                            if finalGrade!=None:
                                node_n_infoDict['score']=finalGrade
                            else:
                                node_n_infoDict['score']=0
                        else:
                            node_n_infoDict['score']=0
                    except:
                        pass
    

                    #print(node_n_infoDict)
                    nodeX=int(time.mktime(to_datetime(tmpPDF.loc[tmpPDF.index.values[0],'timecreated'],dayfirst=True).to_pydatetime().timetuple()))
                    nodeY=int(time.mktime(to_datetime(tmpPDF.loc[tmpPDF.index.values[-1],'timecreated'],dayfirst=True).to_pydatetime().timetuple()))
                    nodeInfo+=[(nd, {'pos':(nodeX,nodeY),'data':node_n_infoDict})]
                #print(nodeInfo)
                edgeInfo=[(node,states[inn+1],edgeInfoDict[inn]) for inn,node in enumerate(states[:-1])]
                response={"nodeInfo":nodeInfo,"edgeInfo":edgeInfo}
                status="success"
                con.close()
            else:
                pass
        except:
            pass
        return {"status":status,"response":response}

    def get_user_context_connectivity(self,userid,contextlevel,edulevel,startDateStr,endDateStr):
        nodeInfo=[]
        edgeInfo=[]
        response={"nodeInfo":nodeInfo,"edgeInfo":edgeInfo}
        status='No activity'
        eventDicts=self.get_user_context_events(userid,contextlevel,edulevel,startDateStr,endDateStr)['response']
        try:
            if len(eventDicts)!=0:
                eventsPDF=DataFrame(eventDicts)
                #print(eventDicts)
                states=eventsPDF['contextid'].to_list()
                contextsList=list(set(states))
                edgeInfoDict=eventsPDF[['eventname','relateduserid','target','timecreated','usrdt','ip','userid']].to_dict(orient='records')
                nodeDataKeys=['contextid','contextlevel','contextinstanceid','courseid']
                modContexts=self.get_module_contexts_info(contextsList)['response']
                modulesList=[dct['moduleid'] for dct in modContexts]
                dedicationsPDF=DataFrame(self.get_users_modules_dedication([userid], modulesList)['response']).fillna(0)
                for nd in contextsList:
                    contextDedPDF=dedicationsPDF[dedicationsPDF['contextid']==nd]
                    node_n_infoDict={ky:0 for ky in nodeDataKeys}
                    node_n_infoDict['score']=0
                    tmpPDF=eventsPDF[eventsPDF['contextid']==nd]
                    node_n_infoDict=tmpPDF.loc[tmpPDF.index.values[0],nodeDataKeys].to_dict()
                    temp=[mod for mod in modContexts if mod['contextid']==nd][0]  #self.get_module_contexts_info([node_n_infoDict['contextid']])['response']
                    node_n_infoDict['modulename']=temp['modulename']
                    node_n_infoDict['coursename']=temp['coursename']
                    node_n_infoDict['modtype']=temp['modtype']
                    node_n_infoDict['modscore']=temp['score']
                    node_n_infoDict['totaldedication']=sum(contextDedPDF['dedication'].to_list())  #sum([dct['dedication'] for dct in dedicationsDict if dct['contextid']==nd])
                    node_n_infoDict['score']=0 #max(contextDedPDF['grademax'].to_list())

                    #print(node_n_infoDict)
                    nodeX=int(time.mktime(to_datetime(tmpPDF.loc[tmpPDF.index.values[0],'timecreated'],dayfirst=True).to_pydatetime().timetuple()))
                    nodeY=int(time.mktime(to_datetime(tmpPDF.loc[tmpPDF.index.values[-1],'timecreated'],dayfirst=True).to_pydatetime().timetuple()))
                    nodeInfo+=[(nd, {'pos':(nodeX,nodeY),'data':node_n_infoDict})]
                #print(nodeInfo)
                edgeInfo=[(node,states[inn+1],edgeInfoDict[inn]) for inn,node in enumerate(states[:-1])]
                response={"nodeInfo":nodeInfo,"edgeInfo":edgeInfo}
                status="success"
            else:
                pass
        except:
            pass
        return {"status":status,"response":response}

    def get_user_context_connectivity_new(self,userid,contextlevel,edulevel,startDateStr,endDateStr):
        nodeInfo=[]
        edgeInfo=[]
        response={"nodeInfo":nodeInfo,"edgeInfo":edgeInfo}
        status='No activity'
        try:    
            ##############
            allEventDicts=self.get_user_context_events(userid,contextlevel,edulevel,startDateStr,endDateStr)['response']
            ##################
            if len(allEventDicts)!=0:
                allEventPDF=DataFrame(allEventDicts)
                allEventModulesList=list(set(allEventPDF['contextinstanceid'].to_list()))
                ####################
                dedicationsPDF=DataFrame(self.get_grades_dedications_by_users_by_modules(allEventModulesList,[userid])['response']).fillna(0.0)
                ####################
                modulesList=list(set(dedicationsPDF['moduleid'].to_list()))
                eventsPDF=allEventPDF[allEventPDF['contextinstanceid'].isin(modulesList)].copy()
                states=eventsPDF['contextinstanceid'].to_list()
                edgeInfoDict=eventsPDF[['eventname','relateduserid','target','timecreated','usrdt','ip','userid']].to_dict(orient='records')
                nodeDataKeys=['coursename','sectionname','itemname','finalgrade','attainment']
                
                for nd in modulesList:
                    moduleDedPDF=dedicationsPDF[dedicationsPDF['moduleid']==nd]
                    tmpPDF=eventsPDF[eventsPDF['contextinstanceid']==nd]
                    node_n_infoDict={ky:0 for ky in nodeDataKeys}
                    node_n_infoDict=moduleDedPDF.loc[moduleDedPDF.index.values[0],nodeDataKeys].to_dict()
                    node_n_infoDict['finalgrade']=moduleDedPDF['finalgrade'].max()
                    node_n_infoDict['attainment']=moduleDedPDF['attainment'].max()
                    node_n_infoDict['dedication']=moduleDedPDF['dedication'].sum()
                    nodeX=int(time.mktime(to_datetime(tmpPDF['timecreated'].min(),dayfirst=True).to_pydatetime().timetuple()))
                    nodeY=int(time.mktime(to_datetime(tmpPDF['timecreated'].max(),dayfirst=True).to_pydatetime().timetuple()))
                    nodeInfo+=[(nd, {'pos':(nodeX,nodeY),'data':node_n_infoDict})]
                edgeInfo=[(node,states[inn+1],edgeInfoDict[inn]) for inn,node in enumerate(states[:-1])]
                response={"nodeInfo":nodeInfo,"edgeInfo":edgeInfo}
                status="success"
            else:
                pass
        except:
            pass    
        return {"status":status,"response":response}        

    def get_user_context_connectivity_figure(self,userid,startDateStr,endDateStr,contextlevel=70,edulevel=2):
        nodeInfo=[]
        edgeInfo=[]
        response=[]
        status='No activity'
        try:    
            ##############
            allEventDicts=self.get_user_context_events(userid,contextlevel,edulevel,startDateStr,endDateStr)['response']
            ##################
            if len(allEventDicts)!=0:
                allEventPDF=DataFrame(allEventDicts)
                allEventModulesList=list(set(allEventPDF['contextinstanceid'].to_list()))
                ####################
                dedicationsPDF=DataFrame(self.get_grades_dedications_by_users_by_modules(allEventModulesList,[userid])['response']).fillna(0.0)
                ####################
                modulesList=list(set(dedicationsPDF['moduleid'].to_list()))
                eventsPDF=allEventPDF[allEventPDF['contextinstanceid'].isin(modulesList)].copy()
                states=eventsPDF['contextinstanceid'].to_list()
                edgeInfoDict=eventsPDF[['eventname','relateduserid','target','timecreated','usrdt','ip','userid']].to_dict(orient='records')
                nodeDataKeys=['coursename','sectionname','itemname','finalgrade','attainment']
                
                for nd in modulesList:
                    moduleDedPDF=dedicationsPDF[dedicationsPDF['moduleid']==nd]
                    tmpPDF=eventsPDF[eventsPDF['contextinstanceid']==nd]
                    node_n_infoDict={ky:0 for ky in nodeDataKeys}
                    node_n_infoDict=moduleDedPDF.loc[moduleDedPDF.index.values[0],nodeDataKeys].to_dict()
                    node_n_infoDict['finalgrade']=moduleDedPDF['finalgrade'].max()
                    node_n_infoDict['attainment']=moduleDedPDF['attainment'].max()
                    node_n_infoDict['dedication']=moduleDedPDF['dedication'].sum()
                    nodeX=int(time.mktime(to_datetime(tmpPDF['timecreated'].min(),dayfirst=True).to_pydatetime().timetuple()))
                    nodeY=int(time.mktime(to_datetime(tmpPDF['timecreated'].max(),dayfirst=True).to_pydatetime().timetuple()))
                    nodeInfo+=[(nd, {'pos':(nodeX,nodeY),'data':node_n_infoDict})]
                edgeInfo=[(node,states[inn+1],edgeInfoDict[inn]) for inn,node in enumerate(states[:-1])]
                nodeInfoG=[]; edgeInfoG=[];
                fig=go.Figure()

                G = nx.MultiDiGraph()
                nodeInfoG=[tuple(nI) for nI in nodeInfo]
                G.add_nodes_from(nodeInfo)
                if len(edgeInfo)!=0:    
                    edgeInfoG=[tuple(nI) for nI in edgeInfo]
                    states=[nn[0] for nn in nodeInfoG]    
                    G.add_edges_from(edgeInfoG)
                    fig=self.plot_network_graph(G,'usrdt','Module Transition')

                response={"figures":[fig.to_json()],"data":{"nodeinfo":nodeInfoG,"edgeinfo":edgeInfoG}}
                status="success"
            else:
                pass
        except:
            pass    
        return {"status":status,"response":response} 

    def plot_network_graph(self,G,nodesizekey,graphTitle):
        fig = go.Figure()
        node_x = []
        node_y = []
        edge_x=[]
        edge_y=[]
        node_text=[]
        edge_text=[]
        node_size=[]
        edge_size=[]
        node_color=[]
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            nodeName=G.nodes[node]['data']['itemname']
            courseName=G.nodes[node]['data']['coursename']
            sectionName=G.nodes[node]['data']['sectionname']
            nodeTime=G.nodes[node]['data']['dedication']
            nodeScore=G.nodes[node]['data']['finalgrade']
            print(nodeName)
            node_x.append(x)
            node_y.append(y)
            for edge in list(set([edg for edg in G.out_edges(node)])):
                x0, y0 = G.nodes[edge[0]]['pos']
                x1, y1 = G.nodes[edge[1]]['pos']
                edge_x.append(x0)
                edge_x.append(x1)
                #edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                #edge_y.append(None)
                edge_text.append(str(edge))
                if edge[0]!=edge[1]:
                    edgesize=G.number_of_edges(edge[0],edge[1])+G.number_of_edges(edge[1],edge[0])
                else:
                    edgesize=G.number_of_edges(edge[0],edge[1])
                fig.add_trace(go.Scatter(
                    x=edge_x, y=edge_y,
                    mode="lines+markers",
                    text='',
                    hoverinfo='text',
                    #marker=dict(symbol="arrow",color="royalblue",size=10,angleref="previous",standoff=20),
                    line=dict(width=1.5,color='#888'), #dict(width=round(0.5+edgesize/4),color='#888'), 
                    #hovertemplate="""Number of edges:{} - {}<br><extra></extra>""".format(str(edge),edgesize)
                    ))

            node_size.append(24) #node_size.append(nodesize)
            node_color.append(len(list(set([edg for edg in G.in_edges(node)])))) #node_size.append(nodesize)
            ine=list(set([edg[0] for edg in G.in_edges(node)]))
            ine.sort()
            oute=list(set([edg[1] for edg in G.out_edges(node)]))
            oute.sort()
            innodes=', '.join([str(nn) for nn in ine])
            outnodes=', '.join([str(nn) for nn in oute])

            nodetxt="""Node ID: {}<br>Name: {}<br>Course: {}<br>Time spent / mins: {} <br>Final Gratde: {} <br>From nodes: {} <br>To nodes: {}""".format(str(node),nodeName,courseName,round(nodeTime+0.5),round(nodeScore,1),innodes,outnodes)
            node_text.append(nodetxt)

        node_trace=go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True, #True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Rainbow', #'YlGnBu',
                reversescale=True,
                color=[], #'royalblue',
                colorbar=dict(
                    thickness=15,
                    title='Number of re-visits',
                    xanchor='left',
                    titleside='right'),
                line_width=2),
                hovertemplate="""%{text}<br><extra></extra>"""
                )
        

        #normalized_node_size=[44*round((xx-min(node_size))/(max(node_size)-min(node_size))) for xx in node_size]
        node_trace.marker.size=node_size
        node_trace.marker.color=node_color
        node_trace.text=node_text
        #edge_trace.line.width=5 #edge_size
        #edge_trace.marker.text=edge_text
        node_adjacencies = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))

        fig.add_trace(node_trace)
        fig.update_layout(
                    title='<br>'+graphTitle,
                    titlefont_size=16,
                    xaxis_title="Time first visited",
                    yaxis_title="Time last visited",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Test text",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

        return fig


    def get_user_context_events_graph(self,graphInfo):
        G = nx.MultiDiGraph()
        nodeInfo=graphInfo['nodeInfo']
        if len(nodeInfo)!=0:    
            G.add_nodes_from(nodeInfo)
        edgeInfo=graphInfo['edgeInfo']
        if len(edgeInfo)!=0:    
            states=[nn[0] for nn in graphInfo['nodeInfo']]    #pd.DataFrame(output)['contextid'].to_list()
            G.add_edges_from(edgeInfo)
        return G

    def get_user_graph_properties(self,G):
        userproperties={'number_of_nodes':0,'total_re_visits':0,'number_of_selfloops':0,'density':0,'global_reaching_centrality':0,'totalgrade':0,'totaldedication':0}
        number_of_nodes=G.number_of_nodes()
        userproperties['number_of_nodes']=number_of_nodes
        self_loops=nx.number_of_selfloops(G)
        userproperties['total_re_visits']=max(0,G.number_of_edges()-self_loops-(number_of_nodes-1))
        userproperties['number_of_selfloops']=self_loops
        userproperties['density']=0
        userproperties['global_reaching_centrality']=0
        tgrade=0
        tdedication=0
        for node in G.nodes():
            tgrade+=G.nodes[node]['data']['finalgrade']
            tdedication+=G.nodes[node]['data']['dedication'] #
        userproperties['totalgrade']=tgrade
        userproperties['totaldedication']=round(tdedication+0.5)
        usrdt=0
        for edg in G.edges():
            for ky in [*G.get_edge_data(edg[0],edg[1])]:
                usrdt+=G.get_edge_data(edg[0],edg[1],ky)['usrdt']
        userproperties['usrdt']=usrdt/60.
        status='error'
        try:
            userproperties['density']=nx.density(G)
            userproperties['global_reaching_centrality']=nx.global_reaching_centrality(G)

        except:
            pass
        status='success'
        return {'status':status,'response':userproperties}

    def get_users_graph_properties(self,userids,contextlevel,edulevel,startDateStr,endDateStr):
        userdicts=[]
        status='error'
        G = nx.MultiDiGraph()
        for userid in userids:
            graphInfo=self.get_user_context_connectivity_new(userid,contextlevel,edulevel,startDateStr,endDateStr)['response']
            if len(graphInfo['nodeInfo'])!=0:
                try:
                    G=self.get_user_context_events_graph(graphInfo)
                    userdict=self.get_user_graph_properties(G)['response']
                    userdict['userid']=userid
                    userdicts+=[userdict]
                except:
                    pass                   
        status='success'
        return {"status":status,"response":userdicts}


###########################################################
#### User functions ######################
###########################################################

    def create_user(self,userdict):
        userInfo=self.call(self.mWAP,'core_user_get_users',criteria=[{'key':'username','value':userdict['username']}])['users'] #[0]
        userExists=(len(userInfo)!=0)
        if userExists:
            response='User '+userdict['username']+' alread exists'
            #Go back to the form
        else:
            response=self.call(self.mWAP,'core_user_create_users',users=[userdict])
        return response

    def get_users_by_field(self,field,values):
        '''
        Webserice call: {"field":string,"values":[]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        try:        
            response=self.call(self.mWAP,'core_user_get_users_by_field',field=field,values=values)
            status='success'
        except:
            pass
        
        return {'status':status,'response':response}

    def create_users(self,datadicts):
        '''
        Webserice call: {"datadicts":[{"username":string,"firstname":string,"lastname":string,"email":str}]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        field='email'
        userdicts=copy.deepcopy(datadicts)
        tempPDF=DataFrame(userdicts)
        tempPDF['createpassword']=0
        tempPDF['password']='TempPWD'
        userdicts=tempPDF.to_dict(orient='records')
        try:        
            searchusers=[dct[field] for dct in userdicts]
            existingUsers=self.call(self.mWAP,'core_user_get_users_by_field',field=field,values=searchusers)
            existingUserList=[dct[field] for dct in existingUsers]
            users2bAdded=[dct for dct in userdicts if dct[field] not in existingUserList]
            #response=users2bAdded
            response=self.call(self.mWAP,'core_user_create_users',users=users2bAdded)
            status='success'
        except:
            pass
        
        return {'status':status,'response':response}

    def delete_users(self,userids):
        '''
        Webserice call: {"deleteusers":<list of field values>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        try:        
            response=self.call(self.mWAP,'core_user_delete_users',userids=userids)
            status='success'
        except:
            pass
        
        return {'status':status,'response':response}

    def get_user_info(self,criteria):
        '''
        Webserice call: criteria=[{'key':<'username','email,..>,'value':str}]
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        try:
            response=self.call(self.mWAP,'core_user_get_users',criteria=criteria)['users']
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_all_users(self):
        '''
        Webserice call: {}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            response=read_sql(sql_text('SELECT * FROM mdl_user WHERE deleted=0'),con).to_dict(orient='records')
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}

    def get_user_id_list(self):
        '''
        Webserice call: {}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        try:
            self.engine.dispose()
            con=self.engine.connect()
            usersDict=read_sql(sql_text('SELECT id, firstname, lastname FROM mdl_user WHERE deleted=0'),con).to_dict(orient='records')
            responsePDF=DataFrame([{"label":dct['firstname']+' '+dct['lastname'], "value":dct['id']} for dct in usersDict]).sort_values(by=['label'])
            response=responsePDF.to_dict(orient="records")
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}

##############################
##Enrolment functions
##############################
    def get_role_id_list(self):
        '''
        Webserice call: {}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            rolesDict=read_sql(sql_text('SELECT id, shortname FROM mdl_role'),con).to_dict(orient='records')
            response=[{"label":dct['shortname'], "value":dct['id']} for dct in rolesDict]
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}

    def assign_context_roles(self,datadicts):
        '''
        Webserice call: {"datadicts":[{'userid':'int', 'roleid':'int', 'contextid':'int','contextlevel':'str->(block, course, coursecat, system, user, module)'}]}
        Response: {'status':status,'response':response}
        '''
        #roleid= int   //Role to assign to the user
        #userid int   //The user that is going to be assigned
        #contextid int  Optional //The context to assign the user role in
        #contextlevel="module" #string  Optional //The context level to assign the user role in(block, course, coursecat, system, user, module)

        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_role_assign_roles',assignments=datadicts)
            status='success'
        except:
            pass
        response=[{'status':status}]
        return {'status':status,'response':response}
    
    def assign_users_contexts_role_from_instances(self,roleid,contextlevel,instanceids,userids):
        '''
        Webserice call: {"datadicts":[{'userid':'int', 'roleid':'int', 'contextid':'int','contextlevel':'str->(block, coursecat, system, user, module)'}]}
        Response: {'status':status,'response':response}
        '''
        #roleid= int   //Role to assign to the user
        #userid int   //The user that is going to be assigned
        #contextid int  Optional //The context to assign the user role in
        #contextlevel="module" #string  Optional //The context level to assign the user role in(block, course, coursecat, system, user, module)
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()
        try:
            sqlQ="SELECT mctx.id, mctx.instanceid FROM mdl_context mctx WHERE mctx.contextlevel={} AND mctx.instanceid IN {}".format(contextlevel,tuple(instanceids+[0]))
            contextids=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
            contextlevelsmap={40:"coursecat",70:"module",10:"system"}
            datadicts=[]
            for userid in userids:
                for dct in contextids:
                    datadicts+=[{'userid':userid,'roleid':roleid,'contextid':dct['id'],'contextlevel':contextlevelsmap[contextlevel]}]            
                    response=self.assign_context_roles(datadicts)['response']
            status="success"
        except:
            pass

        con.close()
        return {'status':status,'response':response}    

    def assign_users_contexts_role_from_contexts(self,roleid,contextlevel,contextids,userids):
        '''
        Webserice call: {"datadicts":[{'userid':'int', 'roleid':'int', 'contextid':'int','contextlevel':'str->(block, coursecat, system, user, module)'}]}
        Response: {'status':status,'response':response}
        '''
        #roleid= int   //Role to assign to the user
        #userid int   //The user that is going to be assigned
        #contextid int  Optional //The context to assign the user role in
        #contextlevel="module" #string  Optional //The context level to assign the user role in(block, course, coursecat, system, user, module)
        response=[]
        status='error'
        contextlevelsmap={40:"coursecat",70:"module",10:"system"}
        datadicts=[]
        for userid in userids:
            for contextid in contextids:
                datadicts+=[{'userid':userid,'roleid':roleid,'contextid':contextid,'contextlevel':contextlevelsmap[contextlevel]}]            
                response=self.assign_context_roles(datadicts)['response']
        status="success"
        return {'status':status,'response':response}

    def assign_context_role(self,contextid, userid,roleid):
        '''
        Webserice call: {"coursename":<Course short name>,"username":<username>,"userrole":<User role short name>}
        Response: {'status':status,'response':response}
        '''
        #roleid= int   //Role to assign to the user
        #userid int   //The user that is going to be assigned
        #contextid int  Optional //The context to assign the user role in
        #contextlevel="module" #string  Optional //The context level to assign the user role in(block, course, coursecat, system, user, module)

        response=[]
        status="error"
        try:
            enrolmentList=[{'userid':userid, 'roleid':roleid, 'contextid':contextid}]
            response=self.call(self.mWAP,'core_role_assign_roles',assignments=enrolmentList)
            status='success'
        except:
            pass
        return {'status':status,'response':response}
    
    def assign_module_roles(self,datadicts):
        '''
        Webserice call: {"datadicts":[{'userid':userid, 'roleid':roleid,'instanceid':moduleid, 'contextid':contextid,'contextlevel':"module"}]}
        Response: {'status':status,'response':response}
        '''
        #roleid= int   //Role to assign to the user
        #userid int   //The user that is going to be assigned
        #contextid int  //The context to assign the user role in
        #contextlevel="module" #string  //The context level to assign the user role in(block, course, coursecat, system, user, module)

        response=[]
        status="error"
        try:
            #roleID=roleid #read_sql(sql_text('SELECT id FROM mdl_role WHERE shortname="{}"'.format(userrole)),self.engine)['id'].values[0] #TEAL2.O Teacher
            response=self.call(self.mWAP,'core_role_assign_roles',assignments=datadicts)
            status='success'
            response=datadicts
        except:
            pass
        return {'status':status,'response':response} 

    def assign_module_default_roles(self,userroledicts, moduledicts):
        '''
        Webserice call: {"userroledicts":[{"userid":"<>","roleid":"<>"}],"moduledicts":[{"moduleid":"<>","contextid":"<>"}]}
        Response: {'status':status,'response':response}
        '''
        #roleid= int   //Role to assign to the user
        #userid int   //The user that is going to be assigned
        #contextid int  //The context to assign the user role in
        #contextlevel="module" #string  //The context level to assign the user role in(block, course, coursecat, system, user, module)

        response=[]
        status="error"
        datadicts=[]
        try:
            for module in moduledicts:
                for dct in userroledicts:
                    datadicts+=[{'userid':dct['userid'], 'roleid':dct['roleid'],'instanceid':module['moduleid'], 'contextid':module['contextid'],'contextlevel':"module"}]
            response=self.call(self.mWAP,'core_role_assign_roles',assignments=datadicts)
            status='success'
            response=datadicts
        except:
            pass
        return {'status':status,'response':response} 

    def unassign_module_roles(self,datadicts):
        '''
        Webserice call: {"datadicts":[{'userid':userid, 'roleid':roleid,'instanceid':moduleid, 'contextid':contextid,'contextlevel':"module"}]}
        Response: {'status':status,'response':response}
        '''
        #roleid= int   //Role to assign to the user
        #userid int   //The user that is going to be assigned
        #contextid int  //The context to assign the user role in
        #contextlevel="module" #string  //The context level to assign the user role in(block, course, coursecat, system, user, module)

        response=[]
        status="error"
        try:
            #roleID=roleid #read_sql(sql_text('SELECT id FROM mdl_role WHERE shortname="{}"'.format(userrole)),self.engine)['id'].values[0] #TEAL2.O Teacher
            response=self.call(self.mWAP,'core_role_unassign_roles',unassignments=datadicts)
            status='success'
            response=datadicts            
        except:
            pass
        return {'status':status,'response':response}    

    def manual_enrol_cohort_in_course(self,courseid,cohortids,roleid):
        '''
        Webserice call: {"coursename":<Course short name>,"cohortname":<Cohort short name>,"roleid":<roleid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            cohortUserIDs=self.call(self.mWAP,'core_cohort_get_cohort_members',cohortids=cohortids)[0]['userids']
            roleID=roleid #read_sql(sql_text('SELECT id FROM mdl_role WHERE shortname="{}"'.format(userrole)),self.engine)['id'].values[0] #TEAL2.O Teacher
            enrolmentList=[]
            for userid in cohortUserIDs:
                enrolmentList+=[{'courseid':courseid, 'userid':userid, 'roleid':roleid}]
            response=self.call(self.mWAP,'enrol_manual_enrol_users',enrolments=enrolmentList)
            status='success'
        except:
            pass

        return {'response':response,'status':status}

    def manual_unenrol_cohort_in_course(self,coursename,cohortname,roleid):
        '''
        Webserice call: {"coursename":<Course short name>,"cohortname":<Cohort short name>,"userrole":<User role short name>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            contentDict=[crs for crs in self.call(self.mWAP,'core_course_search_courses',criterianame='search',criteriavalue=coursename)['courses'] if crs['shortname']==coursename][0]
            contentID=contentDict['id'] 
            cohortDict=[dct for dct in self.call(self.mWAP, 'core_cohort_get_cohorts') if dct['name']==cohortname][0]
            cohortUserIDs=self.call(self.mWAP,'core_cohort_get_cohort_members',cohortids=[cohortDict['id']])[0]['userids']
            roleID=roleid #read_sql(sql_text('SELECT id FROM mdl_role WHERE shortname="{}"'.format(userrole)),self.engine)['id'].values[0] #TEAL2.O Teacher
            enrolmentList=[]
            for userID in cohortUserIDs:
                enrolmentList+=[{'courseid':contentID, 'userid':userID, 'roleid':roleID}]
            response=self.call(self.mWAP,'enrol_manual_unenrol_users',enrolments=enrolmentList)
            status='success'
        except:
            pass

        return {'response':response,'status':status}

    def manual_enrol_users_in_courses(self,datadicts):
        '''
        Webserice call: {"datadicts":[{'courseid':courseid, 'userid':userid, 'roleid':roleid}]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'enrol_manual_enrol_users',enrolments=datadicts)
            status='success'
            response=datadicts
        except:
            pass
        return {'status':status,'response':response}

    def manual_enrol_system_users_in_courses(self,courseids):
        '''
        Webserice call: {"courseids":["<>"]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        contextlevel=10
        instanceid=0
        datadicts=[]
        try:
            systemusersdicts=self.get_context_all_users_and_roles(contextlevel, instanceid)['response']
            for courseid in courseids:
                for dct in systemusersdicts:
                    datadicts+=[{"courseid":courseid, 'userid':dct['userid'], 'roleid':dct['roleid']}]
            response=self.manual_enrol_users_in_courses(datadicts)['response']
            status='success'
            #response=datadicts
        except:
            pass
        return {'status':status,'response':response}

    def manual_enrol_users_in_course_in_role(self,courseid,roleid,userids):
        enroldatadicts=[]
        for userid in userids:
            dct={}
            dct['courseid']=courseid
            dct['roleid']=roleid
            dct['userid']=userid
            enroldatadicts+=[dct]
        response=self.manual_enrol_users_in_courses(enroldatadicts)['response']
        status='success'
        return {'status':status,'response':response}

    def manual_unenrol_users_in_courses(self,datadicts):
        '''
        Webserice call: {"datadicts":[{'courseid':courseid, 'userid':userid, 'roleid':roleid}]}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'enrol_manual_unenrol_users',enrolments=datadicts)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def manual_enrol_user_in_course(self,coursename,username,roleid):
        '''
        Webserice call: {"coursename":<Course short name>,"username":<username>,"userrole":<User role short name>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            contentDict=[crs for crs in self.call(self.mWAP,'core_course_search_courses',criterianame='search',criteriavalue=coursename)['courses'] if crs['shortname']==coursename][0]
            contentID=contentDict['id'] 
            
            userInfo=[usr for usr in self.call(self.mWAP,'core_user_get_users',criteria=[{'key':'username','value':username}])['users'] if usr['username']==username][0]
            userID=userInfo['id']
            roleID=roleid #read_sql(sql_text('SELECT id FROM mdl_role WHERE shortname="{}"'.format(userrole)),self.engine)['id'].values[0] #TEAL2.O Teacher
            enrolmentList=[{'courseid':contentID, 'userid':userID, 'roleid':roleID}]
            response=self.call(self.mWAP,'enrol_manual_enrol_users',enrolments=enrolmentList)
            status='success'
            print(response)
        except:
            pass
        return {'status':status,'response':response}

    def manual_unenrol_user_in_course(self,coursename,username,roleid):
        '''
        Webserice call: {"coursename":<Course short name>,"username":<Cohort username>,"userrole":<User role short name>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            contentDict=[crs for crs in self.call(self.mWAP,'core_course_search_courses',criterianame='search',criteriavalue=coursename)['courses'] if crs['shortname']==coursename][0]
            contentID=contentDict['id'] 
            
            userInfo=[usr for usr in self.call(self.mWAP,'core_user_get_users',criteria=[{'key':'username','value':username}])['users'] if usr['username']==username][0]
            userID=userInfo['id']
            roleID=roleid #read_sql(sql_text('SELECT id FROM mdl_role WHERE shortname="{}"'.format(userrole)),self.engine)['id'].values[0] #TEAL2.O Teacher
            enrolmentList=[{'courseid':contentID, 'userid':userID, 'roleid':roleID}]
            response=self.call(self.mWAP,'enrol_manual_unenrol_users',enrolments=enrolmentList)
            status='success'
            response=datadicts
        except:
            pass
        return {'status':status,'response':response}

    def get_course_users_by_rolename(self,courseid,rolename):
        '''
        Webserice call: {"courseid":<courseid>, "rolename":<rolename>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            courseUsers=self.call(self.mWAP,'core_enrol_get_enrolled_users',courseid=courseid)
            response=[usr for usr in courseUsers if rolename in [rls['shortname'] for rls in usr['roles']]]
            status='success'
        except:
            pass

        return {'status':status,'response':response}  

##############################
##Cohort create/edit/add functions
################################
    def get_cohorts(self):
        '''
        Webserice call: {}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_cohort_get_cohorts')
            status="success"
        except:
            pass
        return {'status':status,'response':response}

    def get_cohort_members(self,cohortids):
        '''
        Webserice call: {cohortids:<list of cohort ids>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            response=self.call(self.mWAP,'core_cohort_get_cohort_members',cohortids=cohortids)
            status="success"
        except:
            pass
        return {'status':status,'response':response}        

    def create_cohorts(self,datadicts):
        '''
        Webserice call: {"datadicts":[list of ->{"cohortype":<category type - str->(id, idnumber, system)>,"typevalue":<category id - int>,"cohortname":<Cohort name>,"cohortid":<cohort idnumber - str>}]}
        Response: {'status':status,'response':response}
        '''
        cohortsdict=datadicts
        response=[]
        status="error"
        try:
            cohorts=[{'categorytype': {'type':dct['cohortype'], 'value':str(dct['typevalue'])},'name':dct['cohortname'],'idnumber':dct['cohortid']} for dct in cohortsdict]
            response=self.call(self.mWAP,'core_cohort_create_cohorts',cohorts=cohorts)
            status="success"
        except:
            pass
        return {'status':status,'response':response}

    def create_category_cohorts(self,categoryid,cohortsdict):
        '''
        Webserice call: {"cohortsdict":[list of ->{"cohortname":<Cohort name>,"cohortid":<cohort idnumber - str>}}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            catDicts=self.call(self.mWAP,'core_course_get_categories',criteria=[{'key':'id', 'value':categoryid}])
            if len(catDicts)!=0:
                cohorts=[{'categorytype': {'type':'id', 'value':str(catDicts[0]['id'])},'name':dct['cohortname'],'idnumber':dct['cohortid']} for dct in cohortsdict]
                response=self.call(self.mWAP,'core_cohort_create_cohorts',cohorts=cohorts)
                status="success"
            else:
                status='Category by the id {} does not exist.'.format(categoryid)
        except:
            pass
        return {'status':status,'response':response}

    def add_cohort_members(self,cohortid,memberids):
        '''
        Webserice call: {cohortid:<cohort idnumber>, 'memberids':<list of member ids>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            cohortmembers=[{'cohorttype':{'type':'idnumber','value':str(cohortid)},'usertype':{'type':'id','value':str(usrid)}} for usrid in memberids]
            response=self.call(self.mWAP,'core_cohort_add_cohort_members',members=cohortmembers)
            status="success"
        except:
            pass
        return {'status':status,'response':response}   
    
    def delete_cohort_members(self,cohortid,memberids):
        '''
        Webserice call: {cohortid:<cohort idnumber>, 'memberids':<list of member ids>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            cohortmembers=[{'cohortid':cohortid,'userid':usrid} for usrid in memberids]
            response=self.call(self.mWAP,'core_cohort_delete_cohort_members',members=cohortmembers)
            status="success"
        except:
            pass
        return {'status':status,'response':response}   

####################################################
#Manual Moodle Actions
####################################################

    def view_course(self,courseid,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'course/view.php?id={}'.format(courseid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def view_module(self,moduleid,siteurl):
        response=[]
        status="error"
        try:
            response=self.get_course_module_by_id(moduleid)['response']
            response=siteurl+'mod/{}/view.php?id={}'.format(response[0]['modname'],moduleid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def view_my_courses_moodle(self,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'my/courses.php'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def edit_course(self,courseid,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'course/edit.php?id={}'.format(courseid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def edit_course_section(self, sectionid, siteurl):
        #Edits course section metadata 
        response=[]
        status='error'
        try:
            response=siteurl+'course/editsection.php?id={}&sr=0'.format(sectionid)
            status='success'
        except:
            pass
        return {'status':status,'response':response} 

    def edit_module(self,moduleid,siteurl):
        response=[]
        status="error"
        try:
            response=siteurl+'course/modedit.php?update={}&return=1'.format(moduleid)
            status='success'            
        except:
            pass
        return {'status':status,'response':response}        

    def edit_module_role_assignments(self,moduleid,siteurl):
        response=[]
        status="error"
        try:
            contextlevel=70
            contextid=self.get_module_contextid(moduleid,contextlevel)['response']   #self.get_module_full_info_by_id(moduleid)['response']['contextid']
            response=siteurl+'admin/roles/assign.php?contextid={}'.format(contextid)
            status='success'            
        except:
            pass
        return {'status':status,'response':response} 

    def enrol_users_in_course(self,courseid,siteurl):
        response=[]
        status="error"
        try:
            response=siteurl+'user/index.php?id={}'.format(courseid)
        except:
            pass
        return {'status':status,'response':response}

    def edit_course_categories(self,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'course/management.php'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_dashboard(self,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'my/'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def get_mycourses_link(self,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'my/courses.php'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def manage_category_roles(self,categoryid,siteurl):
        response=[]
        status='error'
        try:
            contextlevel=40
            contextid=self.get_category_contextid(categoryid,contextlevel)['response']   #self.get_module_full_info_by_id(moduleid)['response']['contextid']
            response=siteurl+'admin/roles/assign.php?contextid={}'.format(contextid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def manage_category_cohorts(self,categoryid,siteurl):
        response=[]
        status='error'
        try:
            contextlevel=40
            contextid=self.get_category_contextid(categoryid,contextlevel)['response']   #self.get_module_full_info_by_id(moduleid)['response']['contextid']
            response=siteurl+'cohort/index.php?contextid={}'.format(contextid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def manage_category_courses(self,categoryid,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'course/management.php?categoryid={}'.format(categoryid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def view_course_category(self,categoryid,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'course/index.php?categoryid={}'.format(categoryid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def edit_course_category_old(self,categoryid,siteurl):
        response=[]
        status='error'
        try:
            response=siteurl+'course/editcategory.php?id={}'.format(categoryid)
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def create_course_categories(self,siteurl):
        response=siteurl+'course/editcategory.php?parent=0'
        status='success'
        return {'status':status,'response':response}

    def add_activity_module_2_course_section(self,modname,courseid,sectionid,siteurl):
        response="[]"
        status="error"
        try:
            sectionnumber=self.get_course_section_from_section_id(sectionid)['response']['section']
            response=siteurl+'course/modedit.php?add={}&type=&course={}&section={}&return=0&sr=0'.format(modname,courseid,sectionnumber)
            status='success'
        except:
            pass
        return {'status':status,'response':response}        

########################
#Manual user actions
######################################

    def bulk_user_actions(self,siteurl):
        response=[]
        status="error"
        try:
            response=siteurl+'admin/user/user_bulk.php'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def upload_users(self,siteurl):
        response=[]
        status="error"
        try:
            response=siteurl+'admin/tool/uploaduser/index.php'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def view_add_cohorts(self,siteurl):
        response=[]
        status="error"
        try:
            response=siteurl+'cohort/index.php'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def view_add_users(self,siteurl):
        response=[]
        status="error"
        try:
            response=siteurl+'admin/user.php'
            #response=siteurl+'admin/category.php?category=accounts'
            status='success'
        except:
            pass
        return {'status':status,'response':response}

#########################################################
#LLS
#########################################################
    def get_cobds(self,courseids):
        response=[]
        status='error'
        try:    
            assignPDF=DataFrame(self.get_course_assignment_local_roles_full_info(courseids)['response']).round({'grade':0})
            
            if len(assignPDF)!=0:
                assignPDF.loc[assignPDF['gradetype']!=1,'grademax']=0
                assignColumnsRenameDict={'moduleid':'moduleid','categoryname':'client','coursename':'program','sectionname':'section','activityname':'activity','activityintro':'description','activity':'tasks','duedate':'datetime','useremail':'assignedto','roleshortname':'roleshortname','grade':'cost/trainer','grademax':'cost/client','dropdown':'status'}
                if 'dropdown' not in [*assignPDF]:
                    assignPDF['dropdown']='Pending'
                renamedAssignPDF=assignPDF[[*assignColumnsRenameDict]].fillna(0).copy(deep=True)
                renamedAssignPDF.rename(columns = assignColumnsRenameDict, inplace = True)
                renamedAssignPDF['description'] = renamedAssignPDF['description'].str.replace(r'<[^<>]*>', '', regex=True)

                assignids=list(set(renamedAssignPDF['moduleid'].to_list()))
                if len(assignids)!=0:
                    evaluatorsPDF=DataFrame(self.get_assignment_local_roles_full_info_by_modules(assignids)['response'])
                    for assignid in assignids:
                        #assignEvaluators=renamedAssignPDF[(renamedAssignPDF['moduleid']==assignid) & (renamedAssignPDF['roleshortname']=='evaluator')] #.to_dict(orient='records')
                        #assignEvaluators=evaluatorsPDF[(evaluatorsPDF['moduleid']==assignid) & (evaluatorsPDF['roleshortname']=='evaluator')] #.to_dict(orient='records')
                        #assignParticipants=renamedAssignPDF[(renamedAssignPDF['moduleid']==assignid) & (renamedAssignPDF['roleshortname']=='participant')]
                        assignEvaluators=evaluatorsPDF[(evaluatorsPDF['moduleid']==assignid) & (evaluatorsPDF['roleshortname'].isin(['evaluator','editingteacher']))] #.to_dict(orient='records')
                        assignParticipants=renamedAssignPDF[(renamedAssignPDF['moduleid']==assignid) & (renamedAssignPDF['roleshortname'].isin(['participant','student']))]
                        tmpdct={'evaluator/trainer':'','participant':'','cost/trainer':0,'cost/client':0}
                        tmpdct2={}
                        if len(assignEvaluators)!=0:
                            tmpdct=assignEvaluators.to_dict(orient='records')[0]
                            tmpdct['evaluator/trainer']=', '.join(assignEvaluators['useremail'].to_list())
                            #tmpdct['cost']=sum(assignEvaluators['grademax'].to_list())
                        if len(assignParticipants)!=0:
                            tmpdct2=assignParticipants.to_dict(orient='records')[0]
                            tmpdct2['participant']=', '.join(assignParticipants['assignedto'].to_list())
                            tmpdct2['cost/trainer']=sum(assignParticipants['cost/trainer'].to_list())
                            if len(assignParticipants['cost/client'].to_list())!=0:
                                tmpdct2['cost/client']=assignParticipants['cost/client'].to_list()[0] #sum(assignParticipants['cost/client'].to_list())        
                            else:
                                tmpdct2['cost/client']=0
                            tmpdct.update(tmpdct2)
                            assignmentdct=copy.deepcopy(tmpdct)
                            #assignmentdct['cost']=tmpdct['cost']
                            for ky in ['moduleid','roleshortname']:
                                assignmentdct.pop(ky)
                            response+=[assignmentdct]
                    tempPDF=DataFrame(response).fillna('')
                    tempPDF[['mode', 'location', 'duration']]='NA'
                    response=tempPDF.to_dict(orient='records')
        except:
            pass

        try:
            systemusers=DataFrame(self.get_context_all_users_and_roles(10, 0)['response'])['userid'].to_list()
            tempPDFSched=DataFrame(self.get_course_scheduler_events_full_info(courseids)['response']).fillna(0)
            if len(tempPDFSched) !=0:
                schedulerPDF=tempPDFSched[~tempPDFSched['studentid'].isin(systemusers)]
                if len(schedulerPDF)!=0:
                    if 'dropdown' not in [*schedulerPDF]:
                        schedulerPDF['dropdown']='Pending'
                    schedulerColumnsRenameDict={'categoryname':'client','coursename':'program','sectionname':'section','schedulername':'activity','schedulerintro':'description','appointmentnote':'tasks','appointmentlocation':'mode','schedulenotes':'location','starttime':'datetime','duration':'duration','teacher':'evaluator/trainer','student':'participant','grade':'cost/trainer','grademax':'cost/client','dropdown':'status'}
                    renamedSchedulerPDF=schedulerPDF[[*schedulerColumnsRenameDict]].copy(deep=True)
                    renamedSchedulerPDF.rename(columns = schedulerColumnsRenameDict, inplace = True)
                    response+=renamedSchedulerPDF.to_dict(orient='records')
        except:
            pass         

        try:
            columnNames=['client','program','section','activity','description','tasks','mode','location','datetime','duration','evaluator/trainer','participant','cost/trainer','cost/client','status']
            responsePDF=DataFrame(response).fillna('')[columnNames]
            responsePDF.loc[responsePDF['status']==0,'status']='Pending'
            #responsePDF['cost/check']=responsePDF['cost/client']>2*1.1*responsePDF['cost/trainer']
            #responsePDF['cost/trainer']=responsePDF['cost/trainer']*100
            #responsePDF['cost/client']=responsePDF['cost/client']*100
            response=responsePDF.to_dict(orient='records')
        except:
            pass
        return {'status':status,'response':response}

    def get_program_users_assignments_schedules_info(self,courseids,userids):
        rolename="participant"
        newColumnNames={'sectionname':'section','activityname':'activityname','activityintro':'description','activity':'tasks','useremail':'assignedto','allowsubmissionsfromdate':'assignedon','duedate':'duedate', 'gradingduedate':'evaluateby','grade':'cost'}
        response1PDF=DataFrame(self.get_course_assignment_local_roles_full_info_by_role_by_userids(courseids,userids,rolename)['response'])[[*newColumnNames]]
        response1=response1PDF.rename(columns = newColumnNames).to_dict(orient='records')

        rolename="student"
        newColumnNames2={'sectionname':'section','schedulername':'topic','schedulerintro':'description','schedulenotes':'schedulenotes','appointmentlocation':'mode','appointmentnote':'location','starttime':'starttime','duration':'duration','teacher':'assignedto','student':'participant','grade':'cost','attended':'completed'}
        response2PDF=DataFrame(self.get_course_scheduler_events_full_info_by_role_by_userids(courseids,userids,rolename)['response'])[[*newColumnNames2]]
        response2=response2PDF.rename(columns = newColumnNames2).to_dict(orient='records')
        status='success'
        response={'assignments':response1,'schedules':response2}                  
        return {'status':status,'response':response}

#####################################################
#Not used
#####################################################  
    def create_course_categories_moodle(webserviceAccessParams,categoryStructureDict):
        response=[]
        category_structure_PDF=pd.DataFrame(categoryStructureDict)
        categoryLevels=[*category_structure_PDF]
        categoryIds={}
        proviousLevel=[]
        previousLevel=''
        for level in categoryLevels:
            levelCategoryData=[]
            catGps=list(set(category_structure_PDF[level].to_list()))
            catGps.sort()
            for catName in catGps:
                if level==categoryLevels[0]:
                    parentId=0
                else:
                    parentLevel=list(set(category_structure_PDF[category_structure_PDF[level]==catName][previousLevel].to_list()))[0]
                    parentId=categoryIds[parentLevel]
                levelCategoryData.append({'name':catName,'idnumber':'','description':'','descriptionformat': 1, 'parent': parentId,'theme':''})
            #print(levelCategoryData)
            resp=call(webserviceAccessParams,'core_course_create_categories', categories=levelCategoryData)
            for dct in resp:
                categoryIds[dct['name']]=dct['id']

            previousLevel=level
            response.append(resp)
        return

    def update_course_category_name(self,categoryid,newcategoryname):
        #{"description":"","id":17,"idnumber":"","name":"what da","timemodified":1678874400,"visible":1,"visibleold":1}
        #update_course_category_name {"categoryid":37,"newcategoryname":"New Category Name2-Morning"}
        tablename='mdl_course_categories'
        filterDict={"id":categoryid}
        updateStrDict={"name":newcategoryname}
        updateNumericDict={}
        updateTimeStrDict={"timemodified":datetime.now(tz=pytz.timezone("Asia/Colombo")).strftime("%d/%m/%Y %H%M%S")}
        status='error'
        response=[]
        try:
            response=self.update_table_record(tablename, filterDict, updateStrDict,updateNumericDict,updateTimeStrDict)
            status:'success'
        except:
            pass      
        return {'status':status,'response':response}

    def course_content_GitHub_push(self,coursename,updatecomment):
        response=[]
        status='error'
        parameters={'access_parameters':{'gToken':self.GHAP['gToken'], 'gUser':self.GHAP['gUser']}, 'repoName':coursename, 'updateComment':updatecomment}
        webserviceAccessParams=self.mWAP
        chosenContentDict=[crs for crs in self.call(webserviceAccessParams,'core_course_search_courses',criterianame='search',criteriavalue=coursename)['courses'] if crs['shortname']==coursename][0]
        contentMetaDataSummaryJSON=json.dumps(chosenContentDict,indent=2)
        parameters['fileInfoDict']={'filename':'contentMetaDataSummary.json', 'filecontent':contentMetaDataSummaryJSON}
        response.append(self.mgGH.create_update_GITHUB_organization_repos(parameters))
        chosenContentId=chosenContentDict['id']
        
        chosenContentFullDict=self.call(webserviceAccessParams,'core_course_get_courses',options={'ids':[chosenContentId]})
        contentMetaDataJSON=json.dumps(chosenContentFullDict,indent=2)
        parameters['fileInfoDict']={'filename':'contentMetaData.json', 'filecontent':contentMetaDataJSON}
        response.append(self.mgGH.create_update_GITHUB_organization_repos(parameters))

        chosenContentSecns=self.call(webserviceAccessParams,'core_course_get_contents',courseid=chosenContentId)
        contentSecnsJSON=json.dumps(chosenContentSecns,indent=2)
        parameters['fileInfoDict']={'filename':'contentSecnsSummary.json', 'filecontent':contentSecnsJSON}
        response.append(self.mgGH.create_update_GITHUB_organization_repos(parameters))

        self.engine.dispose()
        con=self.engine.connect()

        for section in [{'id':secn['id'],'name':secn['name'], 'modules':secn['modules']} for secn in self.call(webserviceAccessParams,'core_course_get_contents',courseid=chosenContentId)]:
            for module in section['modules']:

                fileDict=read_sql(sql_text('SELECT * FROM mdl_{} WHERE id={}'.format(module['modname'],module['instance'])),con).to_dict(orient='records')[0]
                
                if module['modname']=='hvp':
                    mainLibraryID=fileDict['main_library_id']
                    fileDict['main_library_id']=read_sql(sql_text('SELECT * FROM mdl_hvp_libraries WHERE id={}'.format(mainLibraryID)),con).to_dict(orient='records')[0]
                
                fileJSON=json.dumps(fileDict,indent=2)
                #parametersV2={'moduleType':'hvp','access_parameters':parameters['access_parameters'], 'repoName':contentShortName, 'fileInfoDict':{'filename':'section_'+str(section['id'])+'_content/'+module['modname']+'.json', 'filecontent':fileJSON}, 'updateComment':parameters['updateComment']}
                parametersV2={'access_parameters':parameters['access_parameters'], 'repoName':contentShortName, 'fileInfoDict':{'filename':'section_'+str(section['id'])+'_content/'+'mod_'+str(module['id'])+'_'+module['modname']+'_'+str(module['instance'])+'.json', 'filecontent':fileJSON}, 'updateComment':parameters['updateComment']}
                response.append(self.mgGH.create_update_GITHUB_organization_repos(parametersV2))
        status='success'
        con.close()    
        return {'status':status,'response':response}

    def copy_from_template_and_update_course_module_from_GitHub(self,templatename,coursename,sectionname,modtype,githubpullmoddict):
        chosenCourseShortName=coursename
        sectionName=sectionname #parameters['sectionName']
        chosenModType=modtype #parameters['chosenModType']
        githubPullModDict=githubpullmoddict #parameters['githubPullModDict']
        chosenCourseModules=self.get_course_modules(chosenCourseShortName)
        chosenCourseTemplateModules=[tmplCm for tmplCm in chosenCourseModules if tmplCm['sectionname']==sectionName][0]['sectionmodules']
        mod2Duplicate=[mod for mod in chosenCourseTemplateModules if mod['modname']==chosenModType]
        self.call(self.mWAP,'core_course_edit_module',action='duplicate',id=mod2Duplicate[0]['id'])
        updatedCourseModules=self.get_course_modules(chosenCourseShortName)
        copiedSectionModules0=[tmplCm for tmplCm in updatedCourseModules if tmplCm['sectionname']==sectionName][0]['sectionmodules']
        copiedSectionModules=[cCm for cCm in copiedSectionModules0 if  '(copy)' in cCm['name']]
        moduleName=copiedSectionModules[0]['name']
        parametersUpdate={'chosenCourseShortName':chosenCourseShortName,'sectionName':sectionName,'moduleName':moduleName,'webserviceAccessParams':self.mWAP,'githubPullModDict':githubPullModDict}   
        response=self.update_course_module_from_GitHub(coursename,sectionname,modulename,githubpullmoddict)
        status='success'
        return {'status':status, 'response':response}

    def update_course_module_from_GitHub(self,coursename,sectionname,modulename,githubpullmoddict): 
        chosenCourseShortName=coursename #parameters['chosenCourseShortName']
        sectionName=sectionname #parameters['sectionName']
        moduleName=modulename #parameters['moduleName']
        chosenCourseSummaryDict=[crs for crs in self.call(self.mWAP,'core_course_search_courses',criterianame='search',criteriavalue=chosenCourseShortName)['courses'] if crs['shortname']==chosenCourseShortName][0]
        chosenCourseModules=self.get_course_modules(chosenCourseShortName)
        sectionModulesInSection=[tmplCm for tmplCm in chosenCourseModules if tmplCm['sectionname']==sectionName][0]['sectionmodules']
        updateModInfoDict=[mod for mod in sectionModulesInSection if mod['name']==moduleName][0]

        githubPullModDict=githubpullmoddict #parameters['githubPullModDict']
        githubPullModDict['id']=updateModInfoDict['instance']
        githubPullModDict['course']=chosenCourseSummaryDict['id']
        githubPullModDict['timemodified']=int(time.mktime(datetime.datetime.now().timetuple()))

        self.engine.dispose()
        con=self.engine.connect()

        if updateModInfoDict['modname']=='hvp':
            hvpMainMachineName=githubPullModDict['main_library_id']['machine_name']
            try:
                githubPullModDict['main_library_id']=read_sql(sql_text('SELECT * FROM mdl_hvp_libraries WHERE machine_name ="{}"'.format(hvpMainMachineName)),con)['id'].to_list()[0]
            except:
                msg=hvpMainMachineName+' HVP machine installed'
            githubPullModDict['filtered']=githubPullModDict['filtered'].replace("'","''")
            githubPullModDict['json_content']=githubPullModDict['json_content'].replace("'","''")

        con.close()

        keysWithoutID=[*githubPullModDict]
        keysWithoutID.remove('id')
        numericFieldsInfoDict={ky:githubPullModDict[ky] for ky in keysWithoutID if type(githubPullModDict[ky]) in [int,float]}
        textFieldsInfoDict={ky:githubPullModDict[ky] for ky in [*githubPullModDict] if type(githubPullModDict[ky])==str}
        params={}
        params['db_table_name']='mdl_'+updateModInfoDict['modname']
        params['filterDict']={'id':updateModInfoDict['instance']}
        params['updateDict']={'numericFieldsInfoDict':numericFieldsInfoDict,'textFieldsInfoDict':textFieldsInfoDict}
        print(params)
        self.mgDB.update_record(self.engine,params)
        response=self.call(self.mWAP,'core_course_edit_module',action='show',id=updateModInfoDict['id'])
        status='success'
        return {'status':status, 'response':response}

    def get_course_users_by_roleV2(self,coursename,rolename):
        '''
        Webserice call: {"coursename":<Course short name>, "rolename":<Role name>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            coursesDict=self.call(self.mWAP,'core_course_search_courses',criterianame='search',criteriavalue=coursename)
            if len(coursesDict['courses'])==0:
                response=[]
                status="No such course in the system"
            else:
                courseDict=[crs for crs in coursesDict['courses'] if crs['shortname']==coursename][0]
                chosenContentID=courseDict['id']
                courseUsers=self.call(self.mWAP,'core_enrol_get_enrolled_users',courseid=chosenContentID)
                response=[usr for usr in courseUsers if rolename in [rls['shortname'] for rls in usr['roles']]]
                status='success'
        except:
            pass

        return {'status':status,'response':response}
      
    def get_course_module_by_section_by_name(self,coursename,secnname,modulename,modvisible=1,secnvisible=1):
        '''
        Webserice call: {"action":<one of hide/show/stealth/duplicate/edit>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            output=self.get_course_modules(coursename, modvisible, secnvisible)
            coursesecns=output['response']
            if len(coursesecns)!=0:
                response=[mod for secn in coursesecns for mod in secn['sectionmodules'] if ((secn['sectionname']==secnname) & (mod['name']==modulename))]
                status='success'
            else:
                response=[]
                status='No module by the name {} in section by the name {}'.format(modulename,secnname)
        except:
            pass

        return {'status':status,'response':response}

    def create_course_section_4m_DB(self,courseid,sectionname,siteurl):
        '''
        Webserice call: {"coursename":<Course id>, "sectionname":<section name>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status='error'
        self.engine.dispose()
        con=self.engine.connect()        
        try:
            chosenContentInfoDict=self.call(self.mWAP,'core_course_get_contents',courseid=courseid)
            crsSections={secn['section']:secn['name'] for secn in chosenContentInfoDict}
            print(crsSections)
            emptySecnDict={'course':courseid,
            'section':[*crsSections][-1]+1,
            'name':sectionname,
            'summary':'',
            'summaryformat':1,
            'sequence':'',
            'visible':0,
            'availability':None,
            'timemodified':int(time.mktime(datetime.now().timetuple()))}
            print(emptySecnDict)
            self.mgDB.insert_record({'db_table_name':"mdl_course_sections",'updateDict':emptySecnDict})
            
            sqlQ='SELECT id from mdl_course_sections WHERE course={} AND name="{}"'.format(courseid,sectionname)
            print(sqlQ)
            sectionid=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0]['id']
            self.edit_course_section_visibility({'action':'show','id':sectionid})['response']
            print(response)
            url=siteurl+'course/edit.php?id={}'.format(courseid)
            status='success'
            response={'sectionid':sectionid,'url':url}
        except:
            pass
        
        con.close()
        return {'status':status,'response':response}

    def get_user_course_lms_interaction(self,userid,courseid,edulevel,startDateStr,endDateStr):
        startDate=to_datetime(startDateStr,dayfirst=True).to_pydatetime()
        endDate=to_datetime(endDateStr,dayfirst=True).to_pydatetime()
        start_date_UNIX=time.mktime(startDate.timetuple())
        end_date_UNIX=time.mktime(endDate.timetuple())
        interactionDict={}
        response=[]
        status="error"
        try:            
            deltaDays=endDate-startDate
            trr_n=startDate
            for dy in range(deltaDays.days+1):
            #print(trr_p.strftime("%d-%m-%Y"))
                print(dy)
                interactionDict[trr_n.strftime("%d-%m-%Y")]=self.get_user_course_lms_interaction_in_a_day(userid,courseid,edulevel,trr_n.strftime("%d-%m-%Y"))
                trr_n=trr_n+DateOffset(days=1)
            response=interactionDict #.to_dict(orient='records')
            status='success'        
        except:
            pass

        return {'status':status,'response':response}

    def get_user_module_lms_interaction(self,userid,courseid,moduleid,edulevel,startDateStr,endDateStr):
        startDate=to_datetime(startDateStr,dayfirst=True).to_pydatetime()
        endDate=to_datetime(endDateStr,dayfirst=True).to_pydatetime()
        start_date_UNIX=time.mktime(startDate.timetuple())
        end_date_UNIX=time.mktime(endDate.timetuple())
        interactionDict={}
        response=[]
        status="error"
        print(start_date_UNIX,end_date_UNIX)
        #try:
        deltaDays=endDate-startDate
        trr_n=startDate
        for dy in range(deltaDays.days+1):
            #print(dy)
            interactionDict[trr_n.strftime("%d-%m-%Y")]=self.get_user_module_lms_interaction_in_a_day(userid,courseid,moduleid,edulevel,trr_n.strftime("%d-%m-%Y"))
            trr_n=trr_n+DateOffset(days=1)
        response=interactionDict #.to_dict(orient='records')
        #print(response)
        status='success'        
        #except:
            #pass
        response={dy:response[dy]['response'] for dy in [*response] if len(response[dy]['response'])!=0}
        return {'status':status,'response':response}

    def get_user_module_lms_interaction_graph(self,userid,courseid,moduleid,edulevel,startDateStr,endDateStr):
        modinteractionOutput=self.get_user_module_lms_interaction(userid,courseid,moduleid,edulevel,startDateStr,endDateStr)
        output={'status':modinteractionOutput['status'],'response':modinteractionOutput['response']}
        modInteractions=modinteractionOutput['response']
        fig=go.Figure()
        fig_mod=go.Figure()

        activityList0=list(set([bb[1] for bb in [aa.split('/') for aa in self.get_keys(modInteractions)] if len(bb)>1]))
        if 'core' in activityList0:
            activityList0.remove('core')
        activityList0.sort()
        activityList=[z for z in activityList0 if 'mod_' not in z]
        modList=[z for z in activityList0 if 'mod_' in z]
        x=[]
        for activity in activityList:
            xtemp=0
            for dy in [*modInteractions]:
                if activity in [*modInteractions[dy]]:
                    xtemp+=modInteractions[dy][activity]
                else:
                    xtemp+=0
            x+=[xtemp]

        fig.add_trace(go.Bar(y=[' '.join(zz.split('_')) for zz in activityList],x=x,name='Test',orientation='h'))
        for activity in modList:    
            xm=[]
            for dy in [*modInteractions]:
                if activity in [*modInteractions[dy]]:
                    xm+=[modInteractions[dy][activity]]
                else:
                    xm+=0
            fig_mod.add_trace(go.Bar(x=[*modInteractions],y=xm,name=' '.join(activity.split('_'))))

        fig.update_layout(barmode='stack',title='Interaction statistics',xaxis_title='Number of activities')
        fig_mod.update_layout(barmode='stack',title='Number of hours spent',yaxis_title='Number of hours spent')
        output['response']={'mod_interaction_statistics':fig.to_plotly_json(),'mod_hours_spent':fig_mod.to_plotly_json()}
        return output

    def get_user_module_lms_interaction_graph_fig(self,userid,courseid,moduleid,edulevel,startDateStr,endDateStr):
        modinteractionOutput=self.get_user_module_lms_interaction(userid,courseid,moduleid,edulevel,startDateStr,endDateStr)
        output={'status':modinteractionOutput['status'],'response':modinteractionOutput['response']}
        #print(output)
        modInteractions=modinteractionOutput['response']
        fig=go.Figure()
        fig_mod=go.Figure()
        try:
            activityList0=list(set([bb[1] for bb in [aa.split('/') for aa in self.get_keys(modInteractions)] if len(bb)>1]))
            if 'core' in activityList0:
                activityList0.remove('core')
            activityList0.sort()
            activityList=[z for z in activityList0 if 'mod_' not in z]
            modList=[z for z in activityList0 if 'mod_' in z]
            x=[]
            for activity in activityList:
                xtemp=0
                for dy in [*modInteractions]:
                    if activity in [*modInteractions[dy]]:
                        xtemp+=modInteractions[dy][activity]
                    else:
                        xtemp+=0
                x+=[xtemp]

            fig.add_trace(go.Bar(y=[' '.join(zz.split('_')) for zz in activityList],x=x,name='Test',orientation='h'))
            for activity in modList:    
                xm=[]
                for dy in [*modInteractions]:
                    if activity in [*modInteractions[dy]]:
                        xm+=[modInteractions[dy][activity]]
                    else:
                        xm+=0
                fig_mod.add_trace(go.Bar(x=[*modInteractions],y=xm,name=' '.join(activity.split('_'))))

            fig.update_layout(barmode='stack',title='Interaction statistics',xaxis_title='Number of activities')
            fig_mod.update_layout(barmode='stack',title='Number of hours spent',yaxis_title='Number of hours spent')
        except:
            psss
        fig_mod.add_trace(go.Bar(x=['A','B'],y=[2,3],name='something'))
        print('here')
        output['response']={'mod_interaction_statistics':fig,'mod_hours_spent':fig_mod}
        return output        

    def get_user_module_lms_daily_interaction_graph(self,userid,courseid,moduleid,edulevel,startDateStr,endDateStr):
        modinteractionOutput=self.get_user_module_lms_interaction(userid,courseid,moduleid,edulevel,startDateStr,endDateStr)
        output={'status':modinteractionOutput['status'],'response':modinteractionOutput['response']}
        modInteractions=modinteractionOutput['response']
        fig=go.Figure()
        fig_mod=go.Figure()
        y=[*modInteractions]
        activityList0=list(set([bb[1] for bb in [aa.split('/') for aa in self.get_keys(modInteractions)] if len(bb)>1]))
        if 'core' in activityList0:
            activityList0.remove('core')
        activityList0.sort()
        activityList=[z for z in activityList0 if 'mod_' not in z]
        modList=[z for z in activityList0 if 'mod_' in z]
        for activity in activityList:
            x=[]
            for dy in y:
                if activity in [*modInteractions[dy]]:
                    x+=[modInteractions[dy][activity]]
                else:
                    x+=[0]
            fig.add_trace(go.Bar(x=y,y=x,name=' '.join(activity.split('_'))))
        for activity in modList:    
            xm=[]
            for dy in y:
                if activity in [*modInteractions[dy]]:
                    xm+=[modInteractions[dy][activity]]
                else:
                    xm+=0
            fig_mod.add_trace(go.Bar(x=y,y=xm,name=' '.join(activity.split('_'))))
        print('here')
        fig.update_layout(barmode='stack',title='Interaction statistics')
        fig_mod.update_layout(barmode='stack',title='Number of hours spent')
        output['response']={'mod_interaction_statistics':fig.to_plotly_json(),'mod_hours_spent':fig_mod.to_plotly_json(),}
        return output

    def get_user_lms_interaction_in_a_day(self,userid,edulevel,dateStr):
        interactionDict={}
        response=[]
        status="error"

        date=to_datetime(dateStr,dayfirst=True).to_pydatetime()
        date_UNIX=time.mktime(date.timetuple())

        dateP1=(to_datetime(dateStr,dayfirst=True)+DateOffset(days=1)).to_pydatetime()
        dateP1_UNIX=time.mktime(dateP1.timetuple())

        parameters={"db_table_name":"mdl_logstore_standard_log","returnColumns":["*"],"filterDict":{"userid":userid},"colName":"timecreated","startVal":date_UNIX,"endVal":dateP1_UNIX}
        userDataPDF=DataFrame(self.mgDB.get_filtered_records_between_ranges(parameters)['response'])
        if len(userDataPDF)!=0:
            studentInteraction={}# pd.DataFrame(np.zeros([1,len(columnsList)]),index=[chosenUser], columns=columnsList)
            print(userDataPDF)
            usrwisePDF=userDataPDF.sort_values(by='timecreated').copy(deep=True)
            usrwisePDF['eventname']=usrwisePDF['eventname'].str.split('\\',expand=True)[3]               
            cn=to_datetime(usrwisePDF['timecreated'], unit='s',utc=True).dt.tz_convert('Asia/Colombo').to_list()

            cp=[cn[0]]+cn[:-1]
            trr=to_datetime(cn, dayfirst=True).to_pydatetime()-to_datetime(cp, dayfirst=True).to_pydatetime()
            tru=trr.tolist()
            usrwisePDF['usrdt']=[float("{:.2f}".format(((dt.seconds/60.)%30)/60.)) for dt in tru]
            for cid in list(set(usrwisePDF['courseid'].to_list())):
                studentInteraction[cid]={}
                cuwisePDF=usrwisePDF[(usrwisePDF['courseid']==cid) & (usrwisePDF['edulevel']==edulevel)]
                selectedLearningEventsList=list(set(cuwisePDF['eventname'].to_list()))
                selectedLearningEventsList.sort()
                componentList=list(set(cuwisePDF['component'].to_list()))
                componentList.sort() 

                for lbl in componentList:
                    studentInteraction[cid][lbl]=sum(cuwisePDF[cuwisePDF['component']==lbl]['usrdt'].to_list())
                for lbl in selectedLearningEventsList:
                    studentInteraction[cid][lbl]=len(cuwisePDF[cuwisePDF['eventname']==lbl])
            response=studentInteraction
            status="success"

        else:
            response=[]
            status="No user activity"   
            
        #print(studentInteraction)
        #print(usrwisePDF)
        #aastudentPDF=DataFrame(aastudent,index=[0])
        #aastudentPDF['Total time spent/ Hrs']=aastudentPDF[componentList].sum(axis=1).to_list() 
        #numberofUsrActivityPDF=self.grouped_itemized_PDFs(userDataPDF, 'Event name', selectedLearningEventsList, None, username)
        #numberofUsrActivityPDF['Total number of activities']=numberofUsrActivityPDF.sum(axis=1).to_list()
        return {'status':status,'response':response} #concat([aastudentPDF,DataFrame(numberofUsrActivityPDF.to_dict(orient='records'),index=[0])],axis=1)

    def get_user_course_lms_interaction_in_a_day(self,userid,courseid,edulevel,dateStr):
        interactionDict={}
        response=[]
        status="error"

        date=to_datetime(dateStr,dayfirst=True).to_pydatetime()
        date_UNIX=time.mktime(date.timetuple())

        dateP1=(to_datetime(dateStr,dayfirst=True)+DateOffset(days=1)).to_pydatetime()
        dateP1_UNIX=time.mktime(dateP1.timetuple())
        parameters={"db_table_name":"mdl_logstore_standard_log","returnColumns":["*"],"filterDict":{"userid":userid},"colName":"timecreated","startVal":date_UNIX,"endVal":dateP1_UNIX}
        userDataPDF=DataFrame(self.mgDB.get_filtered_records_between_ranges(parameters)['response'])
        if len(userDataPDF)!=0:
            studentInteraction={}# pd.DataFrame(np.zeros([1,len(columnsList)]),index=[chosenUser], columns=columnsList)
            usrwisePDF=userDataPDF.sort_values(by='timecreated').copy(deep=True)
            print(usrwisePDF['courseid'])
            usrwisePDF['eventname']=usrwisePDF['eventname'].str.split('\\',expand=True)[3]               
            cn=to_datetime(usrwisePDF['timecreated'], unit='s',utc=True).dt.tz_convert('Asia/Colombo').to_list()

            cp=[cn[0]]+cn[:-1]
            trr=to_datetime(cn, dayfirst=True).to_pydatetime()-to_datetime(cp, dayfirst=True).to_pydatetime()
            tru=trr.tolist()
            usrwisePDF['usrdt']=[float("{:.2f}".format(((dt.seconds/60.)%30)/60.)) for dt in tru]
            
            scInteraction={}
            cuwisePDF=usrwisePDF[(usrwisePDF['courseid']==courseid) & (usrwisePDF['edulevel']==edulevel)]
            print(cuwisePDF)
            selectedLearningEventsList=list(set(cuwisePDF['eventname'].to_list()))
            selectedLearningEventsList.sort()
            componentList=list(set(cuwisePDF['component'].to_list()))
            componentList.sort() 

            for lbl in componentList:
                scInteraction[lbl]=sum(cuwisePDF[cuwisePDF['component']==lbl]['usrdt'].to_list())
            for lbl in selectedLearningEventsList:
                scInteraction[lbl]=len(cuwisePDF[cuwisePDF['eventname']==lbl])
            response=scInteraction
            status="success"

        else:
            response=[]
            status="No user activity"   
                
        #print(studentInteraction)
        #print(usrwisePDF)
        #aastudentPDF=DataFrame(aastudent,index=[0])
        #aastudentPDF['Total time spent/ Hrs']=aastudentPDF[componentList].sum(axis=1).to_list() 
        #numberofUsrActivityPDF=self.grouped_itemized_PDFs(userDataPDF, 'Event name', selectedLearningEventsList, None, username)
        #numberofUsrActivityPDF['Total number of activities']=numberofUsrActivityPDF.sum(axis=1).to_list()
        return {'status':status,'response':response} #concat([aastudentPDF,DataFrame(numberofUsrActivityPDF.to_dict(orient='records'),index=[0])],axis=1)
    
    def get_user_module_lms_interaction_in_a_day(self,userid,courseid,moduleid,edulevel,dateStr):
        interactionDict={}
        response=[]
        status="error"
        date=to_datetime(dateStr,dayfirst=True).to_pydatetime()
        date_UNIX=time.mktime(date.timetuple())
        dateP1=(to_datetime(dateStr,dayfirst=True)+DateOffset(days=1)).to_pydatetime()
        dateP1_UNIX=time.mktime(dateP1.timetuple())
        parameters={"db_table_name":"mdl_logstore_standard_log","returnColumns":["*"],"filterDict":{"userid":userid},"colName":"timecreated","startVal":date_UNIX,"endVal":dateP1_UNIX}
        userDataPDF=DataFrame(self.mgDB.get_filtered_records_between_ranges(parameters)['response'])
        if len(userDataPDF)!=0:
            studentInteraction={}# pd.DataFrame(np.zeros([1,len(columnsList)]),index=[chosenUser], columns=columnsList)
            usrwisePDF=userDataPDF.sort_values(by='timecreated').copy(deep=True)
            usrwisePDF['eventname']=usrwisePDF['eventname'].str.split('\\',expand=True)[3]            
            cn=to_datetime(usrwisePDF['timecreated'], unit='s',utc=True).dt.tz_convert('Asia/Colombo').to_list()
            cp=[cn[0]]+cn[:-1]
            trr=to_datetime(cn, dayfirst=True).to_pydatetime()-to_datetime(cp, dayfirst=True).to_pydatetime()
            tru=trr.tolist()
            usrwisePDF['usrdt']=[float("{:.2f}".format(((dt.seconds/60.)%30)/60.)) for dt in tru]
            #print(usrwisePDF)
            scInteraction={}
            cuwisePDF=usrwisePDF[(usrwisePDF['contextinstanceid']==moduleid) & (usrwisePDF['edulevel']==edulevel)]
            #print(cuwisePDF)
            selectedLearningEventsList=list(set(cuwisePDF['eventname'].to_list()))
            selectedLearningEventsList.sort()
            componentList=list(set(cuwisePDF['component'].to_list()))
            componentList.sort() 

            for lbl in componentList:
                scInteraction[lbl]=sum(cuwisePDF[cuwisePDF['component']==lbl]['usrdt'].to_list())
            for lbl in selectedLearningEventsList:
                scInteraction[lbl]=len(cuwisePDF[cuwisePDF['eventname']==lbl])
            response=scInteraction
            status="success"

        else:
            response=[]
            status="No user activity"   
                
        #print(studentInteraction)
        #print(usrwisePDF)
        #aastudentPDF=DataFrame(aastudent,index=[0])
        #aastudentPDF['Total time spent/ Hrs']=aastudentPDF[componentList].sum(axis=1).to_list() 
        #numberofUsrActivityPDF=self.grouped_itemized_PDFs(userDataPDF, 'Event name', selectedLearningEventsList, None, username)
        #numberofUsrActivityPDF['Total number of activities']=numberofUsrActivityPDF.sum(axis=1).to_list()
        return {'status':status,'response':response} #concat([aastudentPDF,DataFrame(numberofUsrActivityPDF.to_dict(orient='records'),index=[0])],axis=1)
    
    def grouped_itemized_PDFs(self, dataPDF, gpFieldName, gpFldList, filterFieldName, filterLabel):
        tempPDF0=dataPDF
        yy1=[]
        aaPDF=DataFrame(yy1) #,index=plotFldList, columns=gpFldList)
        
        if filterFieldName!=None:
            tempPDF0=dataPDF[dataPDF[filterFieldName]==filterLabel]
        
        for xx in gpFldList:
            yy1+=[len(tempPDF0[tempPDF0[gpFieldName]==xx])]

        tmpx0=DataFrame(yy1)
        tmpx00=tmpx0.transpose() #,index=plotFldList, columns=gpFldList)
        aaPDF=DataFrame(tmpx00.to_numpy(),index=[filterLabel], columns=gpFldList)
        return aaPDF   

##########################################################
#DB Manipulation
##########################################################

    def update_table_record_by_id(self, tablename, recordid, updatedict, timestampsdict):
        '''
        Webserice call: {"moduleid":<module id>, "updatedict":<dict of key value pairs to be updated>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        try:
            keyvals=', '.join(['{}={}'.format(ky,updatedict[ky]) for ky in [*updatedict]])
            if len(timestampsdict)!=0:
                keyvals=keyvals+', '+', '.join(['{}={}'.format(ky,int(time.mktime(to_datetime(timestampsdict[ky], errors='raise', dayfirst=True,infer_datetime_format=True).to_pydatetime().timetuple()))) for ky in [*timestampsdict]])
            self.engine.dispose()
            con=self.engine.connect()
            sqlQ='UPDATE {} SET {} WHERE id={}'.format(tablename,keyvals,recordid)
            con.execute(sql_text(sqlQ))
            status='success'
        except:
            pass

        con.close()
        return {'status':status,'response':response}

    def update_table_record(self, tablename, filterDict, updateStrDict,updateNumericDict,updateTimeStrDict):
        '''
        Pass text filter strings as '\"text\"' and time strings with day first
        Ex
        {"tablename":"mdl_course_categories","filterDict":{"name":"\"testcat\""},"updateStrDict":{"name":"\"testcatfromwebservice\""},"updateNumericDict":{},"updateTimeStrDict":{}}
        '''
        filterStrLst=[fltcol+'={}'.format(filterDict[fltcol]) for fltcol in [*filterDict]]
        filterStr=' AND '.join(filterStrLst)
        setText=''
        if len(updateTimeStrDict)!=0:
            setText=', '.join(['{}={}'.format(ky,int(time.mktime(to_datetime(updateTimeStrDict[ky], errors='raise', dayfirst=True,infer_datetime_format=True).to_pydatetime().timetuple()))) for ky in [*updateTimeStrDict]])
        if len(updateStrDict)!=0:
            if setText!='':
                setText=setText+', '
            setText=setText+ ', '.join([xx+"='{}'".format(updateStrDict[xx].replace('\\','\\\\')) for xx in [*updateStrDict]])
        if len(updateNumericDict)!=0:
            if setText!='':
                setText=setText+', '
            setText=setText+ ', '.join([xx+"={}".format(updateNumericDict[xx]) for xx in [*updateNumericDict]])
        
        self.engine.dispose()
        con=self.engine.connect()
        sqlQ="UPDATE {} SET {} WHERE {}".format(tablename,setText,filterStr)
        print(sqlQ)
        con.execute(sql_text(sqlQ))
        con.close()
        return {'status':'SQL querry: {} executed successfully'.format(sqlQ), 'response':[]}




##########################################################
#Youtube Upload
##########################################################

    def upload_youtube(self,youtubeLink,directoryname):
        response=[]
        status="error"
        try:
            if(youtubeLink):
                validateVideoUrl = (
                r'(https?://)?(www\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
                validVideoUrl = re.match(validateVideoUrl, youtubeLink)
                
                if validVideoUrl:
                    # url = YouTube(youtubeLink,use_oauth=True,on_progress_callback = progress_function)
                    url = YouTube(youtubeLink,use_oauth=True)
                    videoTitle=url.title

                    fileName=videoTitle+"_720p.mp4"
                    video = url.streams.filter(res="720p").first()

                    downloadFolder = str(os.path.join(Path.home(), "/home/ubuntu/bucket/test"))
                    video.download(downloadFolder,filename=fileName)
                    status = 'Video Uploaded Successfully!'
                    S3URL="URL_for_S3"+fileName.replace(' ','+')
                else:
                    status = 'Enter Valid YouTube Video URL!'
            
            else:
                status = 'Enter YouTube Video Url.'
           

            
            response=[{"url":S3URL}]
            status='success'
        except:
            pass
        return {'status':status,'response':response}

    def replace_video_hvp(self,moduleid,title,videoURL):
        '''
        Webserice call: {"moduleid":<moduleid>}
        Response: {'status':status,'response':response}
        '''
        response=[]
        status="error"
        self.engine.dispose()
        con=self.engine.connect()
        hvpMainMachineName='H5P.InteractiveVideo'
        main_library_id=read_sql(sql_text('SELECT * FROM mdl_hvp_libraries WHERE machine_name ="{}"'.format(hvpMainMachineName)),con)['id'].to_list()[0]
        sqlQm="SELECT mh.id AS instanceid FROM mdl_hvp mh INNER JOIN mdl_course_modules mcm ON mh.id=mcm.instance WHERE mcm.id={}".format(moduleid)
        instanceid=read_sql(sql_text(sqlQm),con)['instanceid'].to_list()[0]
        #sqlQ="SELECT * FROM mdl_hvp mh WHERE mh.id={}".format(instanceid)
        #modInfoDict=read_sql(sql_text(sqlQ),con).to_dict(orient='records')[0]
        #filtered=json.loads(modInfoDict['filtered'])
        #json_content=json.loads(modInfoDict['json_content'])

        filtered={"interactiveVideo":{"video":{"files":[{"path":videoURL}]}}} #
        json_content={"interactiveVideo":{"video":{"files":[{"path":videoURL}]}}} #
        
        filteredstr=json.dumps(filtered)  #json.dumps(filtered)  #.replace("'","''").replace("/","\/")
        json_content_str=json.dumps(json_content)
        textFieldsInfoDict={'filtered':filteredstr, 'json_content':json_content_str, "name":title, "slug":title}

        tablename='mdl_hvp'
        filterDict={'id':instanceid}
        updateStrDict=textFieldsInfoDict
        updateNumericDict={"main_library_id":main_library_id}
        updateTimeStrDict={}
        response=self.update_table_record(tablename, filterDict, updateStrDict,updateNumericDict,updateTimeStrDict)
        #print(response)
        response=self.call(self.mWAP,'core_course_edit_module',action='show',id=moduleid)
        #print(response)
        status='success'


        #print(response)
        con.close()
        return {'status':status,'response':response}     

##########################################################
#Unused
##########################################################
    



    # def get_schedule_events_course(self,courseid,schedulerid):
    #     '''
    #     Webserice call: {"courseid":courseid,"schedulerid":schedulerid}
    #     Response: {'status':status,'response':response}
    #     '''
    #     response=[]
    #     status='error'
    #     try:
    #         self.engine.dispose()
    #         con=self.engine.connect()
    #         sqlQ="SELECT s.id, s.name, c.shortname AS course, ut.email AS teacher, us.email AS student, ss.starttime, ss.duration, ss.appointmentlocation, sa.studentnote FROM mdl_scheduler s INNER JOIN  mdl_scheduler_slots ss ON s.id = ss.schedulerid INNER JOIN mdl_scheduler_appointment sa ON ss.id=sa.slotid INNER JOIN mdl_course c ON c.id=s.course INNER JOIN mdl_user ut ON ut.id=ss.teacherid INNER JOIN mdl_user us ON us.id=sa.studentid WHERE ss.schedulerid = {} AND s.course ={}".format(schedulerid,courseid)
    #         response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
    #         status='success'
    #     except:
    #         pass
    #     con.close()            
    #     return {'status':status,'response':response}

    # def get_schedule_events_teacher(self,userid):
    #     response=[]
    #     status='error'
    #     try:
    #         self.engine.dispose()
    #         con=self.engine.connect()
    #         sqlQ="SELECT s.id, s.name, c.shortname AS course, ut.email AS teacher, us.email AS student, ss.starttime, ss.duration, ss.appointmentlocation, sa.studentnote FROM mdl_scheduler s INNER JOIN  mdl_scheduler_slots ss ON s.id = ss.schedulerid INNER JOIN mdl_scheduler_appointment sa ON ss.id=sa.slotid INNER JOIN mdl_course c ON c.id=s.course INNER JOIN mdl_user ut ON ut.id=ss.teacherid INNER JOIN mdl_user us ON us.id=sa.studentid WHERE ss.teacherid = {}".format(userid)
    #         response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
    #         status='success'
    #     except:
    #         pass
    #     con.close()            
    #     return {'status':status,'response':response}

    # def get_schedule_events_student(self,userid):
    #     response=[]
    #     status='error'
    #     try:
    #         self.engine.dispose()
    #         con=self.engine.connect()
    #         sqlQ="SELECT s.id, s.name, c.shortname AS course, ut.email AS teacher, us.email AS student, ss.starttime, ss.duration, ss.appointmentlocation, sa.studentnote FROM mdl_scheduler s INNER JOIN  mdl_scheduler_slots ss ON s.id = ss.schedulerid INNER JOIN mdl_scheduler_appointment sa ON ss.id=sa.slotid INNER JOIN mdl_course c ON c.id=s.course INNER JOIN mdl_user ut ON ut.id=ss.teacherid INNER JOIN mdl_user us ON us.id=sa.studentid WHERE sa.studentid = {}".format(userid)
    #         response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
    #         status='success'
    #     except:
    #         pass
    #     con.close()            
    #     return {'status':status,'response':response}

    # def get_schedule_events_user(self,userid):
    #     response=[]
    #     status='error'
    #     try:
    #         self.engine.dispose()
    #         con=self.engine.connect()
    #         sqlQ="SELECT s.id, s.name, c.shortname AS course, ut.email AS teacher, us.email AS student, ss.starttime, ss.duration, ss.appointmentlocation, sa.studentnote FROM mdl_scheduler s INNER JOIN  mdl_scheduler_slots ss ON s.id = ss.schedulerid INNER JOIN mdl_scheduler_appointment sa ON ss.id=sa.slotid INNER JOIN mdl_course c ON c.id=s.course INNER JOIN mdl_user ut ON ut.id=ss.teacherid INNER JOIN mdl_user us ON us.id=sa.studentid WHERE sa.studentid = {} OR ss.teacherid = {}".format(userid,userid)
    #         response=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
    #         status='success'
    #     except:
    #         pass
    #     con.close()            
    #     return {'status':status,'response':response}

    # def get_schedule_list(self):
    #     '''
    #     Webserice call: {}
    #     Response: {'status':status,'response':response}
    #     '''
    #     response=[]
    #     status="error"
    #     try:
    #         self.engine.dispose()
    #         con=self.engine.connect()
    #         sqlQ="SELECT s.id, s.name FROM mdl_scheduler s"
    #         schedInfo=read_sql(sql_text(sqlQ),con).to_dict(orient='records')
    #         if len(schedInfo)!=0:
    #             response=[{'scheduleid':zz['id'], 'name':zz['name']} for zz in schedInfo]             
    #             status='success'
    #         else:
    #             status='No schedules yet'    
    #     except:
    #         pass
    #     con.close()
    #     return {'status':status,'response':response}