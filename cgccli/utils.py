import json
from click import echo
from functools import wraps



#tuple of nested object in case update call is sent 
DICT_UPDATE = ('metadata', 'tags') 

# function returnign error in case unknown cl argument is passed
def noCommandFound(command):
    echo('No such command: {}'.format(command))

# decoreator determening endpoint url before making API call
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

# decoreator doing proper nesting of data before making API call
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
