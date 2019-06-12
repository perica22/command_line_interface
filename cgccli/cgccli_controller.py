import requests
from cgccli.api_service import ApiService


class CgccliController:
    def __init__(self, token, argument, project=None, file=None, data=None, dest=None):
        self.token = token
        self.object = argument[0]
        self.action = argument[1]
        self.file = file
        self.dest = dest
        self.api_service = ApiService(token)


    def make_call(self):
        if self.object == 'projects':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c projects list
            response = self.api_service.get(endpoint='projects/')   
            return response

        elif self.object == 'files':
            if self.action == 'update':
                response = self._update_method()

            elif self.action == 'stat':
                response = self._stat_method()

            elif self.action == 'download':
                response = self._download_method()

    def _download_method(self):
        #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files download --file 5cff5ac9e4b04e1432b04164 --dest perica.txt
        response = self.api_service.get(
            endpoint="files/{}/download_info/".format(self.file))
        content = self._downloadFile(response['url'], self.dest)
        return response

    def _downloadFile(self, url, file_name):
        with open(file_name, "wb") as file:
            # get request
            response = requests.get(url)
            # write to file
            file.write(response.content)


'''
if argument[0] == 'files':
        if argument[1] == 'list':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files list --project perica22/copy-of-cancer-cell-line-encyclopedia-ccle
            response = api_service.get(
                endpoint="files", query="?project={}/".format(project))

        elif argument[1] == 'update':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files update --file 5cff5ac9e4b04e1432b04164 tags=["marina", "perica", "nikola", "jovica"]
            
            data = re.findall(r"[\w']+", ' '.join(data))

            if data[0] in dict_update:
                endpoint_extension = data.pop(0)

                response = api_service.put(
                    endpoint="files/{}/{}".format(file, endpoint_extension), data=data)
            else:
                response = api_service.patch(
                    endpoint="files/{}/".format(file), data=data)

        elif argument[1] == 'stat':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files stat --file 5cff5ac9e4b04e1432b04164
            response = api_service.get(endpoint="files/{}/".format(file))

        elif argument[1] == 'download':
            #cgccli --token 194a5e2aeb4447f5b6f9f56d85bf786c files download --file 5cff5ac9e4b04e1432b04164 --dest perica.txt
            response = api_service.get(
                endpoint="files/{}/download_info/".format(file))
            content = downloadFile(response['url'], dest)
            '''