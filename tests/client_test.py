import json
import unittest

from httmock import urlmatch, HTTMock

from tp.client import Client


@urlmatch(netloc=r'(.*\.)?test\.com/?(.*)')
def schema_mock(url, request):
    if url.path == '/_endpoints':
        return '["users"]'
    elif url.path == '/users/_schema':
        schema = [
            ['id', {'primary_key': True, 'type': 'int'}],
            ['username', {'primary_key': False, 'type': 'str'}],
        ]
        return json.dumps(schema)
    elif url.path == '/users/':
        assert request.method == 'POST'
        assert request.body == b'{"username": "john doe"}'
        return request.body.decode()
    else:
        return {'status_code': 404}


class TestClient(unittest.TestCase):

    def test_client(self):
        with HTTMock(schema_mock):
            client = Client('http://test.com')

            self.assertEqual(
                client.resources,
                ['users'],
            )
            users = client.resource('users')

            users.create(dict(username='john doe'))
