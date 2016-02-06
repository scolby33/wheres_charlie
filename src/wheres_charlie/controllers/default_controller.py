from ..handlers import jwt_required


def locations_get(perPage, page, reverseChronological, showHidden) -> str:
    return 'do some magic!'


@jwt_required({'admin', 'user:post'})
def locations_post(body) -> str:
    return 'do some magic!'


@jwt_required({'admin'})
def locations_delete() -> str:
    return 'do some magic!'


def locations_id_get(id) -> str:
    return 'do some magic!'


@jwt_required({'admin', 'user:post'})
def locations_id_delete(id) -> str:
    return 'do some magic!'


@jwt_required({'admin', 'user:post'})
def locations_id_patch(id, body) -> str:
    return 'do some magic!'


def token_post(grantType, username, password, scope) -> str:
    return 'do some magic!'


def users_get(perPage, page, showHidden) -> str:
    return 'do some magic!'


@jwt_required({'admin'})
def users_post(body) -> str:
    return 'do some magic!'


@jwt_required({'admin'})
def users_delete() -> str:
    return 'do some magic!'


def users_id_get(id) -> str:
    return 'do some magic!'


@jwt_required({'admin', 'user:profile'})
def users_id_delete(id) -> str:
    return 'do some magic!'


@jwt_required({'admin', 'user:profile'})
def users_id_patch(id, body) -> str:
    return 'do some magic!'


def users_id_locations_get(id, perPage, page, reverseChronological, showHidden) -> str:
    return 'do some magic!'


def users_id_locations_latest_get(id) -> str:
    return 'do some magic!'
