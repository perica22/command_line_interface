import json
from functools import wraps
from click import echo



# function returnign error in case unknown cl argument is passed
def no_command_found(command):
    echo('No such command: {}'.format(command))

# decoreator determening endpoint url before making API call
def determine_endpoint_url(function):
    @wraps(function)
    def wrapped(self, **kwargs):
        endpoint = kwargs.get('endpoint', None)
        query = kwargs.get('query', None)

        # concatenating string in order to get full url
        url = 'https://cgc-api.sbgenomics.com/v2/' + endpoint
        if query:
            url = url + query
        kwargs['url'] = url

        return function(self, **kwargs)

    return wrapped

# decoreator doing proper nesting of data before making API call
def get_data_for_request(function):
    @wraps(function)
    def wrapped(self, **kwargs):
        data = kwargs.get('data', None)
        if data:
            # in case tag is in endpoint we need to send list in body
            if 'tags' in kwargs['endpoint']:
                data = json.dumps(data)
            # nesting data with proper key
            else:
                data = json.dumps({data[0]: data[1]})

        kwargs['data'] = data

        return function(self, **kwargs)

    return wrapped
