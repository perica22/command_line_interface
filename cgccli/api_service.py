# IMPORTS
import json

from functools import wraps
from requests import request



def determine_endpoint_url(f):
    @wraps(f)
    def wrapped(self, **kwargs):
        endpoint = kwargs.get('endpoint', None)
        query = kwargs.get('query', None)

        url = 'https://cgc-api.sbgenomics.com/v2/' + endpoint
        if query:
            url = url + query 
        kwargs['url'] = url

        return f(self, **kwargs)

    return wrapped

def get_data_for_request(f):
    @wraps(f)
    def wrapped(self, **kwargs):

        data = kwargs.get('data', None)
        if data:
            if 'tags' in kwargs['endpoint']:
                data = json.dumps(data)
            else:
                data = json.dumps({data[0]: data[1]})

        kwargs['data'] = data

        return f(self, **kwargs)

    return wrapped


#  CLASSES
class ApiService:
    # making a class out of the api() function, adding other methods
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
