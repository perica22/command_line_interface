# IMPORTS
from requests import request
import json
import functools
import requests



def determine_endpoint_url(f):
    @functools.wraps(f)
    def wrapped(self, **kwargs):
        endpoint = kwargs.get('endpoint', None)
        query = kwargs.get('query', None)

        url = 'https://cgc-api.sbgenomics.com/v2/' + endpoint
        if query:
            url = url + query 
        defaults = {'url': url}
        defaults.update(kwargs)

        return f(self, **defaults)

    return wrapped

def get_data_for_request(f):
    @functools.wraps(f)
    def wrapped(self, **kwargs):
        data = kwargs.get('data', None)
        data = json.dumps(data) if isinstance(data, dict) or isinstance(data,list)  else None
        defaults = {'data': data}
        defaults.update(kwargs)
        return f(self, **defaults)

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
    @get_data_for_request
    def get(self, **kwargs):
        return self._request('get', **kwargs)

    @determine_endpoint_url
    @get_data_for_request
    def put(self, **kwargs):
        return self._request('put', **kwargs)

    def _request(self, method, **kwargs):
        """
        Translates all the HTTP calls to interface with the CGC
        """
        data = kwargs.get('data')
        url = kwargs.get('url')

        response = request(
            method, url, data=data, headers=self.headers)
        #response = getattr(requests, method)(url, data, headers=self.headers)
        response_dict = json.loads(response.content) if response.content else {}
        if response.status_code / 100 != 2:
            print(response_dict['message'])
            raise Exception('Server responded with status code %s.' % response.status_code)
        return response_dict
