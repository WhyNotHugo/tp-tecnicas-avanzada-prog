import json

from collections import OrderedDict

from flask import Flask, request, jsonify
from sqlalchemy_wrapper import SQLAlchemy

from werkzeug.exceptions import default_exceptions, HTTPException, \
    BadRequest, NotFound
from sqlalchemy.exc import IntegrityError


class Server(object):

    def __init__(self):
        self.app = Flask('')
        self.resources = []
        self.register_error_handler()

    def init_db(self, connection_uri):
        self.db = SQLAlchemy(connection_uri, app=self.app)
        return self.db

    def register(self, model):
        model.columns = model.__table__.columns.values()
        resource = Resource(model)
        self.resources.append(resource)
        self.add_rules(resource)
        return model

    def register_error_handler(self):
        def error_handler(e):
            if isinstance(e, HTTPException):
                response = jsonify(error=str(e), message=e.get_description())
            else:
                response = jsonify(error='Internal Server Error')
            response.status_code = getattr(e, 'code', 500)
            return response

        app = self.app
        for code in default_exceptions.keys():
            app.register_error_handler(code, error_handler)

    def add_rules(self, resource):
        self.app.add_url_rule(
            '{}/_schema'.format(resource.route),
            '{}-schema'.format(resource.name),
            view_func=resource.schema_view()
        )

        resource_view = resource.resource_view()
        self.app.add_url_rule(
            '{}/'.format(resource.route),
            view_func=resource_view,
            methods=('GET', 'POST')
        )
        self.app.add_url_rule(
            '{}/<int:id>'.format(resource.route),
            view_func=resource_view,
            methods=('GET', 'PUT', 'DELETE')
        )

        self.register_endpoints_view()

    def register_endpoints_view(self):
        endpoints = json.dumps([resource.name for resource in self.resources])

        @self.app.route('/_endpoints')
        def endpoints_view():
            return endpoints

    def run_server(self):
        self.app.run()


class Resource(object):

    def __init__(self, model):
        self.model = model
        self.name = model.__tablename__
        self.route = '/{}'.format(self.name)

    def schema_view(self):
        columns = [(column.name, {
            'type': column.type.python_type.__name__,
            'primary_key': column.primary_key
        }) for column in self.model.columns]
        schema = json.dumps(columns)
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
        return jsonify(self.model.index())

    def create(self):
        return jsonify(self.model.create(request.json)), 201

    def show(self, id):
        return jsonify(self.model.show(id))

    def update(self, id):
        return jsonify(self.model.update(id, request.json))

    def delete(self, id):
        return jsonify(self.model.delete(id))


class ModelMixin(object):

    @classmethod
    def index(cls):
        return [x.to_dict() for x in cls.db.query(cls).all()]

    @classmethod
    def create(cls, data):
        x = cls()
        for column in cls.columns:
            setattr(x, column.name, data.get(column.name))

        try:
            cls.db.add(x)
            cls.db.commit()
        except IntegrityError as e:
            raise BadRequest(str(e))
        return x.to_dict()

    @classmethod
    def show(cls, id):
        return cls.db.query(cls).get_or_error(id, NotFound()).to_dict()

    @classmethod
    def update(cls, id, data):
        x = cls.db.query(cls).get_or_error(id, NotFound())
        for column in cls.columns:
            if column.name in data:
                setattr(x, column.name, data.get(column.name))

        try:
            cls.db.add(x)
            cls.db.commit()
        except IntegrityError as e:
            raise BadRequest(str(e))
        return x.to_dict()

    @classmethod
    def delete(cls, id):
        x = cls.db.query(cls).get_or_error(id, NotFound())
        cls.db.delete(x)
        cls.db.commit()

    def to_dict(self):
        return OrderedDict([
            (column.name, getattr(self, column.name))
            for column in self.columns
        ])
