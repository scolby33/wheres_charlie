from ..handlers import auth_request_handler


def token_post(body) -> str:
    return auth_request_handler()
