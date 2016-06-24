Server side
===========

Models are registered with the API by decorating them with @app.register::

    @app.register
    class User:
        pass

URLs
====

Endpoints
---------

Endpoints are listed by requesting ``/_endpoints``, for example::

    [
      "/users",
      "/cars"
    ]

Schemas
-------

Schemas are described by performing ``GET`` to a ``_schema`` to any endpoint,
for example::

    {
      "id": {
        "type": "int",
        "pk": true
      },
      "name": {
        "type": "str",
        "null": false
      },
      "dateOfBirth": {
        "type": "timestamp",
        "null": "false"
      },
      "active": {
        "type": "boolean"
      },
      "cash": {
        "type": "float"
      },
      "mainCar": {
        "type": "relationship",
        "rel": "Car"
      },
      "cars": {
        "type": "relationship",
        "rel": "Car",
        "list": true
      }
    }

Client
------

The client auto-discovers schemas, and exposes a proxy to interact with the
API. These are the basic methods::

    client = Client('http://localhost')
    client.resources
    resource = client.resource('users')
    resource.schema
    resource.get(1)
    resource.save(user)
    resource.create(user)
    resource.update(id, user)
    resource.delete(id)
    resource.list()

Note: ``save()`` will run a ``create`` if the object has no pk, or an
``update`` if it does.
