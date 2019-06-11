# IMPORTS
from requests import request
import json



#  CLASSES
class API(object):
    # making a class out of the api() function, adding other methods
    def __init__(self, path, headers, method='GET', query=None, data=None, flagFullPath=False):
        self.headers = headers
        self.path = path
        self.method = method
        self.query = query
        self.data = data
        self.flagFullPath = flagFullPath
        #self.flag = {'longList': False}
        #response_dict = self._api_call(path, headers, method, query, data, flagFullPath)
        #self.response_to_fields(response_dict)
        #if self.flag['longList']:
        #    self.long_list(response_dict, headers, path, method, query, data)

    def api_call(self):
        """ Translates all the HTTP calls to interface with the CGC

        flagFullPath is novel, added to smoothly resolve pagination issues with the CGC API"""
        data = json.dumps(self.data) if isinstance(self.data, dict) or isinstance(self.data,list)  else None
        base_url = 'https://cgc-api.sbgenomics.com/v2/'

        if self.flagFullPath:
            response = request(
                self.method, self.path, params=self.query, data=self.data, headers=self.headers)
        else:
            response = request(
                self.method, base_url + self.path, params=self.query, data=self.data, headers=self.headers)
        response_dict = json.loads(response.content) if response.content else {}

        if response.status_code / 100 != 2:
            print response_dict['message']
            raise Exception('Server responded with status code %s.' % response.status_code)
        return response_dict

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

    def long_list(self, rd, headers, path, method, query, data):
        prior = rd['links'][0]['rel']
        # Normally .rel[0] is the next, and .rel[1] is prior. 
        # If .rel[0] = prior, then you are at END_OF_LIST
        keys = rd['items'][0].keys()
        m = len(keys)

        while prior == 'next':
            rd = self._api_call(rd['links'][0]['href'],headers, method, query, data, flagFullPath=True)
            prior = rd['links'][0]['rel']
            n = len(rd['items'])
            for jj in range(m):
                temp = getattr(self, keys[jj])
                for ii in range(n):
                    temp.append(rd['items'][ii][keys[jj]])
                setattr(self, keys[jj], temp)
