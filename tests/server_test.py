import json
import unittest

from tp.server import ModelMixin, Server


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        app = Server()
        app.app.config['TESTING'] = True

        self.app = app
        self.db = app.init_db('sqlite://')

        self.TestClient = app.app.test_client

        @self.app.register
        class User(self.db.Model, ModelMixin):
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(
                self.db.String, unique=True, nullable=False,
            )

        self.db.create_all()
        self.user_class = User


class TestSchema(ServerTestCase):

    def test_schema(self):
        response = self.TestClient().get('/users/_schema')

        schema = json.loads(response.data.decode())
        expecte_schema = [
            ['id', {'primary_key': True, 'type': 'int'}],
            ['username', {'primary_key': False, 'type': 'str'}],
        ]

        schema.sort()

        self.assertEqual(
            schema,
            expecte_schema,
        )


class TestList(ServerTestCase):

    def test_empty(self):
        response = self.TestClient().get('/users/')
        users = json.loads(response.data.decode())
        self.assertEqual(users, [])

    def test_several(self):
        self.db.session.add(self.user_class(username='john doe'))
        self.db.session.add(self.user_class(username='jane smith'))

        response = self.TestClient().get('/users/')

        users = json.loads(response.data.decode())

        self.assertEqual(users, [
            {'id': 1, 'username': 'john doe'},
            {'id': 2, 'username': 'jane smith'}
        ])


class TestFetch(ServerTestCase):

    def test_fetch_existing(self):
        self.db.session.add(self.user_class(username='john doe'))
        response = self.TestClient().get('/users/1')
        user = json.loads(response.data.decode())

        self.assertEqual(user, {'id': 1, 'username': 'john doe'})

    def test_fetch_inexisting(self):
        response = self.TestClient().get('/users/7')
        self.assertEqual(response.status_code, 404)


class TestDelete(ServerTestCase):

    def test_delete_existing(self):
        self.db.session.add(self.user_class(username='john doe'))
        response = self.TestClient().delete('/users/1')

        response = self.TestClient().get('/users/')
        users = json.loads(response.data.decode())
        self.assertEqual(users, [])

    def test_delete_unexisting(self):
        response = self.TestClient().delete('/users/1')

        self.assertEqual(response.status_code, 404)
