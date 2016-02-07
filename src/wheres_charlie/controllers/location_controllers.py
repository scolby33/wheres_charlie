from ..handlers import jwt_required
from .. import models


    query = models.Location.query.order_by(models.Location.date_time).all()
    return models.LocationSchema().dump(*query).data
def locations_get(per_page=10, page=1, reverse_chronological=False, show_hidden=False) -> str:


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
