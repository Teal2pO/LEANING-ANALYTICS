from requests import get, post
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

class moodle_web_service:
    def __init__(self,mWAParams):
        self.mWAP=mWAParams

    def rest_api_parameters(self, in_args, prefix='', out_dict=None):
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

    def call(self, accessParams, fname, **kwargs):
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
