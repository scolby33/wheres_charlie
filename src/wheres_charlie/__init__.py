import connexion

app = connexion.App(__name__, 8080, 'swagger/')
app.add_api('swagger.yaml')

from . import jwt
