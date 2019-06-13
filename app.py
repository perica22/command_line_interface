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
        self.path = path
        self.method = method
        self.query = query
        self.data = data
        self.flagFullPath = flagFullPath
        
        #if self.flag['longList']:
         #   self.long_list(response_dict, path, method, query, data)

    def make_call(self):
        response = api_call(self.path, self.method, self.query, self.data, self.flagFullPath)        
        return response

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

  
def download_files(fileList):
    # download a list of files from URLs
    dl_dir = 'downloads/'
    import ipdb
    ipdb.set_trace()
    try:                    # make sure we have the download directory
        os.stat(dl_dir)
    except:
        os.mkdir(dl_dir)
  
    for ii in range(1, len(fileList)):  # skip first [0] entry, it is a text header
        url = fileList[ii]
        file_name = url.split('/')[-1]
        file_name = file_name.split('?')[0]
        #file_name = file_name.split('%2B')[1]
        u = urlopen(url)
        f = open((dl_dir + file_name), 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
  
        file_size_dl = 0
        block_sz = 1024*1024
        prior_percent = 0
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            if (file_size_dl * 100. / file_size) > (prior_percent+20):
                print status + '\n'
                prior_percent = (file_size_dl * 100. / file_size)
        f.close()
  

if __name__ == "__main__":
    
    # Check which files have been generated (only taking small files to avoid long times)
    myNewFiles = API('files?project=perica22/copy-of-cancer-cell-line-encyclopedia-ccle') 
    response = myNewFiles.make_call() # calling again to see what was generated
    dlList = [i['href'] for i in response['items']]

    '''for ii, f_name in enumerate(myNewFiles.name):
        # downloading only the summary files. Adapt for whichever files you need
        if (f_name[-4:] == '.out'):
            dlList.append(api_call(path=('files/' + myNewFiles.id[ii] + '/download_info'))['url'])'''
    T0 = timer.time()
    download_files(dlList)
    print timer.time() - T0, "seconds download time"


