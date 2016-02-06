from ..handlers import jwt_required
from .. import models


def locations_get(perPage=10, page=0, reverseChronological=True, showHidden=False) -> str:
    query = models.Location.query.order_by(models.Location.date_time).all()
    return models.LocationSchema().dump(*query).data


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
