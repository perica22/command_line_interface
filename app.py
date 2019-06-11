# IMPORTS
import time as timer
from requests import request
import json
from urllib2 import urlopen
import os


# GLOBALS
FLAGS = {'targetFound': False,                  # target project exists in CGC project
         'taskRunning': False,                  # task is still running
         'startTasks': True                     # (False) create, but do NOT start tasks
        }
# project we will create in CGC (Settings > Project name in GUI)
TARGET_PROJECT = 'Copy of Cancer Cell Line Encyclopedia (CCLE)'               
TARGET_APP = 'RNA-seq Alignment - STAR for TCGA PE tar' # app to use
INPUT_EXT = 'tar.gz'

# TODO: replace AUTH_TOKEN with yours here
AUTH_TOKEN = '194a5e2aeb4447f5b6f9f56d85bf786c'


#  FUNCTIONS
def api_call(path, method='GET', query=None, data=None, flagFullPath=False):
    """ Translates all the HTTP calls to interface with the CGC

    This code adapted from the Seven Bridges platform API v1.1 example
    https://docs.sbgenomics.com/display/developerhub/Quickstart
    flagFullPath is novel, added to smoothly resolve pagination issues with the CGC API"""
    data = json.dumps(data) if isinstance(data, dict) or isinstance(data,list)  else None
    base_url = 'https://cgc-api.sbgenomics.com/v2/'

    headers = {
        'X-SBG-Auth-Token': AUTH_TOKEN,
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }

    if flagFullPath:
        response = request(method, path, params=query, data=data, headers=headers)
    else:
        response = request(method, base_url + path, params=query, data=data, headers=headers)
    response_dict = json.loads(response.content) if response.content else {}

    if response.status_code / 100 != 2:
        print response_dict['message']
        raise Exception('Server responded with status code %s.' % response.status_code)
    return response_dict

def hello():  # for debugging
    print("Is it me you're looking for?")
    return True


#  CLASSES
class API(object):
    # making a class out of the api() function, adding other methods
    def __init__(self, path, method='GET', query=None, data=None, flagFullPath=False):
        self.flag = {'longList': False}
        response_dict = api_call(path, method, query, data, flagFullPath)
        self.response_to_fields(response_dict)

        if self.flag['longList']:
            self.long_list(response_dict, path, method, query, data)

    def response_to_fields(self,rd):
        if 'items' in rd.keys():  
            # get * {files, projects, tasks, apps} (object name plural)
            if len(rd['items']) > 0:
                self.list_read(rd)
            else:
                self.empty_read(rd)
        else:           
            # get details about ONE {file, project, task, app}  
            #  (object name singular)
            self.detail_read(rd)

    def list_read(self,rd):
        n = len(rd['items'])
        keys = rd['items'][0].keys()
        m = len(keys)

        for jj in range(m):
            temp = [None]*n
            for ii in range(n):
                temp[ii] = rd['items'][ii][keys[jj]]
            setattr(self, keys[jj], temp)

        if ('links' in rd.keys()) & (len(rd['links']) > 0):
            self.flag['longList'] = True

    def empty_read(self,rd):  # in case an empty project is queried
        self.href = []
        self.id = []
        self.name = []
        self.project = []

    def detail_read(self,rd):
        keys = rd.keys()
        m = len(keys)

        for jj in range(m):
            setattr(self, keys[jj], rd[keys[jj]])

    def long_list(self, rd, path, method, query, data):
        prior = rd['links'][0]['rel']
        # Normally .rel[0] is the next, and .rel[1] is prior. 
        # If .rel[0] = prior, then you are at END_OF_LIST
        keys = rd['items'][0].keys()
        m = len(keys)

        while prior == 'next':
            rd = api_call(rd['links'][0]['href'], method, query, data, flagFullPath=True)
            prior = rd['links'][0]['rel']
            n = len(rd['items'])
            for jj in range(m):
                temp = getattr(self, keys[jj])
                for ii in range(n):
                    temp.append(rd['items'][ii][keys[jj]])
                setattr(self, keys[jj], temp)


if __name__ == "__main__":
    # Did you remember to change the AUTH_TOKEN?
    if AUTH_TOKEN == 'AUTH_TOKEN':
        print "You need to replace 'AUTH_TOKEN' string with your actual token. Please fix it."
        exit()
    # list all billing groups on your account
    billingGroups = API('billing/groups')
    # Select the first billing group, this is "Pilot_funds(USER_NAME)"
    print billingGroups.name[0], \
    'will be charged for this computation. Approximate price is $4 for example STAR RNA seq (n=1) \n'
 
    # list all projects you are part of
    existingProjects = API(path='projects')     # make sure your project doesn't already exist
    import ipdb
    ipdb.set_trace()
    print(existingProjects)
    # set up the information for your new project
    NewProject = {
            'billing_group': billingGroups.id[0],
            'description': "A project created by the API Quickstart",
            'name': TARGET_PROJECT,
            'tags': ['tcga']
    }
 
    # Check to make sure your project doesn't already exist on the platform
    for ii,p_name in enumerate(existingProjects.name):
        if TARGET_PROJECT == p_name:
            FLAGS['targetFound'] = True
            break
 
    # Make a shiny, new project
    if FLAGS['targetFound']:
        myProject = API(path=('projects/' + existingProjects.id[ii]))    
        # GET existing project details (we need them later)
    else:
        myProject = API(method='POST', data=NewProject, path='projects') 
        # POST new project
        # (re)list all projects, to check that new project posted
        existingProjects = API(path='projects')
        # GET new project details (we will need them later)
        myProject = API(path=('projects/' + existingProjects.id[0]))    
        # GET new project details (we need them later)
