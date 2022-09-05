from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config


@view_config(route_name='mapbox_token', renderer='json')
def get_mapbox_token(request) -> str:
    type_of_token = request.registry.settings['mapbox_access_token_file']

    if type_of_token == 'private':
        from langworld_db_pyramid.maputils.mapbox_token_private import token
    elif type_of_token == 'public':
        from langworld_db_pyramid.maputils.mapbox_token_public import token
    else:
        raise HTTPNotFound()

    return token
