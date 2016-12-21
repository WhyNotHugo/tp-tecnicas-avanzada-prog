from tp.server import ModelMixin, Server


app = Server()
db = app.init_db('sqlite://')


@app.register
class User(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)


if __name__ == '__main__':
    db.create_all()
    app.run_server()
