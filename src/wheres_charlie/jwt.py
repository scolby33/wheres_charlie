from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

from . import app, handlers


class User(object):
    def __init__(self, user_id, username, password, allowed_scopes):
        self.id = user_id
        self.username = username
        self.password = password
        self.allowed_scopes = allowed_scopes

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz', {'test'}),
    User(2, 'user2', 'abcxyz', {'test'}),
]

username_table = {u.username: u for u in users}
user_id_table = {u.id: u for u in users}


def authenticate(username, password, scopes):
    user = username_table.get(username, None)
    if (user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')) and
            scopes.issubset(user.allowed_scopes)):
        return user


def identity(payload):
    user_id = payload['sub']
    return user_id_table.get(user_id, None)

app.app.config['JWT_SECRET_KEY']= 'secret'
app.app.config['JWT_AUTH_SCOPES_KEY'] = 'scopes'

jwt = JWT(app=None, authentication_handler=authenticate, identity_handler=identity)
jwt.app = app.app
jwt.auth_request_callback = handlers.auth_request_handler
jwt.jwt_encode_callback = handlers.encode_handler
jwt.jwt_payload_callback = handlers.payload_handler
jwt.auth_response_callback = handlers.auth_response_handler
jwt.init_app(jwt.app)
