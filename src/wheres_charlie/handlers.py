import datetime
from functools import wraps

import jwt

from flask import current_app, request, jsonify, _request_ctx_stack
from flask_jwt import JWTError
from werkzeug.local import LocalProxy

_jwt = LocalProxy(lambda: current_app.extensions['jwt'])


# Handlers for making an authorization request
def auth_request_handler():
    data = request.get_json()
    if data:
        username = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
        password = data.get(current_app.config.get('JWT_AUTH_PASSWORD_KEY'), None)
        # TODO fix this set
        scopes = set(data.get(current_app.config.get('JWT_AUTH_SCOPES_KEY'), set()))
        criterion = [username, password, scopes, len(data) == 3]
    else:
        raise JWTError('Bad Request', 'Invalid credentials')

    if not all(criterion):
        raise JWTError('Bad Request', 'Invalid credentials')

    identity = _jwt.authentication_callback(username, password, scopes)

    if identity:
        access_token = _jwt.jwt_encode_callback(identity, scopes)
        return _jwt.auth_response_callback(access_token, identity)
    else:
        raise JWTError('Bad Request', 'Invalid credentials')


def encode_handler(identity, scopes):
    secret = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

    payload = _jwt.jwt_payload_callback(identity, scopes)
    missing_claims = list(set(required_claims) - set(payload.keys()))

    if missing_claims:
        raise RuntimeError('Payload is missing required claims: %s' % ', '.join(missing_claims))

    headers = _jwt.jwt_headers_callback(identity)

    return jwt.encode(payload, secret, algorithm=algorithm, headers=headers)


def payload_handler(identity, scopes):
    iat = datetime.datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    sub = getattr(identity, 'user_id') or identity['user_id']
    # expiration, issued at, not before, subject, scopes
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'sub': sub, 'scopes': list(scopes)}


def auth_response_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8')})


# JWT verification and wrappers
def _jwt_required(scopes, realm):
    """Does the actual work of verifying the JWT data in the current request.
    This is done automatically for you by `jwt_required()` but you could call it manually.
    Doing so would be useful in the context of optional JWT access in your APIs.

    :param scopes: a set of scopes that can authenticate this endpoint--any ONE from the list will allow authentication
    :param realm: an optional realm
    """
    token = _jwt.request_callback()

    if token is None:
        raise JWTError('Authorization Required', 'Request does not contain an access token',
                       headers={'WWW-Authenticate': 'JWT realm="%s"' % realm})

    try:
        payload = _jwt.jwt_decode_callback(token)
    except jwt.InvalidTokenError as e:
        raise JWTError('Invalid token', str(e))

    _request_ctx_stack.top.current_identity = identity = _jwt.identity_callback(payload)

    if identity is None:
        raise JWTError('Invalid JWT', 'User does not exist')
    elif scopes:
            if not scopes.intersection(payload['scopes']):
                raise JWTError('Invalid JWT', 'Token has wrong scope')


def jwt_required(scopes=None, realm=None):
    """View decorator that requires a valid JWT token to be present in the request

    :param scopes: a set of scopes that can authenticate this endpoint--any ONE from the list will allow authentication
    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(scopes, realm or current_app.config['JWT_DEFAULT_REALM'])
            return fn(*args, **kwargs)
        return decorator
    return wrapper
