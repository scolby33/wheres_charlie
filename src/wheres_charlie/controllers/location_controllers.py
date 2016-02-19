from flask_jwt import current_identity

from ..jwt_handlers import jwt_required, jwt_optional
from .. import models, exceptions


# TODO: user:post vs user:profile for hidden updates
# TODO: more detailed error messages a la flask_jwt

@jwt_optional()
def locations_get(per_page=10, page=1, reverse_chronological=True, show_hidden=False) -> str:
    query = models.Location.query

    if show_hidden:
        authenticated_scopes = getattr(current_identity, 'scopes', set())
        if 'admin' in authenticated_scopes:
            pass
        elif 'user:profile' in authenticated_scopes:
            current_user = getattr(current_identity, 'user', None)
            query = query.filter((models.Location.active == True) |
                                 ((models.Location.active == False) & (models.Location.user == current_user)))
        else:
            raise exceptions.ClientError('You do not have the required authorization to see hidden records.', status_code=401)
    else:
        query = query.filter_by(active=True)

    if reverse_chronological:
        query = query.order_by(models.Location.date_time.desc())
    else:
        query = query.order_by(models.Location.date_time.asc())

    query = query.paginate(page, per_page, False)

    if query.total:
        return models.LocationSchema(many=True).dump(query.items).data
    else:
        raise exceptions.ClientError('No locations found matching this query.', status_code=404)


@jwt_required({'admin', 'user:post'})
def locations_post(body) -> str:  # TODO: do I need try/except/finally in here?
    try:
        if body.get('user_id'):
            authenticated_scopes = getattr(current_identity, 'scopes', set())
            if 'admin' in authenticated_scopes:
                pass
            elif body['user_id'] != current_identity.user.user_id:
                raise exceptions.ClientError('You are not authorized to perform this action.', status_code=401)

        new_location = models.LocationSchema().load(body).data

        models.db.session.add(new_location)
    except:
        models.db.session.rollback()
        raise

    models.db.session.commit()

    return models.LocationSchema().dump(new_location).data, 201


@jwt_optional()
def locations_id_get(id) -> str:
    query = models.Location.query

    authenticated_scopes = getattr(current_identity, 'scopes', set())
    if 'admin' in authenticated_scopes:
        query = query.filter_by(location_id=id)
    elif 'user:profile' in authenticated_scopes:
        current_user = getattr(current_identity, 'user', None)
        query = query.filter((models.Location.active == True) |
                             ((models.Location.active == False) & (models.Location.user == current_user)))\
                             .filter_by(location_id=id)
    else:
        query = query.filter_by(active=True).filter_by(location_id=id)

    if query.count():
        return models.LocationSchema().dump(query.first()).data
    else:
        raise exceptions.ClientError('No location with this id.', status_code=404)


@jwt_required({'admin', 'user:post'})
def locations_id_delete(id) -> str:  # TODO: do I need try/except/finally in here?
    try:
        location = models.Location.query.get(id)
        if not location or (not location.active and location.user != current_identity.user):
            raise exceptions.ClientError('The requested location does not exist.', status_code=404)
        if 'admin' in current_identity.scopes:
            models.db.session.delete(location)
        elif current_identity.user == location.user:
            models.db.session.delete(location)
        else:
            raise exceptions.ClientError('You are not authorized to perform this action.', status_code=401)
    except:
        models.db.session.rollback()
        raise

    models.db.session.commit()

    return 'Deletion successful', 204


@jwt_required({'admin', 'user:post'})
def locations_id_patch(id, body) -> str:
    try:
        location = models.Location.query.get(id)
        if 'admin' in current_identity.scopes:
            models.LocationSchema().load(body, instance=location)
        elif current_identity.user == location.user and body.get('user', True) == current_identity.user.user_id:
            models.LocationSchema().load(body, instance=location)
        else:
            raise exceptions.ClientError('You are not authorized to perform this action', status_code=401)
    except:
        models.db.session.rollback()
        raise

    models.db.session.commit()

    return models.LocationSchema().dump(location).data
