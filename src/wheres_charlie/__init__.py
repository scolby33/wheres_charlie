import connexion

app = connexion.App(__name__, 8080, 'swagger/')

app.app.config.from_object('wheres_charlie.config.DevelopmentConfig')

app.add_api('swagger.yaml')

from . import models
from . import jwt
