import requests

HEADERS = {'Content-Type': 'application/json'}


class Client(object):

    def __init__(self, url):
        self.url = url

    @property
    def resources(self):
        try:
            return self._resources
        except AttributeError:
            r = requests.get('{}/_endpoints'.format(self.url), headers=HEADERS)
            r.raise_for_status()
            self._resources = r.json()
            return self._resources

    def resource(self, resource_name):
        return Resource(self.url, 'users')


class Resource(object):

    def __init__(self, url, resource):
        self.url = '{}/{}/'.format(url, resource)

    def _make_request(self, method, sub=None, data=None):
        url = '{}{}'.format(self.url, sub) if sub else self.url
        r = requests.request(method, url, json=data, headers=HEADERS)
        r.raise_for_status()
        return r.json()

    @property
    def schema(self):
        try:
            return self._schema
        except AttributeError:
            self._schema = self._make_request('get', sub='_schema')
            return self._schema

    def list(self):
        return self._make_request('get')

    def create(self, data):
        return self._make_request('post', data=data)

    def get(self, id):
        return self._make_request('get', sub=id)

    def update(self, id, data):
        return self._make_request('put', sub=id, data=data)

    def delete(self, id):
        return self._make_request('delete', sub=id)

    def save(self, data):
        if 'id' in data:
            self.update(data.get('id'), data)
        else:
            self.create(data)
