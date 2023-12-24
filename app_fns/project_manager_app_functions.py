import base64
import io
import pytz
import time
from datetime import datetime

import numpy as np
import networkx as nx

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# from jupyter_dash import JupyterDash

from pandas import to_datetime
# import plotly.figure_factory as ff

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import requests


###############################################
class the_app_functions:
    def __init__(self):
        self.response = []

############################################

# lrm_admin_app_funtions

###############################
# Category Actions
#############################
    def get_category_list(self, n_clicks, **kwargs):
        apimethod = 'get_category_list'
        apidata = {}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        dropdownlist = response['response']
        return (dropdownlist,)

    def view_course_category(self, *args, **kwargs):
        apimethod = 'view_course_category'
        apidata = {"categoryid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        cat2View = response['response']
        return (cat2View,)

    def edit_course_categories(self, *args, **kwargs):
        apimethod = 'edit_course_categories'
        apidata = {"siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        cat2Edit = response['response']
        return (cat2Edit,)

    def manage_category_cohorts(self, *args, **kwargs):
        apimethod = 'manage_category_cohorts'
        apidata = {"categoryid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        catCohorts = response['response']
        return (catCohorts,)

    def delete_course_category(self, *args, **kwargs):
        apimethod = 'delete_course_categories'
        apidata = {"categoryids": [args[1]]}
        # self.call_lrm_web_API(kwargs['webserviceurl'],apimethod,apidata).json()
        response = 'Disabled for now'
        return (json.dumps(response),)

    def manage_category_courses(self, *args, **kwargs):
        apimethod = 'manage_category_courses'
        apidata = {"categoryid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        catActns = response['response']
        return (catActns,)


# Course Actions


    def view_my_courses_moodle(self, *args, **kwargs):
        apimethod = "view_my_courses_moodle"
        apidata = {}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata)
        myCourses = response['response']
        return (myCourses,)

    def get_user_courses(self, *args, **kwargs):
        apimethod = "get_user_courses"
        apidata = {"userid": args[1], "hidden": 0}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata)
        # print(response.json())
        dropdownlist = []
        dropdownlist = response.json()['response']
        return (dropdownlist, dropdownlist)

    def get_category_course_list(self, *args, **kwargs):
        apimethod = "get_category_course_list"
        apidata = {"categoryid": args[1], "visible": 1}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata)
        # print(response.json())
        dropdownlist = []
        dropdownlist = response.json()['response']
        return (dropdownlist, dropdownlist)

    def view_course(self, *args, **kwargs):
        apimethod = 'view_course'
        apidata = {"courseid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        course2View = response['response']
        return (course2View,)

    def edit_course(self, *args, **kwargs):
        apimethod = 'edit_course'
        apidata = {"courseid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        course2Edit = response['response']
        return (course2Edit,)

    def enrol_users_in_course(self, *args, **kwargs):
        apimethod = 'enrol_users_in_course'
        apidata = {"courseid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        courseEnrol = response['response']
        return (courseEnrol,)

    def create_course_4m_moodle_template(self, *args, **kwargs):
        '''
        Webserice call: {"courseinfodict":{"templatename":<template shortname>,"categoryid":<Category ID>,"shortname":<Course short name>,"fullname":<Course full name>},"startdate":<start time str>,"enddate":<end time str>,}
        Response: {'status':status,'response':response}
        '''
        apimethod = 'create_course_4m_moodle_template'
        courseinfodict = json.loads(args[2])
        print(courseinfodict)
        courseinfodict["categoryid"] = args[1]
        courseinfodict["templatename"] = 'template_classroom'
        # {"courseinfodict":{"templatename":<template shortname>,"categoryname":<Category short name>,"shortname":<Course short name>,"fullname":<Course full name>},"startdate":<start time str>,"enddate":<end time str>,}

        apidata = json.dumps(
            {"siteurl": kwargs['siteurl'], "courseinfodict": courseinfodict})
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        # courseid=response['response'][0]['id']
        print(response)
        # kwargs['siteurl']+'/course/view.php?id={}'.format(courseid)
        course2View = response['response']['courseurl']
        return (course2View,)

    def duplicate_course(self, *args, **kwargs):
        '''
        Webserice call: {"courseinfodict":{"courseid":<courseid>,"categoryid":<Category ID>,"shortname":<Course short name>,"fullname":<Course full name>},"siteurl":siteurl}
        Response: {'status':status,'response':response}
        '''
        apimethod = 'duplicate_course'
        courseinfodict = json.loads(args[2])
        courseinfodict['categoryid'] = args[1]

        apidata = courseinfodict
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        courseid = response['response']['id']
        print(response)
        course2View = kwargs['siteurl'] + \
            'course/view.php?id={}'.format(courseid)
        return (course2View,)

    def create_courses(self, *args, **kwargs):
        '''
        Webserice call: {"shortname":"JULY13tyu","fullname":"From Colab July 14tyu","startdate":"13/06/2023 0800","enddate":"13/07/2023 0800"}
        Response: {'status':status,'response':response}
        '''
        apimethod = 'create_courses'
        inputdict = json.loads(args[2])
        inputdict['categoryid'] = args[1]
        apidata = {"datadicts": [inputdict]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        courseid = response['response'][0]['id']
        print(response)
        course2View = kwargs['siteurl'] + \
            'course/view.php?id={}'.format(courseid)
        return (course2View,)

    def change_edit_mode(self, *args, **kwargs):
        apimethod = 'change_edit_mode'
        apidata = {"editmode": args[1], "userid": args[2],
                   "contextlevel": args[3], "instanceid": args[4], "editrole": args[5]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata)
        return (response,)

# Section Actions
    def get_course_sections_list(self, *args, **kwargs):
        apimethod = 'get_course_sections_list'
        apidata = {"courseid": args[1], "secnvisible": 1}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata)
        dropdownlist = response.json()['response']
        return (dropdownlist, dropdownlist)

    def edit_course_section(self, *args, **kwargs):
        apimethod = 'edit_course_section'
        apidata = {"sectionid": args[1], "siteurl": kwargs['siteurl']}
        print(apidata)
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        section2Edit = response['response']
        return (section2Edit,)

    def edit_course_section_visibility(self, *args, **kwargs):
        apimethod = 'edit_course_section_visibility'
        apidata = {'action': args[1], 'id': args[2]}
        print(apidata)
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        section2Edit = response['response']
        return (section2Edit,)

    def create_course_section(self, *args, **kwargs):
        apimethod = 'create_course_section'
        apidata = json.loads(args[1])
        apidata['courseid'] = args[2]
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        sectionid = response['response'][0]['sectionid']
        createSectionBtnURL = kwargs['siteurl'] + \
            "course/editsection.php?id={}&sr=0".format(sectionid)
        return (createSectionBtnURL,)

# Module actions
    def get_course_section_modules_list(self, *args, **kwargs):
        apimethod = 'get_course_section_modules_list'
        apidata = {
            "courseid": args[1], "sectionid": args[2], "modvisible": 1, "secnvisible": 1}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata)
        print(response.json())
        dropdownlist = response.json()['response']
        return (dropdownlist, dropdownlist)

    def view_module(self, *args, **kwargs):
        apimethod = 'view_module'
        apidata = {"moduleid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        mod2View = response['response']
        print(mod2View)
        return (mod2View,)

    def edit_module(self, *args, **kwargs):
        apimethod = 'edit_module'
        apidata = {"moduleid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        mod2Edit = response['response']
        return (mod2Edit,)

    def edit_module_role_assignments(self, *args, **kwargs):
        apimethod = 'edit_module_role_assignments'
        apidata = {"moduleid": args[1], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        mod2Enrol = response['response']
        return (mod2Enrol,)

    def add_activity_module_2_course_section(self, *args, **kwargs):
        apimethod = 'add_activity_module_2_course_section'
        apidata = {"modname": args[1], "courseid": args[2],
                   "sectionid": args[3], "siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        addedMod = response['response']
        return (addedMod,)

    def create_assignments(self, *args, **kwargs):
        '''
        for parameters refer to
        #infodict={"title":"WP2.2.1", "description":"Design of the structure of the backend","allowsubmissionsfromdate":"15-05-2020","duedate":"15-12-2020","cutoffdate":"15-12-2021","gradingduedate":"14/12/2023", "grade":40}
        '''
        infodict = json.loads(args[3])
        infodict['courseid'] = args[1]
        infodict['sectionid'] = args[2]
        apidata = {"datadicts": [infodict]}
        apimethod = 'create_assignments'
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        moduleid = response['response'][0]['moduleid']
        createSectionBtnURL = kwargs['siteurl'] + \
            "mod/{}/view.php?id={}".format("assign", moduleid)
        return (createSectionBtnURL,)

    def update_course_module(self, *args, **kwargs):
        '''
        for parameters refer to
        #update_course_module(courseid,sectionid,moduleid,title=None,visible=1,optionsDict=None)
        #update_hvp_module(courseid,sectionid,moduleid,title=None,visible=1,optionsDict=None,hvpmethod=None,hvpparameters=None)
        '''
        moduleid = args[3]
        apidata = json.loads(args[4])
        apidata['courseid'] = args[1]
        apidata['sectionid'] = args[2]
        apidata['moduleid'] = moduleid
        modulename = self.call_lrm_web_API(kwargs['webserviceurl'], "get_course_module_by_id", {
                                           "moduleid": moduleid}).json()['response'][0]['modname']
        if modulename != 'hvp':
            apimethod = 'update_course_module'
        else:
            apimethod = 'update_hvp_module'

        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        moduleid = response['response'][0]['moduleid']
        createSectionBtnURL = kwargs['siteurl'] + \
            "mod/{}/view.php?id={}".format(modulename, moduleid)
        return (createSectionBtnURL,)
# User management

    def get_user_capabilities(self, *args, **kwargs):
        apimethod = 'get_user_capabilities'
        apidata = {"userid": args[1],
                   "contextlevel": args[2], "instanceid": args[3]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        userRoles = response['response']
        return (userRoles,)

    def get_system_user_rolenames(self, *args, **kwargs):
        apimethod = 'get_system_user_rolenames'
        apidata = {"userid": args[1]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        userRoles = response['response']
        return (userRoles,)

    def get_context_user_rolenames(self, *args, **kwargs):
        apimethod = 'get_context_user_rolenames'
        apidata = {"userid": args[1],
                   "contextlevel": args[2], "instanceid": args[3]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        userRoles = response['response']
        return (userRoles,)

    def view_add_users(self, *args, **kwargs):
        apimethod = 'view_add_users'
        apidata = {"siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        userActns = response['response']
        return (userActns,)

    def view_add_cohorts(self, *args, **kwargs):
        apimethod = 'view_add_cohorts'
        apidata = {"siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        cohortActns = response['response']
        return (cohortActns,)

    def bulk_user_actions(self, *args, **kwargs):
        apimethod = 'bulk_user_actions'
        apidata = {"siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        userActns = response['response']
        return (userActns,)

    def upload_users(self, *args, **kwargs):
        apimethod = 'upload_users'
        apidata = {"siteurl": kwargs['siteurl']}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        userActns = response['response']
        return (userActns,)


########################
# Old stuff
#####################


    def get_all_users(self, *args, **kwargs):
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], 'get_all_users', {})
        userList = [usr['username'] for usr in response.json()['response']]
        userList.sort()

        return (userList, response.text)

    def enroll_course_user(self, *args, **kwargs):
        courseName = args[1]
        userName = args[3]
        roleID = args[4]
        usersDict = json.loads(args[2])['response']
        if len(usersDict) != 0:
            userId = [usr['id']
                      for usr in usersDict if usr['username'] == userName][0]
        print(userId, courseName)
        apidata = {"coursename": courseName,
                   "username": userName, "roleid": roleID}
        apimethod = 'manual_enroll_user_in_course'
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata)
        return (userName+' enrolled in program '+courseName+str(response),)

    def create_course_category(self, *args, **kwargs):
        apimethod = 'create_course_category'
        apidata = {"categoryname": args[1], "parentid": args[2]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        print(response)
        # createdCat=kwargs['siteurl']+'/course/index.php?categoryid={}'.format(response[0]['id'])
        editCat = kwargs['siteurl'] + \
            '/course/editcategory.php?id={}'.format(response[0]['id'])
        return (editCat,)

    def update_course_category_name(self, *args, **kwargs):
        # Obsolete - dont use
        apimethod = 'update_course_category_name'
        apidata = {"categoryid": args[2], "newcategoryname": args[1]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        editedSecn = kwargs['siteurl'] + \
            '/course/index.php?categoryid={}'.format(args[2])
        msg = 'The name of the Category {} was updated to {}'.format(
            editedSecn, args[1])
        return (msg,)

    def get_course_category_by_name(self, *args, **kwargs):
        apimethod = 'get_sql_request'
        apidata = {
            "sqlQ": "SELECT * FROM mdl_course_categories WHERE name="+"%5C%22"+args[1]+"%5C%22"}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        cat2View = ''
        id2View = None
        print(response, len(response['response']))
        if len(response['response']) != 0:
            id2View = response['response'][0]['id']
            cat2View = kwargs['siteurl'] + \
                '/course/index.php?categoryid={}'.format(id2View)
        print(cat2View)
        return (cat2View, id2View)
######################################
# User Interactions
####################################

    def get_user_module_lms_interaction_graph_fig(self, *args, **kwargs):
        print(args[1], args[2], args[3], args[4], args[5])
        apimethod = 'get_user_module_lms_interaction'
        apidata = {"userid": args[1], "courseid": args[2], "moduleid": args[3],
                   "edulevel": 2, "startDateStr": args[4], "endDateStr": args[5]}
        output = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        # ={'status':modinteractionOutput['status'],'response':modinteractionOutput['response']}
        print(output)
        # print(output)
        modInteractions = output['response']
        fig = go.Figure()
        fig_mod = go.Figure()
        try:
            activityList0 = list(set([bb[1] for bb in [aa.split(
                '/') for aa in self.get_keys(modInteractions)] if len(bb) > 1]))
            if 'core' in activityList0:
                activityList0.remove('core')
            activityList0.sort()
            activityList = [z for z in activityList0 if 'mod_' not in z]
            modList = [z for z in activityList0 if 'mod_' in z]
            x = []
            for activity in activityList:
                xtemp = 0
                for dy in [*modInteractions]:
                    if activity in [*modInteractions[dy]]:
                        xtemp += modInteractions[dy][activity]
                    else:
                        xtemp += 0
                x += [xtemp]

            fig.add_trace(go.Bar(y=[' '.join(zz.split('_'))
                          for zz in activityList], x=x, name='Test', orientation='h'))
            for activity in modList:
                xm = []
                for dy in [*modInteractions]:
                    if activity in [*modInteractions[dy]]:
                        xm += [modInteractions[dy][activity]]
                    else:
                        xm += 0
                fig_mod.add_trace(
                    go.Bar(x=[*modInteractions], y=xm, name=' '.join(activity.split('_'))))

            fig.update_layout(
                barmode='stack', title='Interaction statistics', xaxis_title='Number of activities')
            fig_mod.update_layout(
                barmode='stack', title='Number of hours spent', yaxis_title='Number of hours spent')
        except:
            pass
        # fig_mod.add_trace(go.Bar(x=['A','B'],y=[2,3],name='something'))
        print('here')
        return (fig, fig_mod)

    def get_course_users_list(self, *args, **kwargs):
        apimethod = 'get_course_users_list'
        apidata = {"courseid": args[1]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        dropdownlist = response['response']
        return (dropdownlist,)

    def get_user_context_events(self, *args, **kwargs):
        print(args[1], args[2], args[3])
        apimethod = 'get_user_context_events'
        contextlevel = 70
        apidata = {"userid": args[1], "contextlevel": contextlevel,
                   "edulevel": 2, "startDateStr": args[2], "endDateStr": args[3]}
        output = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        # print(output) #={'status':modinteractionOutput['status'],'response':modinteractionOutput['response']}

        if len(output) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            div = self.dict_2_table_div(output)
        return (div, json.dumps(output))

    def get_user_context_events_fig(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        print(args[1], args[2], args[3])
        apimethod = 'get_user_context_connectivity'
        contextlevel = 70
        apidata = {"userid": args[1], "contextlevel": contextlevel,
                   "edulevel": 2, "startDateStr": args[2], "endDateStr": args[3]}
        output = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        # output=mgLRM.get_user_context_connectivity(**apidata)['response']
        print(output)
        nodeInfo = []
        edgeInfo = []
        fig = go.Figure()
        print(len(output))
        if len(output) != 0:
            G = nx.MultiDiGraph()
            nodeInfo = [tuple(nI) for nI in output['nodeInfo']]
            G.add_nodes_from(nodeInfo)
            if len(output['edgeInfo']) != 0:
                edgeInfo = [tuple(nI) for nI in output['edgeInfo']]
                # pd.DataFrame(output)['contextid'].to_list()
                states = [nn[0] for nn in output['nodeInfo']]
                G.add_edges_from(edgeInfo)
            fig = self.plot_network_graph(G, 'usrdt', 'Module Transition')

        return (fig,)

    def plot_network_graph(self, G, nodesizekey, graphTitle):
        fig = go.Figure()
        node_x = []
        node_y = []
        edge_x = []
        edge_y = []
        node_text = []
        edge_text = []
        node_size = []
        edge_size = []
        node_color = []
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            nodeName = G.nodes[node]['data']['modulename']
            courseName = G.nodes[node]['data']['coursename']
            nodeTime = G.nodes[node]['data']['totaldedication']/60.
            nodeScore = G.nodes[node]['data']['score']
            print(nodeName)
            node_x.append(x)
            node_y.append(y)
            nodesize = 0
            for edge in list(set([edg for edg in G.out_edges(node)])):
                for ky in range(G.number_of_edges(edge[0], edge[1])):
                    nodesize += G.get_edge_data(edge[0],
                                                edge[1], key=ky)[nodesizekey]
                x0, y0 = G.nodes[edge[0]]['pos']
                x1, y1 = G.nodes[edge[1]]['pos']
                edge_x.append(x0)
                edge_x.append(x1)
                # edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                # edge_y.append(None)
                edge_text.append(str(edge))
                if edge[0] != edge[1]:
                    edgesize = G.number_of_edges(
                        edge[0], edge[1])+G.number_of_edges(edge[1], edge[0])
                else:
                    edgesize = G.number_of_edges(edge[0], edge[1])
                fig.add_trace(go.Scatter(
                    x=edge_x, y=edge_y,
                    mode="lines+markers",
                    text='',
                    hoverinfo='text',
                    # marker=dict(symbol="arrow",color="royalblue",size=10,angleref="previous",standoff=20),
                    # dict(width=round(0.5+edgesize/4),color='#888'),
                    line=dict(width=1.5, color='#888'),
                    # hovertemplate="""Number of edges:{} - {}<br><extra></extra>""".format(str(edge),edgesize)
                ))

            node_size.append(24)  # node_size.append(nodesize)
            # node_size.append(nodesize)
            node_color.append(
                len(list(set([edg for edg in G.in_edges(node)]))))
            ine = list(set([edg[0] for edg in G.in_edges(node)]))
            ine.sort()
            oute = list(set([edg[1] for edg in G.out_edges(node)]))
            oute.sort()
            innodes = ', '.join([str(nn) for nn in ine])
            outnodes = ', '.join([str(nn) for nn in oute])

            nodetxt = """Node ID: {}<br>Name: {}<br>Course: {}<br>Time spent / mins: {} <br>Score: {} <br>From nodes: {} <br>To nodes: {}""".format(
                str(node), nodeName, courseName, round(nodeTime+0.5), round(nodeScore, 1), innodes, outnodes)
            node_text.append(nodetxt)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,  # True,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Rainbow',  # 'YlGnBu',
                reversescale=True,
                color=[],  # 'royalblue',
                colorbar=dict(
                    thickness=15,
                    title='Number of re-visits',
                    xanchor='left',
                    titleside='right'),
                line_width=2),
            hovertemplate="""%{text}<br><extra></extra>"""
        )

        # normalized_node_size=[44*round((xx-min(node_size))/(max(node_size)-min(node_size))) for xx in node_size]
        node_trace.marker.size = node_size
        node_trace.marker.color = node_color
        node_trace.text = node_text
        # edge_trace.line.width=5 #edge_size
        # edge_trace.marker.text=edge_text
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
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[dict(
                text="Test text",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002)],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

        return fig

    def get_course_user_dedication(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        rolename = "student"
        apimethod = 'get_course_user_dedication'
        contextlevel = 70
        apidata = {"courseid": args[1], "rolename": rolename}
        courseUserInteractions = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        df = pd.DataFrame(courseUserInteractions)
        df.loc[:, 'dedication'] = [round(zz/60.)
                                   for zz in df['dedication'].to_list()]
        ycol = 'dedication'
        xcol = 'firstname'  # 'userid' #'modtype' #'userid'
        colorcol = 'modulename'  # 'instanceid'
        fig = px.bar(df, y=ycol, x=xcol, color=colorcol,
                     barmode='stack', height=400, hover_data=['score'])
        if len(courseUserInteractions) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            div = self.dict_2_table_div(courseUserInteractions)
        return (fig, div)

    def get_module_user_dedication(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        rolename = "student"
        apimethod = 'get_module_user_dedication'
        contextlevel = 70
        apidata = {"courseid": args[1],
                   "moduleid": args[2], "rolename": rolename}
        moduleUserInteractions = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        df = pd.DataFrame(moduleUserInteractions)
        df.loc[:, 'dedication'] = [round(zz/60.)
                                   for zz in df['dedication'].to_list()]
        ycol = 'dedication'
        xcol = 'firstname'  # 'userid' #'modtype' #'userid'
        colorcol = 'day'  # 'instanceid'
        fig = px.bar(df, y=ycol, x=xcol, color=colorcol, barmode='stack',
                     height=400, hover_data=['score'])  # , histfunc='avg')
        if len(moduleUserInteractions) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            div = self.dict_2_table_div(moduleUserInteractions)
        return (fig, div)

    def get_course_user_clusters(self, *args, **kwargs):
        print(args[1], args[2], args[3])
        apimethod = 'get_course_user_clusters'
        contextlevel = 70
        apidata = {"courseid": args[1],
                   "startDateStr": args[2], "endDateStr": args[3]}
        output = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()['response']
        # ={'status':modinteractionOutput['status'],'response':modinteractionOutput['response']}
        print(output)
        if len(output) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            div = self.dict_2_table_div(output)
        return (div, json.dumps(output))

    def get_course_user_clusters_fig(self, *args, **kwargs):
        print(args[1])
        df = pd.DataFrame(json.loads(args[1]))
        df.loc[:, 'labels'] = ['G-'+str(zz) for zz in df['labels'].to_list()]
        df.loc[:, 'totaldedication'] = [
            round(zz) for zz in df['totaldedication'].to_list()]
        renameMap = {'number_of_nodes': 'Number of activities', 'totaldedication': 'Time spent / mins',
                     'labels': 'Cluster', 'total_re_visits': 'Number of re-visits', 'number_of_selfloops': 'Number of continuations'}
        df.rename(columns=renameMap, inplace=True)
        # ['density','global_reaching_centrality','Cluser','Number of activities','Number of continuations','Number of re-visits','Time spent','userid']
        hovercol = 'Number of activities'
        xcol = 'Time spent / mins'
        colorcol = 'Cluster'
        ycol = 'Number of re-visits'
        sizecol = 'Number of continuations'
        fig = px.scatter(df, x=xcol, y=ycol, color=colorcol,
                         size=sizecol, hover_data=['user'])
        return (fig,)

    def get_course_user_clusters_fig3d(self, *args, **kwargs):
        df = pd.DataFrame(json.loads(args[1]))
        df.loc[:, 'labels'] = ['G-'+str(zz) for zz in df['labels'].to_list()]
        df.loc[:, 'totaldedication'] = [
            round(zz) for zz in df['totaldedication'].to_list()]
        renameMap = {'number_of_nodes': 'Number of activities', 'totaldedication': 'Time spent / mins',
                     'labels': 'Cluster', 'total_re_visits': 'Number of re-visits', 'number_of_selfloops': 'Number of continuations'}
        df.rename(columns=renameMap, inplace=True)
        # ['density','global_reaching_centrality','Cluser','Number of activities','Number of continuations','Number of re-visits','Time spent','userid']
        hovercol = 'Number of activities'
        xcol = 'Time spent / mins'
        colorcol = 'Cluster'
        ycol = 'Number of re-visits'
        zcol = 'Number of activities'
        sizecol = 'Number of continuations'
        fig = px.scatter_3d(df, x=xcol, y=ycol, z=zcol, color=colorcol,
                            size=sizecol, hover_data=['user', 'score'])
        return (fig,)

################################################
# Add hvp interactions
################################################

    def add_hvp_interactions(self, *args, **kwargs):
        apimethod = 'add_hvp_interactions'
        apidata = {"moduleid": args[1], 'videoURL': args[2]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        dropdownlist = response['response']
        return (dropdownlist,)


################################################
# Session scheduling
################################################


    def get_schedule_list(self, *args, **kwargs):
        apimethod = 'get_schedule_list'
        apidata = {}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        scheduleList = response['response']
        return (scheduleList,)

    def get_schedule_events_user(self, *args, **kwargs):
        apimethod = 'get_schedule_events_user'
        apidata = {"userid": args[1]}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        eventsList = response['response']
        return (eventsList,)


#######################
# General Functions
#######################


    def drop_down_menu_options(self, *args, **kwargs):
        temp = kwargs
        for arg in args:
            temp = temp[arg]
        return ([{'label': i, 'value': i} for i in temp],)

    def return_args(self, *args, **kwargs):
        response = args[1]
        return (response,)

    def csv_upload_df_return(self, contents):
        if contents is None:
            raise PreventUpdate
            df = pd.DataFrame()

        else:  # read CSV data
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            except Exception as e:
                df = pd.DataFrame()

        updateDataPDF = df
        updateDataPDF = updateDataPDF.fillna('')
        return updateDataPDF

    def csv_upload_div_return_and_store(self, contents):
        updateDataPDF = self.csv_upload_df_return(contents)
        if len(updateDataPDF) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            dataDict = updateDataPDF.to_dict(orient='records')
            # print(dataDict)
            div = self.dict_2_table_div(dataDict)
        return div, json.dumps(dataDict)

    def dict_2_table_div(self, contents):
        # div=dash_table.DataTable(
        #         data=contents,
        #         columns=[{'id': c, 'name': c} for c in [*contents[0]]],
        #         style_cell={'textAlign': 'left','height':'auto','whiteSpace': 'normal'},
        #         style_header={
        #         'backgroundColor': '#8febb5',
        #         'fontWeight': 'bold'
        #         },
        #         #page_size=2,
        #         style_table={'height': '300px', 'overflowY': 'auto'},#enable scroll
        #         # style_table={'height': '300px'},#enable scroll
        #         # style_table={
        #         #     'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
        #         #     'minWidth': '900px', 'width': '900px', 'maxWidth': '900px'
        #         # },
        #         # fixed_rows={'headers': True}
        div = dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in [*contents[0]]
            ],
            data=contents,
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=100,
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender"),
            style_table={'overflowX': 'scroll', 'overflowY': 'auto', 'height': '300px'})
        return div

    def get_from_store_return_str(self, contents):
        updateDataPDF = pd.read_json(contents)
        dataDict = updateDataPDF.to_dict(orient='records')
        return (json.dumps(dataDict),)

    def get_json_from_store_table_return(self, contents):
        updateDataPDF = pd.read_json(contents)
        if len(updateDataPDF) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            dataDict = updateDataPDF.to_dict('records')
            div = self.pdf_2_table_div(dataDict)
        return div

    def get_json_from_store_dict_div_return(self, contents):
        updateDataPDF = pd.read_json(contents)
        if len(updateDataPDF) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            dataDict = updateDataPDF.to_dict('records')
            div = html.Div([
                html.P(json.dumps(dataDict)),
            ])
        return (div,)

    def get_from_store_fig_return(self, contents):
        updateDataPDF = pd.read_json(contents)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=updateDataPDF['AA'].to_list(
        ), y=updateDataPDF['BB'].to_list(), visible=True, name='Sales'))
        fig.update_layout(title='test', width=850, height=400)

        return (fig,)

    def fillDropdown(self, data, **kwargs):
        updateDataPDF = pd.read_json(data)
        dropdownlist = list(set(updateDataPDF[kwargs['colname']].to_list()))
        dropdownlist.sort()
        return (dropdownlist,)

    def fn_btn1(self, *args, **kwargs):
        div = ("btn test",)
        return div

    def call_lrm_web_API_get(self, siteurl, apimethod, apidata):
        apidata = str(apidata).replace('"', '%22').replace(
            "'", '%22').replace('%22\%22', '\%22').replace("\%22%22", '\%22')
        url1 = "{}/api/input?method={}&data={}".format(
            siteurl, apimethod, apidata)
        print(url1)
        response = requests.get(url1, verify=False)
        return response

    def call_lrm_web_API(self, siteurl, apimethod, apidata):
        url = "{}/api/postcall".format(siteurl)
        postdata = {"method": apimethod, "data": apidata}
        response = requests.post(url, json=postdata, verify=False)
        return response

    def call_web_service_return_str(self, n_cliks, method, data, **kwargs):
        response = self.call_lrm_web_API(kwargs['webserviceurl'], method, data)
        # print(url1)
        # response = requests.get(url1)
        # response=response.json() #JSON return
        return (response.text,)

    def get_method_return_dropdown(self, n_cliks, **kwargs):
        apimethod = 'get_methods_list'
        apidata = {}
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], apimethod, apidata).json()
        dropdownlist = response['response']
        return (dropdownlist, json.dumps(dropdownlist))

    def call_web_service_return_table(self, n_cliks, method, data, **kwargs):
        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], method, json.loads(data)).json()
        print(response)
        if len(response['response']) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            div = self.dict_2_table_div(response['response'])
        return (div, json.dumps(response['response']))

    def call_web_service_return_tableV2(self, n_cliks, *args, **kwargs):
        data = args[3]
        options = json.loads(args[1])
        for option in options:
            if option['value'] == args[2]:
                method = option['label']

        response = self.call_lrm_web_API(
            kwargs['webserviceurl'], method, json.loads(data)).json()
        print(response)
        if len(response['response']) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            div = self.dict_2_table_div(response['response'])
        return (div,)

    def get_4m_store_and_callweb_API(self, n_clicks, apimethod, contents, **kwargs):
        contentsPDF = pd.read_json(contents)
        apidata = {"datadicts": contentsPDF.to_dict(orient='records')}
        url = "{}/api/postcall".format(kwargs['webserviceurl'])
        postdata = {"method": apimethod, "data": apidata}
        response = requests.post(url, json=postdata, verify=False).json()

        if len(response['response']) == 0:
            raise PreventUpdate
            div = html.Div()
        else:
            div = self.dict_2_table_div(response['response'])
        return (div, json.dumps(response['response']))
##################################
# Calendar App functions
#################################

    def google_authenticatefn(self, n_clicks):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        global creds
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            msg = "token valid"
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                msg = "token expired"
                creds.refresh(Request())
            else:
                msg = "authenticating"
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()

                # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('credentials.json',SCOPES)
                # flow.redirect_uri = 'http://localhost:5000/'
                # authorization_url, state = flow.authorization_url(
                #     # Enable offline access so that you can refresh an access token without
                #     # re-prompting the user for permission. Recommended for web server apps.
                #     access_type='offline',
                #     # Enable incremental authorization. Recommended as a best practice.
                #     include_granted_scopes='true')

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return (msg,)

    def read_cal_events(self, n_clicks, calid, **kwargs):
        global service
        # creds=kwargs["creds"]
        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId=calid, timeMin=now,
                                                  maxResults=kwargs['maxResults'], singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                # return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get(
                    'dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)

        return (str(event),)

    def calurl_return(self, n_clicks, calid):
        calurl = 'https://calendar.google.com/calendar/u/1/embed?src={}&ctz=Asia/Colombo&csspa=1'.format(
            calid)
        return (calurl, calid)

    def get_store_dict_create_GC_events_dict(self, n_clicks, calendarid, contents):
        # global service
        service = build('calendar', 'v3', credentials=creds)
        updateDataPDF = pd.read_json(contents)
        eventdicts = updateDataPDF.to_dict(orient='records')

        eventGCdicts = []
        for evnt in eventdicts:
            print('evnt', evnt)
            eventGCdicts += mc.create_event(service, calendarid, evnt)
        return (str(eventGCdicts),)

##########################################################
# Competency
##########################################################
    def get_assignments_grades_with_competency_original(self, webserviceurl):
        apimethod = 'get_all_modules_local_student_grades_competency'
        parameters = {}
        response = self.call_lrm_web_API(
            webserviceurl, apimethod, parameters).json()['response']
        return response

    def get_assignments_grades_with_competency(self, webserviceurl):
        apimethod = 'get_all_modules_local_student_grades_competency'
        parameters = {}
        responsePDF = pd.DataFrame(self.call_lrm_web_API(
            webserviceurl, apimethod, parameters).json()['response'])
        responsePDF['attainment'] = responsePDF['finalgrade'] / \
            responsePDF['grademax']
        responsePDF['minattainment'] = responsePDF['gradepass'] / \
            responsePDF['grademax']

        gradesList = responsePDF['finalgrade'].fillna(0).to_list()
        maxGradesList = responsePDF['grademax'].fillna(0).to_list()
        passGradesList = responsePDF['gradepass'].fillna(0).to_list()
        newColNames = {'competencyframework': 'project', 'coursename': 'WP', 'firstname': 'partner', 'sectionname': 'group', 'competencyname': 'deliverable', 'activityname': 'taskname', 'grademax': 'assigned_units', 'finalgrade': 'utilized_units',
                       'gradedeficit': 'unutilized_units', 'gradepass': 'feasible_units', 'attainment': 'completion_rate', 'minattainment': 'feasible_completion_rate'}  # , 're_allocated':'re_allocated'} #'gradedeficit':'unutilizedunits',
        outputPDF = responsePDF[[*newColNames]].copy(deep=True)
        outputPDF.rename(columns=newColNames, inplace=True)
        outputPDF['to_be_utilized_units'] = outputPDF['feasible_units'] - \
            outputPDF['utilized_units']
        outputPDF['cannot_be_claimed_units'] = outputPDF['assigned_units'] - \
            outputPDF['feasible_units']

        # userIDs=responsePDF['userid'].to_list()
        # userids=list(set(userIDs))
        # scalename='TEAL2.O'
        # sqlQ="SELECT * FROM mdl_scale WHERE name='{}' AND userid IN {}".format(scalename,tuple(userids+[0]))
        # scaleslist=pd.DataFrame(self.call_lrm_web_API(webserviceurl,"get_sql_request",{'sqlQ':sqlQ}).json()['response'])['scale'].to_list()
        # ratescales={userids[iz]:json.loads(zz)['researcher'] for iz,zz in enumerate(scaleslist)}

        # outputPDF['allocated_cost']=[gr*ratescales[userIDs[ig]] for ig,gr in enumerate(maxGradesList)]
        # outputPDF['feasible_max_cost']=[gr*ratescales[userIDs[ig]] for ig,gr in enumerate(passGradesList)]
        # outputPDF['utilized_cost']=[gr*ratescales[userIDs[ig]] for ig,gr in enumerate(gradesList)]
        # outputPDF['to_be_utilized_cost']=outputPDF['feasible_max_cost']-outputPDF['utilized_cost']
        # outputPDF['cannot_be_claimed_cost']=outputPDF['allocated_cost']-outputPDF['feasible_max_cost']

        response = outputPDF.to_dict(orient='records')
        return response

    def get_assignments_by_competencies(self, webserviceurl, scalename, competencyids):
        modname = 'assign'
        rolename = 'student'
        parameters = {"modname": modname, "rolename": rolename,
                      "competencyids": competencyids}
        apimethod = "get_modules_users_information_by_competencies"
        colnames = ['userid', 'firstname', 'coursename', 'name', 'intro', 'competencyidnumber', 'competency', 'competencydescription', 'grade', 'finalgrade',
                    'attainment', 'allowsubmissionsfromdate', 'duedate', 'cutoffdate', 'gradingduedate', 'course', 'sectionid', 'moduleid', 'competencyframeworkid', 'competencyid']
        responsePDF = pd.DataFrame(self.call_lrm_web_API(
            webserviceurl, apimethod, parameters).json()['response'])[colnames]
        gradesList = responsePDF['finalgrade'].fillna(0).to_list()
        maxGradesList = responsePDF['grade'].fillna(0).to_list()
        userIDs = responsePDF['userid'].to_list()
        userids = list(set(userIDs))
        sqlQ = "SELECT * FROM mdl_scale WHERE name='{}' AND userid IN {}".format(
            scalename, tuple(userids+[0]))
        scaleslist = pd.DataFrame(self.call_lrm_web_API(webserviceurl, "get_sql_request", {
                                  'sqlQ': sqlQ}).json()['response'])['scale'].to_list()
        ratescales = {userids[iz]: json.loads(
            zz)['researcher'] for iz, zz in enumerate(scaleslist)}
        for lbl in ['allowsubmissionsfromdate', 'duedate', 'cutoffdate', 'gradingduedate']:
            temp = pd.to_datetime(
                responsePDF[lbl].to_list(), unit='s', origin='unix').to_list()
            responsePDF[lbl] = [zz.strftime(
                "%d/%m/%Y, %H:%M:%S") for zz in temp]

        newColNames = {'moduleid': 'taskid', 'name': 'taskname', 'intro': 'description', 'coursename': 'WP', 'grade': 'assignedunits', 'finalgrade': 'completedunits', 'allowsubmissionsfromdate': 'startdate', 'cutoffdate': 'extendedduedate',
                       'gradingduedate': 'evaluateby', 'course': 'WPid', 'competencyframeworkid': 'evaluationframework', 'competencyid': 'deliverableid', 'competency': 'deliverable', 'competencydescription': 'deliverabledescription', 'competencyidnumber': 'deliverablelabel'}
        responsePDF.rename(columns=newColNames, inplace=True)
        responsePDF['completedunits'] = gradesList
        responsePDF['actualcost'] = [gr*ratescales[userIDs[ig]]
                                     for ig, gr in enumerate(gradesList)]
        responsePDF['allocatedcost'] = [gr*ratescales[userIDs[ig]]
                                        for ig, gr in enumerate(maxGradesList)]
        responsePDF['tobeclaimedcost'] = responsePDF["allocatedcost"] - \
            responsePDF["actualcost"]
        colomnorder = ['userid', 'firstname', 'WP', 'taskname', 'description', 'deliverablelabel', 'deliverable', 'deliverabledescription', 'attainment', 'assignedunits', 'allocatedcost',
                       'completedunits', 'actualcost', 'tobeclaimedcost', 'startdate', 'duedate', 'extendedduedate', 'WPid', 'sectionid', 'taskid', 'evaluationframework', 'deliverableid']
        response = responsePDF[colomnorder].to_dict(orient='records')
        return response

    def get_gantt_chart_by_projects_users(self, projectids, roleid, userids, startTime, endTime):
        response, responsePrint = self.get_project_tasks_by_users(
            projectids, roleid, userids, startTime, endTime)
        df = pd.DataFrame([{'Task': dct['name'], 'Start': datetime.fromtimestamp(dct['starttime']).strftime(
            "%Y-%m-%d"), 'Finish': datetime.fromtimestamp(dct['endtime']).strftime("%Y-%m-%d"), 'Resource': dct['projectid']} for dct in responsePrint])
        return ff.create_gantt(df)

    def get_attainment_info_fig_menus(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        output = self.get_assignments_grades_with_competency(
            kwargs['webserviceurl'])
        assignmentsPDF = pd.DataFrame(output)
        options = [{'label': ky, 'value': ky} for ky in [*assignmentsPDF]]
        return (options, options, options, options)

    def get_attainment_levels_fig_menus(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        output = self.get_assignments_grades_with_competency(
            kwargs['webserviceurl'])
        assignmentsPDF = pd.DataFrame(output)
        options = [{'label': ky, 'value': ky} for ky in [*assignmentsPDF]]
        return (options, options, options)

    def get_attainment_info_fig(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        output = json.loads(args[1])
        assignmentsPDF = pd.DataFrame(output)
        xcol = args[2]
        ycol = args[3]
        groupcol = args[4]
        textcol = args[5]
        fig = px.bar(assignmentsPDF, x=xcol, y=ycol, color=groupcol,
                     text=textcol, title="{} vs {}".format(ycol, xcol))
        return (fig,)

    def get_attainment_levels_fig(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        output = json.loads(args[1])
        assignmentsPDF = pd.DataFrame(output)
        xcol = args[2]
        ycol = args[3]
        groupcol = args[4]
        fig = px.histogram(assignmentsPDF, x=xcol, y=ycol, color=groupcol, barmode='group',
                           histfunc='avg', title="Average of {} vs {}".format(ycol, xcol))
        return (fig,)

    def get_col_names(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        output = self.get_assignments_grades_with_competency(
            kwargs['webserviceurl'])
        assignmentsPDF = pd.DataFrame(output)
        options = [{'label': ky, 'value': ky} for ky in [*assignmentsPDF]]
        return (options,)

    def get_given_col_labels(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        output = self.get_assignments_grades_with_competency(
            kwargs['webserviceurl'])
        assignmentsPDF = pd.DataFrame(output)
        labelsList = list(set(assignmentsPDF[args[0]].to_list()))
        labelsList.sort()
        options = [{'label': ky, 'value': ky} for ky in labelsList]
        return (options,)

    def get_filtered_framework_assignments(self, *args, **kwargs):
        # args=(1,4,70,'01/01/2023','17/01/2023')
        fulloutputPDF = pd.DataFrame(
            self.get_assignments_grades_with_competency(kwargs['webserviceurl']))
        output = fulloutputPDF[fulloutputPDF[args[0]].isin(
            args[1])].to_dict(orient='records')
        div = self.dict_2_table_div(output)
        return (div, json.dumps(output))

    def download_csv(self, *args, **kwargs):
        if args[0] is None:
            raise PreventUpdate

        dataPDF = pd.DataFrame(json.loads(args[1]))
        return (dcc.send_data_frame(dataPDF.to_csv, 'downloaded.csv', index=False),)

##########################
# Unused
##########################
    # def get_schedule_events_course(self,*args,**kwargs):
    #     apimethod='get_schedule_events_course'
    #     apidata={"courseid":args[1],"schedulerid":args[2]}
    #     response=self.call_lrm_web_API(kwargs['webserviceurl'],apimethod,apidata).json()
    #     print(response)
    #     eventsList=response['response']
    #     return (eventsList,)
