import re
import requests

from cgccli.api_service import ApiService



DICT_UPDATE = ('metadata', 'tags')

class CgccliController:

    def __init__(self, token, file=None, data=None, dest=None):
        self.api_service = ApiService(token)
        self.file = file
        self.dest = dest
        self.data = data

    def make_project_call(self, action):
        #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c projects list
        return self.api_service.get(endpoint='projects/')   

    def make_files_call(self, action):
        if action == 'list':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files list --project perica22/copy-of-cancer-cell-line-encyclopedia-ccle
            return api_service.get(
            endpoint="files", query="?project={}/".format(project))

        elif action == 'update':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files update --file 5cff5ac9e4b04e1432b04164 tags=["marina", "perica", "nikola", "jovica"]
            endpoint_extension = self._determine_endpoint_extension_and_method(self.data)
            if endpoint_extension:
                return api_service.put(
                    endpoint="files/{}/{}".format(file, endpoint_extension), data=data)
            else:
                return api_service.patch(
                    endpoint="files/{}/".format(file), data=data)

        elif action == 'stat':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files stat --file 5cff5ac9e4b04e1432b04164
            return self.api_service.get(endpoint="files/{}/".format(file))

        elif action == 'download':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files download --file 5cff5ac9e4b04e1432b04164 --dest perica.txt
            response = self.api_service.get(
                endpoint="files/{}/download_info/".format(self.file))
            self._downloadFile(response['url'], self.dest)
            return response

    def _determine_endpoint_extension_and_method(self):
        data = re.findall(r"[\w']+", ' '.join(data))

        if data[0] in DICT_UPDATE:
            endpoint_extension = data.pop(0)
        return endpoint_extension if endpoint_extension else None

    def _downloadFile(self, url, file_name):
        with open(file_name, "wb") as file:
            # get request
            response = requests.get(url)
            # write to file
            file.write(response.content)
