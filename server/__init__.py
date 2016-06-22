import json

from flask import Flask, request
from sqlalchemy_wrapper import SQLAlchemy


class Server(object):

    def __init__(self):
        self._app = Flask('')
        self._resources = []

    def init_db(self, connection_uri):
        self._db = SQLAlchemy(connection_uri)
        return self._db

    def register(self, model):
        resource = Resource(model)
        self._resources.append(resource)
        self._add_rules(resource)
        return model

    def run_server(self):
        self._app.run(debug=True)

    def _add_rules(self, resource):
        app = self._app
        app.add_url_rule('{}/_schema'.format(resource.route),
                         '{}-schema'.format(resource.name),
                         view_func=resource.schema_view())

        resource_view = resource.resource_view()
        app.add_url_rule('{}/'.format(resource.route),
                         view_func=resource_view, methods=('GET', 'POST'))
        app.add_url_rule('{}/<int:id>'.format(resource.route),
                         view_func=resource_view, methods=('GET', 'PUT', 'DELETE'))


class Resource(object):

    def __init__(self, model):
        self.name = model.__tablename__
        self.route = '/{}'.format(self.name)
        self.columns = model.__table__.columns

    def schema_view(self):
        schema = json.dumps(dict(keys=self.columns.keys()))
        return lambda: schema

    def resource_view(self):
        def view(id=None):
            resource = view.resource
            method = request.method

            if method == 'GET':
                if not id:
                    return resource.index()
                else:
                    return resource.show(id)
            elif method == 'POST':
                return resource.create()
            elif method == 'PUT':
                return resource.update(id)
            elif method == 'DELETE':
                return resource.delete(id)

        view.resource = self
        return view

    def index(self):
        return 'index'

    def create(self):
        return 'create'

    def show(self, id):
        return 'show'

    def update(self, id):
        return 'update'

    def delete(self, id):
        return 'delete'
