Server side
===========

Models are registered with the API by decorating them with @register::

    @register
    class User:
        pass

URLs
====

Endpoints
---------

Endpoints are listed by requesting ``/_endpoints``, for example::

    {
      "endpoints": [
        "/users",
        "/cars"
      ]
    }

Schemas
-------

Schemas are described by performing ``GET`` to a ``_schema`` to any endpoint,
for example::

    {
      "name": {
        "type": "str",
        "null": false
      },
      "id": {
        "type": "int",
        "pk": true
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

    c = Client("User")

    c.find(0)
    c.save(user)
      c.create(user)
      c.update(user)
    c.delete(user)
    c.list()

Note: ``save()`` will run a ``create`` if the object has no pk, or an
``update`` if it does.
