from server import Server


app = Server()
db = app.init_db('sqlite://')


@app.register
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


if __name__ == '__main__':
    db.create_all()
    app.run_server()

