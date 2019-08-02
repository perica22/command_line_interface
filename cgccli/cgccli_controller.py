import os
import re
import requests

from cgccli.api_service import ApiService



#tuple of nested object in case update call is sent
DICT_UPDATE = ('metadata', 'tags')

class CgccliController:
    """
    Prepering data for API calls
    Args:
        token: used to make instance of API service
    """
    def __init__(self, token):
        self.api_service = ApiService(token)

    def make_project_call(self, action):
        """
        Projects API call
        """
        if action == 'list':
            return self.api_service.get(endpoint='projects/')

    def make_files_call(self, action, **kwargs):
        """
        Files API calls
        Args:
            action:
        kwargs:
            data: request body data
            file: files on which change is made
            dest: path in which file will be downloaded
        """
        if action == 'list': # in case list is passed as 2nd argument
            return self.api_service.get(
                endpoint="files", query="?project=%s/" % (kwargs['project']))

        if action == 'update': # in case update is passed as 2nd argument
            endpoint_extension, data = self._determine_endpoint_extension_and_data(kwargs['data'])

            # determing based on endpoint_extension which call needs to be made
            if endpoint_extension:
                return self.api_service.put(
                    endpoint="files/{}/{}".format(
                        kwargs['file'], endpoint_extension), data=data)

            return self.api_service.patch(
                endpoint="files/{}/".format(kwargs['file']), data=kwargs['data'])

        if action == 'stat': # in case stat is passed as 2nd argument
            return self.api_service.get(endpoint="files/{}/".format(kwargs['file']))

        if action == 'download': # in case download is passed as 2nd argument
            response = self.api_service.get(
                endpoint="files/{}/download_info/".format(kwargs['file']))
            file_name = self._download_file(response['url'], kwargs['dest'])

            return 'Downloaded: %s' % (file_name)

    def _determine_endpoint_extension_and_data(self, data):
        """
        Changing endpoint in case nested data needs to be updated
        Args:
            data: rquest body
        Returns:
            endpoint_extension: endpoint extension in case of nested data update
            data: modified request body
        """
        data = re.findall(r"[\w']+", ' '.join(data))

        endpoint_extension = None
        if data[0] in DICT_UPDATE: # checkign if zeroth element exsists in predifined tuple
            endpoint_extension = data.pop(0)

        return endpoint_extension, data

    def _download_file(self, url, file_path):
        """
        Method downloading the file
        Args:
            url: URL from which file needs to be downloaded
            file_path: PATH where to download file localy
        Exception:
            IndexError: thrown on checking for eisting PATH locally
        Returns:
            file name which is downloaded
        """
        # make sure we have the download directory
        if '/' in file_path:
            path = file_path.split('/') # splitting path
            file_path = path.pop(-1) # last element from list is file name
            try:
                os.stat(path[0])
            except IndexError:
                # going through path list, making dir and cd into it
                for path_dir in path:
                    os.mkdir(path_dir)
                    os.chdir(path_dir)

        with open(file_path, "wb") as dl_dir:
            response = requests.get(url)  # get request
            dl_dir.write(response.content) # write to file
            return file_path
