from serverConfig import *
import json
from flask import request, jsonify, Flask
from flask_restful import reqparse

import sys
sys.path.append('../')


def test_fn(a):
    return a


method_names = {'test_fn': test_fn}


def wrapper_fn(func):

    def inner1(**a):
        c = func(**a)
        return c

    return inner1


def tealPythonWrapper(functionName, **functionParameters):
    '''functionParameters is a dictionary of the parameters to be passed to the function'''

    function_to_be_called = wrapper_fn(functionName)
    return function_to_be_called(**functionParameters)


def web_API(app):
    # app = Flask(__name__)
    # run_with_ngrok(app) #Comment to run on server
    @app.route("/{}/api/".format(moodlename))
    def home():
        # "<marquee><h3> App description.</h3></marquee>"
        return '<h3> POST111 site URL/input?method=fn_name&data={"arg1":arg1,"arg2":arg2,"arg3":arg3} </h3>'

    @app.route("/{}/api/input".format(moodlename), methods=['GET', 'POST'])
    def get_method():
        method = request.args.get('method')
        data = request.args.get('data')
        response = tealPythonWrapper(method_names[method], **json.loads(data))
        return jsonify(response)

    @app.route("/{}/api/postcall".format(moodlename), methods=['POST'])
    def postmethod():
        postdata = request.json
        method = postdata['method']
        data = postdata['data']
        response = tealPythonWrapper(method_names[method], **data)
        return jsonify(response), 200

    @app.route("/api/gitupdate", methods=['GET', 'POST'])
    def get_method2():
        import os
        out = os.system("/home/ubuntu/mugas_python_methods/updateFromGh.sh")

        return (str(out))

    @app.route('/api/output', methods=['POST'])
    def post_method():
        method = request.args.get('method')
        data = request.args.get('data')
        response = tealPythonWrapper(method_names[method], **json.loads(data))

        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('request', required=True)
        parser.add_argument('data', required=True)
        args = parser.parse_args()
        response = tealPythonWrapper(
            method_names[args['request']], **json.loads(args['data']))
        return jsonify(response)
    # return app.run()
    return app
