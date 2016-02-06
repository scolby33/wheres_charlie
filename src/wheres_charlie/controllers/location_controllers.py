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
