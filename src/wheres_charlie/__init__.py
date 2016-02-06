import connexion

con = connexion.App(__name__, 8080, 'swagger/')
app = con.app

app.config.from_object('wheres_charlie.config.DevelopmentConfig')

con.add_api('swagger.yaml')

from . import models
from . import jwt
