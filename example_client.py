from tp.client import Client


client = Client('http://localhost:5000')
print('resources:', client.resources)

users = client.resource('users')
print('users:', users.schema)

user = users.create(dict(username='sp'))

sp_user = users.get(1)
print(sp_user)

sp_user['username'] = 'test'
users.save(sp_user)
print(sp_user)
print(users.list())
users.delete(sp_user.get('id'))
print(users.list())
