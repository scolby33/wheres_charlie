from flask_jwt import JWT
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_security.utils import verify_and_update_password

from . import app, handlers, models


def authenticate(username, password, scopes):
    user = user_datastore.get_user(username)
    if user and verify_and_update_password(password, user):
        scope_perms = []
        for scope in scopes:
            scope_perms.append(user.has_role(scope))
        if all(scope_perms):
            return user


def identity(payload):
    user_id = payload['sub']
    return user_datastore.get_user(user_id)

user_datastore = SQLAlchemyUserDatastore(models.db, models.User, models.Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_default_user():
    models.db.create_all()
    new_role = user_datastore.find_or_create_role('admin')
    new_user = user_datastore.create_user(name='scott', password='pass')
    user_datastore.add_role_to_user(new_user, new_role)
    models.db.session.commit()
    new_location = models.Location(user_id=new_user.user_id, location_string='Timbuktu')
    models.db.session.add(new_location)
    models.db.session.commit()

models.db.create_all()

jwt = JWT(app=None, authentication_handler=authenticate, identity_handler=identity)
jwt.app = app
jwt.auth_request_callback = handlers.auth_request_handler
jwt.jwt_encode_callback = handlers.encode_handler
jwt.jwt_payload_callback = handlers.payload_handler
jwt.auth_response_callback = handlers.auth_response_handler
jwt.init_app(jwt.app)
