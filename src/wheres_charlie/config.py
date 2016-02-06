class Config(object):
    DEBUG = False

    JWT_AUTH_SCOPES_KEY = 'scopes'


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    SECRET_KEY = 'secret'
    JWT_SECRET_KEY = 'secret'
