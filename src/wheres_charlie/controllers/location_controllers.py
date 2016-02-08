from flask_jwt import current_identity

from ..handlers import jwt_required, jwt_optional
from .. import models


@jwt_optional()
def locations_get(per_page=10, page=1, reverse_chronological=True, show_hidden=False) -> str:
    query = models.Location.query

    if not show_hidden or 'admin' not in current_identity.scopes:  # TODO fails if current_identity is None
        query = query.filter_by(active=True)

    if reverse_chronological:
        query = query.order_by(models.Location.date_time.desc())
    else:
        query = query.order_by(models.Location.date_time.asc())

    query = query.paginate(page, per_page, True)

    rv = []
    for row in query.items:
        rv.append(models.LocationSchema().dump(row).data)

    return rv


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
