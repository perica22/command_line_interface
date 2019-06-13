import os
import re
import requests

from cgccli.api_service import ApiService
from cgccli.utils import noCommandFound, DICT_UPDATE



class CgccliController:

    def __init__(self, token):
        self.api_service = ApiService(token)

    def make_project_call(self, action):
        '''
        Projects call
        '''
        #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c projects list
        if action == 'list':
            return self.api_service.get(endpoint='projects/') 

    def make_files_call(self, action, project=None, data=None, file=None, dest=None):
        '''
        Files calls
        '''
        if action == 'list':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files list --project perica22/copy-of-cancer-cell-line-encyclopedia-ccle
            return self.api_service.get(
                endpoint="files", query="?project=%s/" % (project))

        elif action == 'update':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files update --file 5cff5ac9e4b04e1432b04164 tags=["marina", "perica", "nikola", "jovica"]
            endpoint_extension, data = self._determine_endpoint_extension_and_data(data)
            if endpoint_extension:
                return self.api_service.put(
                    endpoint="files/{}/{}".format(file, endpoint_extension), data=data)
            else:
                return self.api_service.patch(
                    endpoint="files/{}/".format(file), data=data)

        elif action == 'stat':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files stat --file 5cff5ac9e4b04e1432b04164
            return self.api_service.get(endpoint="files/{}/".format(file))

        elif action == 'download':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files download --file 5cff5ac9e4b04e1432b04164 --dest perica.txt
            response = self.api_service.get(
                endpoint="files/{}/download_info/".format(file))
            file_name = self._downloadFile(response['url'], dest)
            return 'Downloaded: %s' % (file_name)

    def _determine_endpoint_extension_and_data(self, data):
        '''
        Changing endpoint in case nested data needs to be updated
        '''
        data = re.findall(r"[\w']+", ' '.join(data))
        
        endpoint_extension = None
        if data[0] in DICT_UPDATE:
            endpoint_extension = data.pop(0)
        return endpoint_extension, data

    def _downloadFile(self, url, file_path):
        '''
        Method downloading the file
        '''
        # make sure we have the download directory
        if '/' in file_path:
            path = file_path.split('/')
            file_path = path.pop(-1)
            try:
                os.stat(path[0])
            except:
                for path_dir in path:
                    os.mkdir(path_dir)
                    os.chdir(path_dir)

        with open(file_path, "wb") as dl_dir:
            response = requests.get(url)  # get request
            dl_dir.write(response.content) # write to file
            return file_path
