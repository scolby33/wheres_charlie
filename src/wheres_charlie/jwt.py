from flask_jwt import JWT
from flask_security.utils import verify_and_update_password
from werkzeug.security import safe_str_cmp

from . import app, handlers, models

def authenticate(username, password, scopes):
    user = models.user_datastore.get_user(username)
    if user and verify_and_update_password(password, user):
        scope_perms = []
        for scope in scopes:
            scope_perms.append(user.has_role(scope))
        if all(scope_perms):
            return user


def identity(payload):
    user_id = payload['sub']
    return models.user_datastore.get_user(user_id)

jwt = JWT(app=None, authentication_handler=authenticate, identity_handler=identity)
jwt.app = app
jwt.auth_request_callback = handlers.auth_request_handler
jwt.jwt_encode_callback = handlers.encode_handler
jwt.jwt_payload_callback = handlers.payload_handler
jwt.auth_response_callback = handlers.auth_response_handler
jwt.init_app(jwt.app)
