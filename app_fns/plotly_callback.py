def wrapper_fn(func): 
     
    def inner1(*x,**a): 
        c=func(*x,**a) 
        return c
            
    return inner1 
    
def tealPythonWrapper(functionName,*fnVaraibles,**functionParameters):
    '''functionParameters is a dictionary of the parameters to be passed to the function'''
    
    function_to_be_called = wrapper_fn(functionName)  
    return function_to_be_called(*fnVaraibles,**functionParameters)


class plotly_call_back:
    def __init__(self):
        self.response=[]

    def get_inputs_give_outputs(self,app,callBackInput,**kwargs):
        self.fnParams=kwargs['fnParams']
        self.callbkfn=kwargs['callbackfunction']

        @app.callback(callBackInput, prevent_initial_call=True)
        def update_app(*inputvalue):
            callBackOutput=tealPythonWrapper(self.callbkfn,*inputvalue,**self.fnParams)
            return callBackOutput
