from flask_jwt import current_identity

from ..jwt_handlers import jwt_required, jwt_optional
from .. import models, exceptions, security


@jwt_optional()
def users_get(per_page=10, page=1, show_hidden=False) -> str:
    query = models.User.query

    if show_hidden:
        authenticated_scopes = getattr(current_identity, 'scopes', set())
        if 'admin' in authenticated_scopes:
            pass
        elif 'user:profile' in authenticated_scopes:
            current_user = getattr(current_identity, 'user', None)
            query = query.filter((models.User.active == True) |
                                 ((models.User.active == False) * (models.User == current_user)))
        else:
            raise exceptions.ClientError('You do not have the required authorization to see hidden records.', status_code=401)
    else:
        query = query.filter_by(active=True)
    query = query.order_by(models.User.user_id.asc())
    query = query.paginate(page, per_page, False)
    if query.total:
        return models.UserSchema(many=True).dump(query.items).data
    else:
        raise exceptions.ClientError('No users found matching this query.', status_code=404)


@jwt_required({'admin'})
def users_post(body) -> str:
    return 'do some magic!'


@jwt_optional()
def users_id_get(id) -> str:
    requested_user = security.user_datastore.get_user(id)

    if not requested_user:
        raise exceptions.ClientError('No user with this id', status_code=404)
    elif not requested_user.active:
        authenticated_scopes = getattr(current_identity, 'scopes', set())
        if not ('admin' in authenticated_scopes or
                        'user:profile' in authenticated_scopes and current_identity.user == requested_user):
            raise exceptions.ClientError('No user with this id', status_code=404)
    return models.UserSchema().dump(requested_user).data


@jwt_required({'admin', 'user:profile'})
def users_id_delete(id) -> str:  # TODO: do I need a try/except block?
    requested_user = security.user_datastore.get_user(id)
    if not requested_user:
        raise exceptions.ClientError('No user with this id', status_code=404)
    else:
        authenticated_scopes = getattr(current_identity, 'scopes', set())
        if not('admin' in authenticated_scopes or
               'user:profile' in authenticated_scopes and current_identity.user == requested_user):
            raise exceptions.ClientError('No user with this id', status_code=404)  # TODO: right error code? What if user is hidden?
    security.user_datastore.delete_user(requested_user)
    models.db.session.commit()
    return 'Deletion successful', 204


@jwt_required({'admin', 'user:profile'})
def users_id_patch(id, body) -> str:
    return 'do some magic!'


def users_id_locations_get(id, per_page, page, reverse_chronological, show_hidden) -> str:
    return 'do some magic!'


def users_id_locations_latest_get(id) -> str:
    return 'do some magic!'
