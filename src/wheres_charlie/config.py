class Config(object):
    DEBUG = False

    SECURITY_USER_IDENTITY_ATTRIBUTES = ['user_id', 'name']

    JWT_AUTH_SCOPES_KEY = 'scopes'
    JWT_AUTH_URL_RULE = None


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    SECRET_KEY = 'secret'
    JWT_SECRET_KEY = 'secret'
