import json

from flask import Flask
from flask.views import MethodView
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
        self._app.add_url_rule('{}/_schema'.format(resource.route),
                               '{}-schema'.format(resource.name),
                               view_func=resource.schema_view())


class Resource(MethodView):

    def __init__(self, model):
        self.name = model.__tablename__
        self.route = '/{}'.format(self.name)
        self.columns = model.__table__.columns

    def schema_view(self):
        schema = json.dumps(dict(keys=self.columns.keys()))
        return lambda: schema

