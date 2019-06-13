# IMPORTS
import json
from requests import request

from cgccli.utils import determine_endpoint_url, get_data_for_request



class ApiService:
    '''
    Making a class out of the API 
    '''
    def __init__(self, token):
        self.headers = {
            "X-SBG-Auth-Token": token,
            "Accept":"application/json",
            "Content-Type":"application/json"
            }

    @determine_endpoint_url
    def get(self, **kwargs):
        return self._request('get', **kwargs)

    @determine_endpoint_url
    @get_data_for_request
    def put(self, **kwargs):
        return self._request('put', **kwargs)

    @determine_endpoint_url
    @get_data_for_request
    def patch(self, **kwargs):
        return self._request('patch', **kwargs)

    def _request(self, method, **kwargs):
        """
        Translates all the HTTP calls to interface with the CGC
        """
        data = kwargs.get('data', None)
        url = kwargs.get('url')

        response = request(
            method, url, data=data, headers=self.headers)

        response_dict = json.loads(response.content) if response.content else {}
        if response.status_code / 100 != 2:
            return response_dict['message']

        return response_dict
