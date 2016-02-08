import datetime

from flask_jwt import JWT
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import verify_and_update_password

from . import app, handlers, models


class AuthenticatedIdentity(object):
    def __init__(self, user, scopes):
        self.user = user
        self.scopes = scopes

    def __repr__(self):
        return '<{}.{} object user={}, scopes={}>'.format(self.__module__, self.__class__.__name__, self.user, self.scopes)


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
    user = user_datastore.get_user(user_id)
    if user is None:
        return None
    return AuthenticatedIdentity(user, payload['scopes'])

user_datastore = SQLAlchemyUserDatastore(models.db, models.User, models.Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_default_user():
    models.db.create_all()
    new_role = user_datastore.find_or_create_role('admin')
    new_role2 = user_datastore.find_or_create_role('user:profile')
    new_user = user_datastore.create_user(name='scott', password='pass')
    user_datastore.add_role_to_user(new_user, new_role)
    user_datastore.add_role_to_user(new_user, new_role2)
    new_user2 = user_datastore.create_user(name='test', password='pass')
    user_datastore.add_role_to_user(new_user2, new_role2)
    models.db.session.commit()
    new_location = models.Location(user_id=new_user.user_id, location_string='Timbuktu', active=True, date_time=datetime.datetime.now())
    models.db.session.add(new_location)
    new_location2 = models.Location(user_id=new_user.user_id, location_string='Stanford', active=True, date_time=datetime.datetime.now() - datetime.timedelta(500))
    models.db.session.add(new_location2)
    new_location3 = models.Location(user_id=new_user.user_id, location_string='Secret Location', active=False, date_time=datetime.datetime.now() - datetime.timedelta(50))
    models.db.session.add(new_location3)
    models.db.session.commit()

models.db.create_all()

jwt = JWT(app=None, authentication_handler=authenticate, identity_handler=identity)
jwt.app = app
jwt.auth_request_callback = handlers.auth_request_handler
jwt.jwt_encode_callback = handlers.encode_handler
jwt.jwt_payload_callback = handlers.payload_handler
jwt.auth_response_callback = handlers.auth_response_handler
jwt.init_app(jwt.app)
